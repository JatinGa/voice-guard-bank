## Voice Feature Implementation - Complete Guide

### What's Working Now

#### 1. **Voice Recording & Transcription** ✅
- Uses Web Speech API for real-time speech recognition (supports English - India accent)
- Fallback to audio recording if Web Speech API not available
- Automatically transcribes voice input without server dependency
- Works offline (no internet required for transcription)

#### 2. **Liveness Check (Anti-Deepfake)** ✅
- Prompts user with random challenge phrase (e.g., "green mango")
- Analyzes transcript for:
  - Challenge phrase matching
  - Filler words (umm, uhh, er, ah, etc.)
  - Natural speech patterns
- Returns liveness score (0-100)
- **Blocks transaction if score < 50** (deepfake detection)

#### 3. **Voice Task Execution** ✅
- Say "check my balance" → automatically fetches and displays balance
- Say "recent transactions" → automatically shows last 5 transactions
- Say "transfer" → prompts for transfer details
- Say "scam" or "fraud" → triggers guardian alert

#### 4. **Mock Banking API** ✅
- Check Balance: Returns ₹45,230.50
- Recent Transactions: Returns 5 sample transactions
- Transfer Money: Simulates transfer completion
- All functions work without backend server

#### 5. **Hardcoded Chat Fallback** ✅
- When `VITE_USE_ML=false`, shows 4 buttons:
  - Check Balance
  - Recent Transactions
  - Transfer Money
  - Report Scam
- Each button executes real mock banking operations

#### 6. **Scam Detection** ✅
- Detects scam phrases: "share otp", "account is blocked", "kyc expired", etc.
- Shows HIGH risk warning and triggers guardian alert
- Prevents transaction execution

#### 7. **Guardian Alert Modal** ✅
- Shows when risk is HIGH or deepfake detected
- Can notify guardians (UI ready, notification service not integrated)

#### 8. **Risk Scoring** ✅
- Combines multiple signals (stress, scam phrases, device, amount)
- Returns structured reasons
- Explainable AI - tells user WHY transaction is risky

### How to Test the Voice Feature

#### Prerequisites
- Modern browser with microphone access (Chrome, Edge, Firefox, Safari)
- Allow microphone permission when prompted

#### Quick Test Steps
1. Click the **Mic button** in the chat
2. Speak clearly: "Check my balance"
3. The system will:
   - Show a random challenge phrase
   - Ask you to repeat it
   - Analyze your speech for liveness
   - Execute the balance check
   - Display your balance

#### Try These Voice Commands
```
"check my balance"          → Shows ₹45,230.50
"recent transactions"       → Lists last 5 transactions
"show transactions"         → Same as above
"transfer money"            → Prompts for transfer details
"send money"                → Same as above
"report scam"               → Triggers guardian alert
"scam"                      → Triggers guardian alert
"fraud"                     → Triggers guardian alert
```

### File Structure

```
src/
├── components/
│   ├── VoiceButton.tsx         # Voice recording + Web Speech API
│   ├── GuardianAlert.tsx       # Guardian approval modal
│   ├── OTPModal.tsx            # OTP verification modal
│   └── RiskScoreCard.tsx       # Risk level display
├── pages/
│   ├── Assistant.tsx           # Main chat orchestration
│   ├── Auth.tsx                # Authentication
│   └── Index.tsx               # Landing page
└── lib/
    ├── mockApi.ts              # Mock banking & liveness service
    └── phraseList.ts           # Scam phrases & challenge words
```

### Architecture

```
User speaks
    ↓
VoiceButton uses Web Speech API
    ↓
Get transcript + liveness score
    ↓
Voice result handler in Assistant.tsx
    ↓
Auto-detect command (balance, transfer, etc.)
    ↓
Call mockApiService based on command
    ↓
Display results in chat
```

### Mock Banking API Functions

All in `src/lib/mockApi.ts`:

```typescript
mockApiService.voiceLiveness(transcript, challengePhrase)
// Returns: { score, passed, reason, transcript }

mockApiService.mockBanking('get_balance')
// Returns: { balance, currency, account_number, last_updated }

mockApiService.mockBanking('get_transactions')
// Returns: { transactions: [...] }

mockApiService.mockBanking('transfer')
// Returns: { success, transaction_id, message, new_balance }
```

### Running the App

#### Start Development Server
```powershell
npm install
npm run dev
```

The app will be at `http://localhost:8080` (or the port shown in terminal)

#### Enable Fallback Mode (No ML)
```powershell
# In .env.local
VITE_USE_ML=false
```

This shows hardcoded option buttons instead of relying on ML transcription.

#### Test Without Microphone
- Use the hardcoded option buttons (fallback mode)
- Type commands in the text input
- The app will still process them

### Current Limitations & Next Steps

#### What's Still Mock
- Speech-to-text uses browser's Web Speech API (limited accuracy)
- Liveness check is simple pattern-matching (not ML-based)
- Stress/emotion detection is not yet implemented
- Guardian notifications don't actually send SMS/email
- Database tables not created (risk_events, devices, profiles)

#### What You Can Improve
1. **Better ASR**: Integrate OpenAI Whisper or AssemblyAI
2. **Real Liveness**: Use Resemblyzer or SpeechBrain for speaker verification
3. **Emotion Detection**: Add speech analysis for stress detection
4. **Database**: Create Supabase tables and connect risk-evaluate function
5. **Notifications**: Integrate Twilio for SMS or email service
6. **Accent Adaptation**: Add language_hint for regional dialects

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Microphone not working | Check browser permissions, try different browser |
| Web Speech API not available | Use fallback mode or try Chrome/Edge |
| Commands not recognized | Speak clearly, try simpler phrases |
| Balance not showing | Check mockApi.ts is imported in Assistant.tsx |
| High liveness score needed | Avoid filler words (umm, uhh, er, ah) |

### Environment Variables

Create `.env.local`:
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_USE_ML=true  # Set to false for hardcoded fallback
```

### Security Notes

- All voice processing happens on the client (browser)
- No audio is sent to external servers in this demo
- For production, integrate secure cloud services for:
  - Real ASR (Whisper, AssemblyAI)
  - Speaker verification (dedicated services)
  - Risk evaluation (secure backend)
  - Transaction execution (banking APIs)

### Testing Checklist

- [ ] Mic button works and requests permission
- [ ] Says random challenge phrase
- [ ] Accepts voice input
- [ ] Displays transcript in chat
- [ ] Shows liveness score (70-90 for normal speech)
- [ ] Auto-executes "check balance" command
- [ ] Shows balance result
- [ ] "Recent transactions" returns 5 items
- [ ] Scam phrase detection works
- [ ] Guardian alert shows on high-risk
- [ ] Fallback buttons work (if VITE_USE_ML=false)
- [ ] Typing commands also works
