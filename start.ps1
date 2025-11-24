#!/usr/bin/env powershell
# Quick startup script for SentinelPay (Windows PowerShell)
# This script sets up and runs both frontend and backend simultaneously

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('both', 'frontend', 'backend', 'local')]
    [string]$Mode = 'both',
    
    [Parameter(Mandatory=$false)]
    [switch]$Help
)

$ErrorActionPreference = "Stop"

function Show-Help {
    Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║         SentinelPay Quick Start Script                         ║
╚════════════════════════════════════════════════════════════════╝

USAGE:
    .\start.ps1 [MODE] [OPTIONS]

MODES:
    both        Start both frontend and backend (default)
    frontend    Start frontend only (local mock mode)
    backend     Start backend only (for external frontend)
    local       Run frontend in local mock mode

OPTIONS:
    -Help       Show this help message

EXAMPLES:
    .\start.ps1                 # Start both frontend and backend
    .\start.ps1 frontend        # Start only frontend
    .\start.ps1 backend         # Start only backend
    .\start.ps1 local           # Local-only development (no backend)

REQUIREMENTS:
    - Node.js 18+ (for frontend)
    - Python 3.8+ (for backend)
    - npm or bun

QUICKSTART (First Time):
    1. .\start.ps1 backend      # Terminal 1
    2. .\start.ps1 frontend     # Terminal 2
    3. Open http://localhost:8080

"@
}

function Initialize-Backend {
    Write-Host "`n📦 Initializing backend..." -ForegroundColor Cyan
    
    if (-not (Test-Path "backend")) {
        Write-Error "Error: 'backend' directory not found. Run from project root."
    }
    
    # Check if venv exists
    if (-not (Test-Path "backend\venv")) {
        Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
        python -m venv backend\venv
    }
    
    # Activate venv
    & "backend\venv\Scripts\Activate.ps1"
    
    # Install requirements
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -q -r backend\requirements.txt 2>$null | Out-Null
    
    # Check for .env
    if (-not (Test-Path "backend\.env")) {
        Write-Host "⚠️  backend\.env not found!" -ForegroundColor Yellow
        Write-Host "Creating from template..." -ForegroundColor Yellow
        Copy-Item "backend\.env.example" "backend\.env"
        Write-Host "❌ Please edit backend\.env with your Supabase credentials:" -ForegroundColor Red
        Write-Host "   - SUPABASE_URL" -ForegroundColor Gray
        Write-Host "   - SUPABASE_KEY" -ForegroundColor Gray
        Write-Host "   - SUPABASE_SERVICE_ROLE_KEY" -ForegroundColor Gray
        Write-Host "" -ForegroundColor Gray
        Write-Host "Then run again: .\start.ps1 backend" -ForegroundColor Cyan
        exit 1
    }
    
    Write-Host "✓ Backend ready" -ForegroundColor Green
}

function Initialize-Frontend {
    Write-Host "`n📦 Initializing frontend..." -ForegroundColor Cyan
    
    if (-not (Test-Path "package.json")) {
        Write-Error "Error: 'package.json' not found. Run from project root."
    }
    
    # Install dependencies
    Write-Host "Installing Node dependencies..." -ForegroundColor Yellow
    npm install -q 2>$null | Out-Null
    
    # Check for .env.local
    if (-not (Test-Path ".env.local")) {
        Write-Host "Creating .env.local..." -ForegroundColor Yellow
        @"
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:5000/api
VITE_USE_BACKEND=true
VITE_USE_ML=false
"@ | Out-File ".env.local"
        Write-Host "✓ Created .env.local (edit if needed)" -ForegroundColor Green
    }
    
    Write-Host "✓ Frontend ready" -ForegroundColor Green
}

function Start-Backend {
    Initialize-Backend
    
    Write-Host "`n🚀 Starting backend on port 5000..." -ForegroundColor Cyan
    Write-Host "Press CTRL+C to stop`n" -ForegroundColor Yellow
    
    # Activate venv and run
    & "backend\venv\Scripts\Activate.ps1"
    python backend\run.py
}

function Start-Frontend {
    Initialize-Frontend
    
    Write-Host "`n🚀 Starting frontend on port 8080..." -ForegroundColor Cyan
    Write-Host "Press CTRL+C to stop`n" -ForegroundColor Yellow
    
    npm run dev
}

function Start-Both {
    Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║    SentinelPay - Starting Frontend + Backend                  ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan
    
    Initialize-Frontend
    Initialize-Backend
    
    Write-Host "`n⚠️  For two-terminal setup:" -ForegroundColor Yellow
    Write-Host "  Terminal 1: .\start.ps1 backend" -ForegroundColor Gray
    Write-Host "  Terminal 2: .\start.ps1 frontend" -ForegroundColor Gray
    Write-Host "" -ForegroundColor Gray
    Write-Host "Starting frontend in 3 seconds..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    
    Start-Frontend
}

function Start-LocalOnly {
    Initialize-Frontend
    
    Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║    SentinelPay - Local Mode (No Backend Required)            ║
╚════════════════════════════════════════════════════════════════╝

✓ All features available locally
✓ Voice processing using Web Speech API
✓ Mock banking with hardcoded fallback

Note: For real ML models, run: .\start.ps1 backend
"@ -ForegroundColor Cyan
    
    Write-Host "`n🚀 Starting frontend on port 8080..." -ForegroundColor Cyan
    Write-Host "Press CTRL+C to stop`n" -ForegroundColor Yellow
    
    npm run dev
}

# Main logic
if ($Help) {
    Show-Help
    exit 0
}

switch ($Mode) {
    'both' { Start-Both }
    'frontend' { Start-Frontend }
    'backend' { Start-Backend }
    'local' { Start-LocalOnly }
    default { Start-Both }
}
