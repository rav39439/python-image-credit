# from jose import jwt, JWTError
# from passlib.context import CryptContext
# import os

# SECRET_KEY = os.getenv("JWT_SECRET")
# ALGORITHM = os.getenv("JWT_ALGORITHM")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def create_access_token(data: dict):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


from fastapi import HTTPException
from jose import jwt, JWTError
import os

# Load Supabase JWT secret and algorithm
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # From Supabase Project Settings
ALGORITHM = "HS256"  # Supabase uses HS256 for signing

# ✅ Function to decode and verify token
def verify_supabase_token(token: str):
    try:
        # Decode JWT using secret
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[ALGORITHM])
        return payload  # payload includes 'sub', 'email', etc.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")