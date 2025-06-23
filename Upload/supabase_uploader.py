from supabase import create_client
import os
import uuid

from datetime import datetime

import uuid
from fastapi import HTTPException
from Config.config import supabase
from dotenv import load_dotenv

# from config import SUPABASE_BUCKET  # or hardcode your bucket name
load_dotenv()  # Load environment variables from .env file

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
bucket_name = os.getenv("SUPABASE_BUCKET")

supabase = create_client(supabase_url, supabase_key)
def upload_file_to_supabase(file_bytes, filename, email, content_type):
    unique_filename = f"{uuid.uuid4()}_{filename}"

    # Step 1: Fetch profile using email
    profile_res = supabase.table("profiles").select("*").eq("email", email).single().execute()

    if not profile_res.data:
        raise HTTPException(status_code=404, detail="User profile not found")

    profile = profile_res.data
    current_credits = profile.get("credits", 0)

    if current_credits <= 0:
        raise HTTPException(status_code=402, detail="Not enough credits")

    # Step 2: Deduct 1 credit
    updated_credits = current_credits - 1
    supabase.table("profiles").update({"credits": updated_credits}).eq("email", email).execute()

    # Step 3: Upload to Supabase Storage
    supabase.storage.from_(bucket_name).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={"content-type": content_type}
    )
    
    
    created_at = datetime.utcnow().isoformat() + "Z"  # Z indicates UTC
# Step 4: Insert task metadata to DB, including created_at
    supabase.table("tasks").insert({
       "filename": unique_filename,
       "email": email,
       "created_at": created_at
    }).execute()
    

    return {
        "message": "File uploaded and task created successfully",
        "filename": unique_filename,
        "remaining_credits": updated_credits
    }