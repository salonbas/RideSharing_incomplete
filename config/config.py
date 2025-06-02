# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")