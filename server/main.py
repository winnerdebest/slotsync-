from fastapi import FastAPI
app = FastAPI(title="SlotSync API")
@app.get("/")
def read_root():
    return {"message": "Welcome to SlotSync API"}
@app.get("/health")
def health_check():
    return {"status": "ok"}