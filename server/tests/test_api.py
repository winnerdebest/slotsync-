import pytest
from datetime import date, timedelta


@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_full_slotsync_flow(async_client):
    # 1. Register a Creator (Doctor)
    creator_reg = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "doctor@slotsync.com",
            "password": "Password123!",
            "full_name": "Dr. Sarah Connor",
            "role": "CREATOR",
        },
    )
    assert creator_reg.status_code == 201
    creator_user = creator_reg.json()

    # 2. Login Creator
    creator_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "doctor@slotsync.com", "password": "Password123!"},
    )
    assert creator_login.status_code == 200
    creator_token = creator_login.json()["access_token"]
    creator_headers = {"Authorization": f"Bearer {creator_token}"}

    # 3. Creator updates profile category to 'Doctor'
    profile_update = await async_client.put(
        "/api/v1/creators/me",
        headers=creator_headers,
        json={
            "category": "Doctor",
            "title": "Cardiologist Specialist",
            "hourly_rate": 150.0,
            "slot_duration_minutes": 30,
        },
    )
    assert profile_update.status_code == 200
    creator_profile = profile_update.json()
    creator_profile_id = creator_profile["id"]

    # 4. Creator sets weekly availability (e.g. Monday = 09:00 - 11:00)
    avail_res = await async_client.post(
        "/api/v1/availability",
        headers=creator_headers,
        json={
            "rules": [
                {"day_of_week": 0, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 1, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 2, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 3, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 4, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 5, "start_time": "09:00", "end_time": "11:00"},
                {"day_of_week": 6, "start_time": "09:00", "end_time": "11:00"},
            ]
        },
    )
    assert avail_res.status_code == 200
    assert len(avail_res.json()) == 7

    # 5. Register a Client
    client_reg = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "client@slotsync.com",
            "password": "Password123!",
            "full_name": "John Doe",
            "role": "CLIENT",
        },
    )
    assert client_reg.status_code == 201

    # 6. Login Client
    client_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "client@slotsync.com", "password": "Password123!"},
    )
    assert client_login.status_code == 200
    client_token = client_login.json()["access_token"]
    client_headers = {"Authorization": f"Bearer {client_token}"}

    # 7. Client searches creators filtered by 'Doctor'
    search_res = await async_client.get("/api/v1/creators?category=Doctor")
    assert search_res.status_code == 200
    creators_found = search_res.json()
    assert len(creators_found) >= 1

    # 8. Client queries available slots for target date
    target_date_str = (date.today() + timedelta(days=1)).isoformat()
    slots_res = await async_client.get(
        f"/api/v1/availability/{creator_profile_id}/slots?date={target_date_str}"
    )
    assert slots_res.status_code == 200
    slots = slots_res.json()
    assert len(slots) == 4  # 09:00-09:30, 09:30-10:00, 10:00-10:30, 10:30-11:00

    first_slot_start = slots[0]["start_time_utc"]

    # 9. Client books first slot
    booking_res = await async_client.post(
        "/api/v1/appointments",
        headers=client_headers,
        json={
            "creator_id": creator_profile_id,
            "start_time_utc": first_slot_start,
            "notes": "Chest pain checkup",
        },
    )
    assert booking_res.status_code == 201
    booking_data = booking_res.json()
    assert booking_data["status"] == "CONFIRMED"

    # 10. Verify double-booking same slot fails with 409 Conflict
    conflict_res = await async_client.post(
        "/api/v1/appointments",
        headers=client_headers,
        json={
            "creator_id": creator_profile_id,
            "start_time_utc": first_slot_start,
            "notes": "Second attempt booking",
        },
    )
    assert conflict_res.status_code == 409

    # 11. Verify open slots now has 3 available instead of 4
    slots_res_after = await async_client.get(
        f"/api/v1/availability/{creator_profile_id}/slots?date={target_date_str}"
    )
    assert len(slots_res_after.json()) == 3
