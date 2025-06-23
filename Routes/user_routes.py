from fastapi import APIRouter, Depends, Header, HTTPException, Form ,Request
from typing import Optional
from Auth.auth import verify_supabase_token
from Config.config import supabase
router = APIRouter()
from urllib.parse import parse_qs
@router.post("/register")
def register(email: str = Form(...),
    password: str = Form(...)):
    try:
        # 1. Register user in Supabase Auth
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if result.user is None:
            raise HTTPException(status_code=400, detail="Failed to register")
        user_id = result.user.id
        # 2. Create corresponding profile with credits
        profile = {
            "authid": user_id,
            "email": email,
            "credits": 10  # Default credits
        }
        supabase.table("profiles").insert(profile).execute()
        return {
            "message": "User registered successfully",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/login")
def login(email: str = Form(...),
    password: str = Form(...)):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if result.session is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": result.session.access_token,
            "user": {
                "id": result.user.id,
                "email": result.user.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Helper to extract user info from JWT and return full profile
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    payload = verify_supabase_token(token)
    email = payload.get("email")
    # Fetch profile from Supabase
    result = supabase.table("profiles").select("*").eq("email", email).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User profile not found")
    return result.data


@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return user  # returns full profile including email, credits, etc.

@router.get("/auth/callback")
def auth_callback(request: Request):
    # Get tokens from query params
    access_token = request.query_params.get("access_token")
    refresh_token = request.query_params.get("refresh_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="No token found")

    # Optional: verify the JWT (optional if you trust Supabase redirect)
    try:
        user_data = verify_supabase_token(access_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Optional: Fetch profile from DB
    profile_res = supabase.table("profiles").select("*").eq("id", user_data["sub"]).single().execute()

    profile = profile_res.data if profile_res.data else None

    # Return data (you could also redirect to frontend if needed)
    return {
        "message": "Authenticated successfully",
        "access_token": access_token,
        "user_id": user_data.get("sub"),
        "email": user_data.get("email"),
        "profile": profile
    }