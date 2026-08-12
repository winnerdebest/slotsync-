import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.device import FCMDevice

logger = logging.getLogger("slotsync.notifications")

_firebase_initialized = False

try:
    import firebase_admin
    from firebase_admin import credentials, messaging

    if settings.FIREBASE_CREDENTIALS_FILE:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        logger.info("Firebase Admin initialized successfully.")
except Exception as e:
    logger.warning(f"Firebase Admin initialization skipped: {e}")


async def send_push_notification(
    db: AsyncSession,
    user_id: str,
    title: str,
    body: str,
    data: Optional[dict] = None,
) -> bool:
    """
    Sends push notification to all FCM registered devices for a specific user.
    Falls back gracefully to logging if Firebase is not configured.
    """
    result = await db.execute(select(FCMDevice).where(FCMDevice.user_id == user_id))
    devices = result.scalars().all()
    tokens = [dev.fcm_token for dev in devices]

    logger.info(f"[PUSH NOTIFICATION LOG] User={user_id} | Title='{title}' | Body='{body}' | Data={data} | DeviceTokensCount={len(tokens)}")

    if not tokens or not _firebase_initialized:
        return False

    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            data={k: str(v) for k, v in (data or {}).items()},
            tokens=tokens,
        )
        response = messaging.send_each_for_multicast(message)
        logger.info(f"FCM Multicast sent: success={response.success_count}, failure={response.failure_count}")
        return True
    except Exception as exc:
        logger.error(f"Error sending FCM message: {exc}")
        return False
