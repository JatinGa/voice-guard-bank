#!/usr/bin/env python3
"""
SentinelPay Quick Start - Test Backend Without Frontend
Run this script to test your backend independently
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.END}")

def test_health():
    """Test health check endpoint"""
    print_header("1. Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is running")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:5000")
        print_info("Make sure backend is running: python backend/run.py")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_balance():
    """Test get balance endpoint"""
    print_header("2. Testing Get Balance")
    
    try:
        response = requests.get(f"{BASE_URL}/banking/balance", timeout=5)
        if response.status_code == 200:
            data = response.json()
            balance = data.get('balance', 0)
            currency = data.get('currency', 'INR')
            print_success(f"Balance retrieved: ₹{balance} {currency}")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_liveness():
    """Test voice liveness check"""
    print_header("3. Testing Voice Liveness Check")
    
    payload = {
        "transcript": "green mango",
        "challenge_phrase": "green mango"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/voice/liveness",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            passed = data.get('passed', False)
            score = data.get('score', 0)
            status = "PASSED" if passed else "FAILED"
            print_success(f"Liveness check: {status} (Score: {score}/100)")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_scam_detection():
    """Test scam phrase detection"""
    print_header("4. Testing Scam Detection")
    
    payload = {
        "text": "share your otp immediately"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/risk/scam-check",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            detected = data.get('detected', False)
            phrases = data.get('phrases', [])
            if detected:
                print_success(f"Scam detected: {', '.join(phrases)}")
            else:
                print_info("No scam phrases detected")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_risk_evaluation():
    """Test risk evaluation"""
    print_header("5. Testing Risk Evaluation")
    
    payload = {
        "transcript": "I need to transfer 50000 rupees urgently",
        "amount": 50000,
        "is_liveness_passed": True,
        "stress_level": "high"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/risk/evaluate",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            risk_level = data.get('risk_level', 'UNKNOWN')
            risk_score = data.get('risk_score', 0)
            print_success(f"Risk evaluated: {risk_level} ({risk_score}/100)")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_transactions():
    """Test get transactions"""
    print_header("6. Testing Get Transactions")
    
    try:
        response = requests.get(
            f"{BASE_URL}/banking/transactions?limit=3",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print_success(f"Retrieved {count} transactions")
            
            transactions = data.get('transactions', [])
            for i, txn in enumerate(transactions[:3], 1):
                print(f"  {i}. {txn.get('description')} - ₹{txn.get('amount')}")
            
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_emotion():
    """Test emotion detection"""
    print_header("7. Testing Emotion Detection")
    
    payload = {
        "text": "I'm very worried about my account. Please help me immediately!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/voice/emotion",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            stress_level = data.get('stress_level', 'unknown')
            confidence = data.get('confidence', 0)
            print_success(f"Stress detected: {stress_level.upper()} (Confidence: {confidence:.2f})")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         SentinelPay Backend Testing Script                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    print_info(f"Testing backend at {BASE_URL}")
    print_info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "Health Check": False,
        "Get Balance": False,
        "Voice Liveness": False,
        "Scam Detection": False,
        "Risk Evaluation": False,
        "Get Transactions": False,
        "Emotion Detection": False,
    }
    
    # Run tests
    results["Health Check"] = test_health()
    
    if not results["Health Check"]:
        print_error("\n⚠️  Backend is not running!")
        print_info("Start backend with: python backend/run.py")
        return
    
    time.sleep(0.5)
    results["Get Balance"] = test_balance()
    
    time.sleep(0.5)
    results["Voice Liveness"] = test_liveness()
    
    time.sleep(0.5)
    results["Scam Detection"] = test_scam_detection()
    
    time.sleep(0.5)
    results["Risk Evaluation"] = test_risk_evaluation()
    
    time.sleep(0.5)
    results["Get Transactions"] = test_transactions()
    
    time.sleep(0.5)
    results["Emotion Detection"] = test_emotion()
    
    # Summary
    print_header("Test Results Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print()
    print_success(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed! Backend is working correctly.{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. Check the errors above.{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user.{Colors.END}\n")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
