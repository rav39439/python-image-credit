from celery import Celery
from Upload.supabase_uploader import upload_file_to_supabase

celery_app = Celery(
    "worker",
   broker="redis://redis:6379/0",
   backend="redis://redis:6379/0"
)

@celery_app.task
def submit_task(file_bytes, filename, username, email, content_type):
    # print(f"{filename}, {username},{email} are registered")
    upload_file_to_supabase(file_bytes, filename, email, content_type)