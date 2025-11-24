# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/260dc0bb-ea45-4004-8db4-5d874eac61a7

# SentinelPay

SentinelPay is a voice-first banking assistant prototype focused on preventing voice-based scams. It includes mock Supabase Edge Functions and frontend scaffolding for liveness checks, stress detection, scam phrase interruption, guardian flows, and explainable risk decisions.

## Features
- Anti–Deepfake Voice Liveness Check (challenge-response)
- Stress & emotion inference from speech (mocked)
- Scam phrase pattern interruption and warnings
- Guardian mode and OTP flows for high-risk transactions
- Explainable risk scoring with human-readable reasons
- Offline support (service worker) for basic functionality

## Quick start (Windows PowerShell)
1. Copy the example env and fill values:
```powershell
cp .env.example .env.local
notepad .env.local
```
2. Install dependencies and run dev server:
```powershell
npm install
npm run dev
```

3. (Optional) Run Supabase Edge Functions locally using Supabase CLI:
```powershell
# Install and login to supabase CLI per docs
cd supabase/functions
supabase functions serve
```

If you do not want to use ML services during development, set `VITE_USE_ML=false` in your `.env.local` and the assistant will fall back to a hardcoded menu of options.

## Files of interest
- `src/pages/Assistant.tsx` — chat UI and orchestration; contains the ML and fallback option flows
- `src/components/VoiceButton.tsx` — media recorder and upload flow
- `src/integrations/supabase/client.ts` — Supabase client bootstrap
- `supabase/functions/*` — serverless function implementations (mock transcription, NLU, risk evaluation, transaction execution, mock banking, voice-liveness)

## Security
- Never commit secret keys (service role keys, API keys). Use server-side environment variables for sensitive operations.
- The liveness and emotion detection implementations are mocked and intended as a scaffold for integrating real models on the server-side.

## Next steps
- Replace mock liveness with a proper speaker-verification model.
- Add IndexedDB queueing for offline transaction requests.
- Integrate real ASR and emotion/stress models (OpenAI/Whisper, AssemblyAI, or on-prem models).

## License & notes
This repository contains prototype code and mock functions for demonstration. Do not use as-is in production without adding proper security, testing, and model validation.
- Vite
