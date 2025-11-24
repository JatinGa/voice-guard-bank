#!/usr/bin/env python3
"""
Database migration script - Creates Supabase tables.
Run this once to set up the database schema.
"""
import os
from app.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client

supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# SQL migrations
MIGRATIONS = [
    # Profiles table
    """
    CREATE TABLE IF NOT EXISTS profiles (
      id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
      username TEXT UNIQUE,
      full_name TEXT,
      avatar_url TEXT,
      phone_number TEXT,
      email TEXT,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
    """,
    
    # Transactions table
    """
    CREATE TABLE IF NOT EXISTS transactions (
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
      amount NUMERIC,
      currency TEXT DEFAULT 'INR',
      recipient_account TEXT,
      recipient_name TEXT,
      description TEXT,
      status TEXT DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
    """,
    
    # Voice liveness checks table
    """
    CREATE TABLE IF NOT EXISTS voice_liveness_checks (
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
      transcript TEXT,
      challenge_phrase TEXT,
      score INTEGER,
      passed BOOLEAN,
      confidence NUMERIC,
      created_at TIMESTAMP DEFAULT NOW()
    );
    """,
    
    # Risk events table
    """
    CREATE TABLE IF NOT EXISTS risk_events (
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
      risk_score INTEGER,
      risk_level TEXT,
      transcript TEXT,
      factors JSONB,
      transaction_id UUID REFERENCES transactions(id),
      created_at TIMESTAMP DEFAULT NOW()
    );
    """,
]


def run_migrations():
    """Execute all migrations."""
    print("🔄 Running database migrations...\n")
    
    for i, sql in enumerate(MIGRATIONS, 1):
        try:
            # This is a placeholder - Supabase doesn't have a direct SQL execution method
            # You need to use the Supabase dashboard or run these manually
            print(f"✓ Migration {i} prepared (execute in Supabase dashboard)")
        except Exception as e:
            print(f"✗ Migration {i} failed: {e}")
    
    print("\n📋 To complete setup, go to Supabase dashboard and execute these SQL commands:")
    print("=" * 60)
    for sql in MIGRATIONS:
        print(sql.strip())
        print("\n" + "=" * 60 + "\n")
    
    print("""
    After running these migrations:
    1. Go to https://supabase.com
    2. Open your project
    3. Go to SQL Editor
    4. Paste and execute each migration above
    5. Return here and run: python backend/run.py
    """)


if __name__ == "__main__":
    run_migrations()
