import os
from supabase import create_client
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
bucket_name = os.getenv("SUPABASE_BUCKET")


supabase = create_client(supabase_url, supabase_key)