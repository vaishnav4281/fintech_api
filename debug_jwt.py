from jose import jwt
from app.config import get_settings

settings = get_settings()
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzc1MTM0NDM0LCJpYXQiOjE3NzUxMzA4MzR9.CE9ShhoXnBqdsPAUkZyYn9W2u0gabYE9n-u_ovrXApw"

print(f"SECRET_KEY in app: {settings.SECRET_KEY}")

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"Successfully decoded! Payload: {payload}")
except Exception as e:
    print(f"Error decoding: {e}")
