from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.api.models import EmailRequest, AlertThreshold
from app.services.weather_service import fetch_weather, get_weather_summary
from app.services.email_service import send_email_alert
from app.core.database import threshold_collection
from app.core.config import CITIES, STATIC_DIR

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    with open(f"{STATIC_DIR}/index.html") as f:
        return f.read()

@router.get("/fetch_weather/{city}")
def get_weather(city: str):
    return fetch_weather(city)

@router.post("/send_email/")
def send_email(request: EmailRequest):
    return send_email_alert(request)

@router.get("/weather_summary/{city}")
def weather_summary(city: str):
    return get_weather_summary(city)

@router.post("/set_alert/")
def set_alert_threshold(alert: AlertThreshold):
    if alert.city not in CITIES:
        raise HTTPException(status_code=400, detail="Invalid city name")
    
    if alert.temperature_threshold is None or alert.temperature_threshold < -100:
        raise HTTPException(status_code=400, detail="Invalid temperature threshold")
    
    threshold_collection.update_one(
        {"email": alert.email, "city": alert.city},
        {"$set": {"temperature_threshold": alert.temperature_threshold}},
        upsert=True
    )
    
    return {
        "message": f"Alert threshold set for {alert.city} for user {alert.email}"
    }

@router.get("/remove_threshold/")
def remove_threshold(email: str, city: str):
    if city not in CITIES:
        raise HTTPException(status_code=400, detail="Invalid city name")
    
    threshold_collection.delete_one({"email": email, "city": city})
    
    return {
        "message": f"Alert threshold removed for {city} for user {email}"
    }

@router.get("/get_alert_thresholds/")
def get_alert_thresholds(email: str):
    thresholds = list(threshold_collection.find({"email": email}, {"_id": 0, "city": 1, "temperature_threshold": 1}))
    return {"alert_thresholds": thresholds}