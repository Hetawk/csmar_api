#!/usr/bin/env python3
"""
CSMAR API Test Script
======================

Quick test to verify CSMAR API is installed and working.
Run this before using the full download script.

Usage:
    python3 test_csmar_api.py
"""

import sys
import os

# Try to load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    dotenv_available = True
except ImportError:
    dotenv_available = False

print("\n" + "="*70)
print("CSMAR API Installation Test")
print("="*70 + "\n")

# Test 1: Check if CSMAR API is installed
print("Test 1: Checking if CSMAR API is installed...")
try:
    from csmarapi.CsmarService import CsmarService
    from csmarapi.ReportUtil import ReportUtil
    print("✅ CSMAR API modules found!\n")
except ImportError as e:
    print(f"❌ CSMAR API not installed: {e}\n")
    print("Please install CSMAR-PYTHON:")
    print("  1. Download from: https://www.gtarsc.com/")
    print("  2. Extract to: [Python]/Lib/site-packages/")
    print("  3. Verify folder structure: csmarapi/CsmarService.py exists")
    sys.exit(1)

# Test 2: Check required dependencies
print("Test 2: Checking required dependencies...")
required_packages = ['urllib3', 'websocket', 'pandas', 'prettytable']
missing = []

for package in required_packages:
    try:
        __import__(package)
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package} - NOT INSTALLED")
        missing.append(package)

if missing:
    print(f"\n❌ Missing packages: {', '.join(missing)}")
    print(f"\nInstall them with:")
    print(f"  pip install {' '.join(missing)}")
    sys.exit(1)

print("\n✅ All dependencies installed!\n")

# Test 3: Try creating CSMAR service instance
print("Test 3: Creating CSMAR service instance...")
try:
    csmar = CsmarService()
    print("✅ CsmarService instance created!\n")
except Exception as e:
    print(f"❌ Failed to create service: {e}\n")
    sys.exit(1)

# Test 4: Prompt for login test (optional)
print("="*70)
print("Login Test (Optional)")
print("="*70 + "\n")

# Check if credentials are in .env
username_from_env = os.getenv("CSMAR_USERNAME", "")
password_from_env = os.getenv("CSMAR_PASSWORD", "")

if username_from_env and password_from_env:
    print(f"✅ Found credentials in .env file")
    print(f"Username: {username_from_env}")
    test_login = input(
        "Test login with these credentials? (y/n): ").strip().lower()

    if test_login == 'y':
        username = username_from_env
        password = password_from_env
    else:
        test_login = 'n'
else:
    if dotenv_available:
        print("⚠️  No credentials found in .env file")
        print("You can create a .env file with:")
        print("  CSMAR_USERNAME=your_username")
        print("  CSMAR_PASSWORD=your_password")
    else:
        print("⚠️  python-dotenv not installed (.env file not supported)")
        print("Install with: pip install python-dotenv")

    print()
    test_login = input(
        "Do you want to test login manually? (y/n): ").strip().lower()

if test_login == 'y':
    # If not from env, ask user to input
    if not (username_from_env and password_from_env):
        username = input("Enter CSMAR username/email/phone: ").strip()

        # Don't echo password
        import getpass
        password = getpass.getpass("Enter CSMAR password: ")

    print("\nAttempting login...")
    try:
        result = csmar.login(username, password, "1")  # 1 = English
        print("✅ Login successful!")
        print("\nYour CSMAR account is working!")
        print("You can now run the full download script.")

        # Optional: List available databases
        print("\n" + "-"*70)
        print("Available Databases")
        print("-"*70)
        databases = csmar.getListDbs()
        ReportUtil(databases)

    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("\nPlease check:")
        print("  1. Username/email/phone is correct")
        print("  2. Password is correct")
        print("  3. Account is a personal registered account")
        print("  4. Internet connection is working")
        sys.exit(1)
else:
    print("\nSkipping login test.")
    print("You can test login later when running the download script.")

# Final summary
print("\n" + "="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\nYour system is ready to download CSMAR data.")
print("\nNext steps:")
print("  1. Edit: src/python/data_acquisition/download_csmar_classifications.py")
print("  2. Add your CSMAR credentials (lines 44-46)")
print("  3. Run: python3 src/python/data_acquisition/download_csmar_classifications.py")
print("\n" + "="*70 + "\n")
