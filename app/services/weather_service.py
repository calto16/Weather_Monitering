import asyncio
import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.config import API_KEY, CITIES, WEATHER_API_URL
from app.core.database import weather_collection, summary_collection
from app.utils.helpers import kelvin_to_celsius

def fetch_weather_data(city):
    params = {"q": city, "appid": API_KEY}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": city,
            "main": data["weather"][0]["main"],
            "temp": kelvin_to_celsius(data["main"]["temp"]),  
            "feels_like": kelvin_to_celsius(data["main"]["feels_like"]), 
            "dt": data["dt"],
            "timestamp": datetime.utcnow()
        }
        weather_collection.insert_one(weather_data)
        return {key: weather_data[key] for key in weather_data if key != "_id"}
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")

async def continuous_fetch_weather():
    while True:
        for city in CITIES:
            fetch_weather_data(city)
        await asyncio.sleep(5 * 60)  # Wait for 5 minutes

async def start_continuous_fetch_weather():
    asyncio.create_task(continuous_fetch_weather())

def fetch_weather(city: str):
    if city not in CITIES:
        raise HTTPException(status_code=400, detail="Invalid city name")

    weather_data = weather_collection.find_one(
        {"city": city}, 
        sort=[("timestamp", -1)]
    )

    if not weather_data:
        raise HTTPException(status_code=404, detail="No weather data found for this city")
    
    return {key: weather_data[key] for key in weather_data if key != "_id"}

def get_weather_summary(city: str):
    now = datetime.utcnow()
    last_24_hours = now - timedelta(hours=24)
    weather_data = list(weather_collection.find({
        "city": city,
        "timestamp": {"$gte": last_24_hours}
    }))
    
    if not weather_data:
        raise HTTPException(status_code=404, detail="No data found for the past 24 hours")

    temps = [data["temp"] for data in weather_data]
    conditions = [data["main"] for data in weather_data]
    
    summary = {
        "city": city,
        "average_temperature": sum(temps) / len(temps),
        "max_temperature": max(temps),
        "min_temperature": min(temps),
        "dominant_weather_condition": max(set(conditions), key=conditions.count),
        "feels_like": weather_data[-1]["feels_like"],
        "dt": weather_data[-1]["dt"],
        "timestamp": now
    }

    try:
        summary_collection.insert_one(summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save summary: {str(e)}")

    summary["_id"] = str(summary_collection.find_one({"city": city, "timestamp": now})["_id"])

    return summary