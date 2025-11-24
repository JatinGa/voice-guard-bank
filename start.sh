#!/bin/bash
# Quick startup script for SentinelPay (macOS/Linux)

set -e

MODE="${1:-both}"
BOLD='\033[1m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

show_help() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║         SentinelPay Quick Start Script                         ║
╚════════════════════════════════════════════════════════════════╝

USAGE:
    ./start.sh [MODE]

MODES:
    both        Start both frontend and backend (default)
    frontend    Start frontend only (local mock mode)
    backend     Start backend only (for external frontend)
    local       Run frontend in local mock mode

EXAMPLES:
    ./start.sh                 # Start both frontend and backend
    ./start.sh frontend        # Start only frontend
    ./start.sh backend         # Start only backend
    ./start.sh local           # Local-only development

REQUIREMENTS:
    - Node.js 18+ (for frontend)
    - Python 3.8+ (for backend)
    - npm or bun

QUICKSTART (First Time):
    1. ./start.sh backend      # Terminal 1
    2. ./start.sh frontend     # Terminal 2
    3. Open http://localhost:8080

EOF
}

init_backend() {
    echo -e "${CYAN}📦 Initializing backend...${NC}\n"
    
    if [ ! -d "backend" ]; then
        echo -e "${RED}Error: 'backend' directory not found.${NC}"
        exit 1
    fi
    
    # Create venv if not exists
    if [ ! -d "backend/venv" ]; then
        echo -e "${YELLOW}Creating Python virtual environment...${NC}"
        python3 -m venv backend/venv
    fi
    
    # Activate venv
    source backend/venv/bin/activate
    
    # Install requirements
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -q -r backend/requirements.txt 2>/dev/null
    
    # Check .env
    if [ ! -f "backend/.env" ]; then
        echo -e "${YELLOW}⚠️  backend/.env not found!${NC}"
        cp backend/.env.example backend/.env
        echo -e "${RED}❌ Please edit backend/.env with your Supabase credentials${NC}"
        echo -e "${CYAN}Then run again: ./start.sh backend${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Backend ready${NC}"
}

init_frontend() {
    echo -e "${CYAN}📦 Initializing frontend...${NC}\n"
    
    if [ ! -f "package.json" ]; then
        echo -e "${RED}Error: 'package.json' not found.${NC}"
        exit 1
    fi
    
    # Install deps
    echo -e "${YELLOW}Installing Node dependencies...${NC}"
    npm install -q 2>/dev/null
    
    # Create .env.local if missing
    if [ ! -f ".env.local" ]; then
        echo -e "${YELLOW}Creating .env.local...${NC}"
        cat > .env.local << 'ENV'
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:5000/api
VITE_USE_BACKEND=true
VITE_USE_ML=false
ENV
        echo -e "${GREEN}✓ Created .env.local${NC}"
    fi
    
    echo -e "${GREEN}✓ Frontend ready${NC}"
}

start_backend() {
    init_backend
    echo -e "${CYAN}🚀 Starting backend on port 5000...${NC}"
    echo -e "${YELLOW}Press CTRL+C to stop${NC}\n"
    source backend/venv/bin/activate
    python backend/run.py
}

start_frontend() {
    init_frontend
    echo -e "${CYAN}🚀 Starting frontend on port 8080...${NC}"
    echo -e "${YELLOW}Press CTRL+C to stop${NC}\n"
    npm run dev
}

start_both() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║    SentinelPay - Starting Frontend + Backend                  ║
╚════════════════════════════════════════════════════════════════╝
EOF
    
    init_frontend
    init_backend
    
    echo -e "${YELLOW}⚠️  For two-terminal setup:${NC}"
    echo -e "  Terminal 1: ./start.sh backend"
    echo -e "  Terminal 2: ./start.sh frontend"
    echo ""
    echo -e "${CYAN}Starting frontend in 3 seconds...${NC}"
    sleep 3
    
    start_frontend
}

start_local() {
    init_frontend
    
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║    SentinelPay - Local Mode (No Backend Required)            ║
╚════════════════════════════════════════════════════════════════╝

✓ All features available locally
✓ Voice processing using Web Speech API
✓ Mock banking with hardcoded fallback

Note: For real ML models, run: ./start.sh backend
EOF
    
    echo -e "\n${CYAN}🚀 Starting frontend on port 8080...${NC}"
    echo -e "${YELLOW}Press CTRL+C to stop${NC}\n"
    npm run dev
}

# Main
case "$MODE" in
    -h|--help|help)
        show_help
        exit 0
        ;;
    both)
        start_both
        ;;
    frontend)
        start_frontend
        ;;
    backend)
        start_backend
        ;;
    local)
        start_local
        ;;
    *)
        start_both
        ;;
esac
