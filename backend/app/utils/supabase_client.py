"""Supabase client and database utilities."""
import os
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY

# Initialize Supabase client (for public operations)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize admin client (for server-side operations requiring service role)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def init_db():
    """Initialize database tables (run once on startup or manually)."""
    try:
        # Check if tables exist by querying them
        supabase_admin.table("profiles").select("*").limit(1).execute()
        print("✓ Database tables already exist")
        return True
    except Exception as e:
        print(f"⚠ Database tables may not exist yet: {e}")
        print("Run: python backend/app/utils/migrations.py to initialize")
        return False


def get_user_profile(user_id: str):
    """Get user profile from database."""
    response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return response.data


def save_transaction(user_id: str, transaction_data: dict):
    """Save transaction to database."""
    data = {
        **transaction_data,
        "user_id": user_id,
    }
    response = supabase.table("transactions").insert(data).execute()
    return response.data


def save_liveness_check(user_id: str, check_data: dict):
    """Save voice liveness check result."""
    data = {
        **check_data,
        "user_id": user_id,
    }
    response = supabase.table("voice_liveness_checks").insert(data).execute()
    return response.data


def get_risk_events(user_id: str, limit: int = 10):
    """Get recent risk events for user."""
    response = (
        supabase.table("risk_events")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def save_risk_event(user_id: str, event_data: dict):
    """Save risk event to database."""
    data = {
        **event_data,
        "user_id": user_id,
    }
    response = supabase.table("risk_events").insert(data).execute()
    return response.data
