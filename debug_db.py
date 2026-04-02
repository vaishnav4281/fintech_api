import os
import sys

# Add project root to sys.path to allow running from scripts/ or root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.config import get_settings
from sqlalchemy import create_engine

settings = get_settings()
print(f"DATABASE_URL: {settings.DATABASE_URL}")

try:
    engine = create_engine(settings.DATABASE_URL)
    print("Engine created successfully")
    # We won't try to connect because it will fail with name resolution error here too
except Exception as e:
    print(f"Error creating engine: {e}")
