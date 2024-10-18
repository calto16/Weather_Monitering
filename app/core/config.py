import os

API_KEY = "{OPEN_WEATHER_API_KEY}"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
MONGODB_URL = "mongodb://localhost:27017/"
DB_NAME = "weather_db"
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
SENDGRID_API_KEY = "{SENDGRID_API_KEY}"
SENDER_EMAIL = 'tushar16rathod@gmail.com'