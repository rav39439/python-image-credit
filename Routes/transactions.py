from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Config.config import supabase
from uuid import UUID

router = APIRouter()

class DepositRequest(BaseModel):
    user_id: UUID
    email: str
    amount: int  # In rupees

@router.post("/deposit")
def deposit_credits(payload: DepositRequest):
    if payload.amount < 10:
        raise HTTPException(status_code=400, detail="Minimum ₹10 required")

    credits_to_add = payload.amount // 10

    # Insert into transactions table
    txn_res = supabase.table("transactions").insert({
        "user_id": str(payload.user_id),
        "email": payload.email,
        "amount": payload.amount,
        "credits_purchased": credits_to_add
    }).execute()
    # print(txn_res)

    if not txn_res.data:
        raise HTTPException(status_code=500, detail="Failed to log transaction")

    # Fetch user profile by user_id (UUID)
    profile_res = supabase.table("profiles").select("*").eq("email", str(payload.email)).single().execute()
    
    # print(profile_res)

    if not profile_res.data:
        raise HTTPException(status_code=404, detail="User profile not found")

    current_credits = profile_res.data.get("credits", 0)
    new_credits = current_credits + credits_to_add

    # Update user credits
    update_res = supabase.table("profiles").update({
        "credits": new_credits
    }).eq("email", payload.email).execute()

    # if update_res.error:
    #     raise HTTPException(status_code=500, detail="Failed to update credits")

    return {
        "message": "Credits added successfully",
        "user_id": str(payload.user_id),
        "email": payload.email,
        "amount": payload.amount,
        "credits_added": credits_to_add,
        "total_credits": new_credits
    }    
    if payload.amount < 10:
        raise HTTPException(status_code=400, detail="Minimum ₹10 required")

    credits_to_add = payload.amount // 10

    # Step 1: Add transaction record
    txn_res = supabase.table("transactions").insert({
        "user_id": payload.user_id,
        "email": payload.email,
        "amount": payload.amount,
        "credits_purchased": credits_to_add
    }).execute()

    # if txn_res.status_code >= 400:
        # raise HTTPException(status_code=500, detail="Failed to log transaction")

    # Step 2: Update user's credit balance
    profile_res = supabase.table("profiles").select("credits").eq("email", payload.email).single().execute()

    if profile_res.status_code >= 400 or not profile_res.data:
        raise HTTPException(status_code=404, detail="User profile not found")

    current_credits = profile_res.data["credits"]
    new_credits = current_credits + credits_to_add

    update_res = supabase.table("profiles").update({"credits": new_credits}).eq("id", payload.user_id).execute()

    if update_res.status_code >= 400:
        raise HTTPException(status_code=500, detail="Failed to update credits")

    return {
        "message": "Credits added successfully",
        "user_id": payload.user_id,
        "email": payload.email,
        "amount": payload.amount,
        "credits_added": credits_to_add,
        "total_credits": new_credits
    }



class EmailRequest(BaseModel):
    email: str




@router.post("/get_transactions")
def get_tasks_by_email(payload: EmailRequest):
    try:
        # Select only the fields we care about
        response = supabase.table("tasks").select("id, filename, email,created_at").eq("email", payload.email) .execute()

        # if response.status_code >= 400:
        #     raise HTTPException(status_code=500, detail="Failed to fetch tasks")

        tasks = response.data or []
        return {
            "message": "Tasks retrieved successfully",
            "transactions": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))