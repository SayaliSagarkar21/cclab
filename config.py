import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    
    # Firebase config
    FIREBASE_CREDENTIALS_PATH =  "firebase-creditionals.json"
    
    # OpenWeatherMap API
    WEATHER_API_KEY = "800577c64d9c09f92eae219696734d04"

    # Google OAuth config
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"