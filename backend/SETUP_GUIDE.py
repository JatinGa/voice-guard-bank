#!/usr/bin/env python3
"""
Supabase + Firebase Comparison and Setup Guide for SentinelPay
"""

COMPARISON = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                    SUPABASE vs FIREBASE COMPARISON                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ FEATURE                │ SUPABASE              │ FIREBASE                    │
├────────────────────────┼───────────────────────┼─────────────────────────────┤
│ Database               │ PostgreSQL (SQL)      │ Firestore (NoSQL)           │
│ Pricing                │ Pay-as-you-go         │ Pay-as-you-go               │
│ Auth                   │ ✓ JWT-based           │ ✓ Native SDK                │
│ Realtime               │ ✓ Built-in            │ ✓ Built-in                  │
│ Scalability            │ Excellent (SQL)       │ Excellent (NoSQL)           │
│ Learning Curve         │ Easier (PostgreSQL)   │ Moderate                    │
│ Server-side Code       │ Edge Functions        │ Cloud Functions             │
│ Free Tier              │ Good ($0-50/mo)       │ Good ($0-50/mo)             │
│ Best For               │ Structured data       │ Mobile/real-time apps       │
└─────────────────────────────────────────────────────────────────────────────┘

RECOMMENDATION FOR SENTINELPAY:
→ Use SUPABASE: Better for transactional banking data (users, transactions,
  risk events) which benefit from SQL structure and foreign key relationships.
→ Can use FIREBASE as alternative for real-time messaging/notifications.

╔════════════════════════════════════════════════════════════════════════════════╗
║                           SUPABASE SETUP                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

STEP 1: Create Supabase Project
────────────────────────────────
1. Go to https://app.supabase.com
2. Click "New Project"
3. Enter:
   - Project Name: "voice-guard-bank"
   - Database Password: (secure password)
   - Region: Choose closest to you
4. Click "Create new project" (takes 2-3 minutes)

STEP 2: Get API Credentials
──────────────────────────
1. Go to Settings → API
2. Copy:
   - Project URL → SUPABASE_URL
   - Anon Public Key → SUPABASE_KEY
   - Service Role Secret → SUPABASE_SERVICE_ROLE_KEY (KEEP SECRET!)
3. Paste into backend/.env

STEP 3: Create Database Tables
──────────────────────────────
1. Go to SQL Editor
2. Copy and run these SQL statements:

-- Profiles table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE,
  full_name TEXT,
  phone_number TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  amount NUMERIC,
  recipient_account TEXT,
  recipient_name TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Voice liveness checks
CREATE TABLE voice_liveness_checks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  transcript TEXT,
  challenge_phrase TEXT,
  score INTEGER,
  passed BOOLEAN,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Risk events
CREATE TABLE risk_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  risk_score INTEGER,
  risk_level TEXT,
  transcript TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

STEP 4: Enable Row Level Security (RLS)
──────────────────────────────────────
1. Go to Authentication → Policies
2. For each table, create policies:
   - Users can only see their own data
   - Admins can see all data
3. Example for profiles table:
   - SELECT: (auth.uid() = id) OR (is_admin = true)
   - INSERT/UPDATE/DELETE: (auth.uid() = id)

STEP 5: Test Connection
──────────────────────
python -c "
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv('.env', cwd='backend')
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

try:
    supabase = create_client(url, key)
    response = supabase.table('profiles').select('count', count='exact').execute()
    print('✓ Connected to Supabase!')
except Exception as e:
    print(f'✗ Error: {e}')
"

╔════════════════════════════════════════════════════════════════════════════════╗
║                          FIREBASE SETUP (ALTERNATIVE)                          ║
╚════════════════════════════════════════════════════════════════════════════════╝

If you prefer Firebase, here's the setup:

STEP 1: Create Firebase Project
───────────────────────────────
1. Go to https://console.firebase.google.com
2. Click "Create a project"
3. Enter name and enable/disable options as needed

STEP 2: Get Firebase Credentials
────────────────────────────────
1. Go to Project Settings → Service Accounts
2. Click "Generate new private key"
3. Save the JSON file (keep it secret!)
4. Copy values to backend/.env:
   FIREBASE_PROJECT_ID=xxx
   FIREBASE_PRIVATE_KEY=xxx
   FIREBASE_CLIENT_EMAIL=xxx

STEP 3: Create Firestore Database
─────────────────────────────────
1. Go to Firestore Database
2. Create Database (choose region)
3. Start in Production Mode
4. Create collections:
   - users/{userId}/transactions
   - users/{userId}/liveness_checks
   - risk_events/{eventId}

STEP 4: Python Integration
──────────────────────────
pip install firebase-admin

from firebase_admin import initialize_app, credentials, firestore

cred = credentials.Certificate('firebase-key.json')
initialize_app(cred)
db = firestore.client()

# Save data
db.collection('users').document(user_id).set({
    'name': 'John',
    'balance': 45230.50
})

# Read data
doc = db.collection('users').document(user_id).get()
print(doc.to_dict())

STEP 5: Frontend Integration
────────────────────────────
npm install firebase

import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: process.env.VITE_FIREBASE_API_KEY,
  projectId: process.env.VITE_FIREBASE_PROJECT_ID,
  // ... other config
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)

╔════════════════════════════════════════════════════════════════════════════════╗
║                      QUICK DECISION TREE                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

Choose SUPABASE if:
  ✓ You want SQL database (transactions benefit from ACID guarantees)
  ✓ You need complex queries and joins
  ✓ You prefer familiar PostgreSQL
  ✓ You want edge functions in TypeScript/Python
  → RECOMMENDED FOR BANKING APP

Choose FIREBASE if:
  ✓ You want quick setup with minimal backend code
  ✓ You need real-time updates across clients
  ✓ You're building mobile-first app
  ✓ You want integrated cloud functions
  → GOOD FOR NOTIFICATIONS/MESSAGING

Our Recommendation: SUPABASE
  - Banking data is inherently structured (transactions, accounts, users)
  - SQL ensures data consistency and integrity
  - Our Python backend integrates seamlessly
  - Better for audit trails and compliance

"""

print(COMPARISON)

# Save this as a reference
if __name__ == "__main__":
    with open("backend/SUPABASE_VS_FIREBASE.txt", "w") as f:
        f.write(COMPARISON)
    print("\n✓ Guide saved to backend/SUPABASE_VS_FIREBASE.txt")
