from fastapi import APIRouter,UploadFile, Form, File
# from Workers.celery_workers import submit_task
from Upload.supabase_uploader import upload_file_to_supabase

import base64

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/upload")
async def submit_task_route(
    file: UploadFile,
    filename: str = Form(...),
    # username: str = Form(...),
    email: str = Form(...)
):
    file_bytes = await file.read()

    # submit_task.delay(
    #     file_bytes,
    #     filename,
    #     username,
    #     email,
    #     file.content_type
    # )
    
    upload_file_to_supabase(
        file_bytes,
        filename,
        email,
        file.content_type
        
    )

    base64_image = base64.b64encode(file_bytes).decode("utf-8")
    data_url = f"data:{file.content_type};base64,{base64_image}"

    return {
        "message": "Task submitted for background processing",
        "preview_data_url": data_url,
        "filename": filename,
        # "username": username,
        "email": email
    }

