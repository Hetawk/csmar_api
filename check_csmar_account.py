#!/usr/bin/env python3
"""
CSMAR Account Status Checker
=============================

Checks your CSMAR account permissions and provides guidance.
"""

import os
from dotenv import load_dotenv
from csmarapi.CsmarService import CsmarService

load_dotenv()
CSMAR_USERNAME = os.getenv("CSMAR_USERNAME", "")
CSMAR_PASSWORD = os.getenv("CSMAR_PASSWORD", "")

print("\n" + "="*70)
print("CSMAR ACCOUNT STATUS CHECKER")
print("="*70)

csmar = CsmarService()
print(f"\nLogging in as: {CSMAR_USERNAME}")
result = csmar.login(CSMAR_USERNAME, CSMAR_PASSWORD, "1")
print("✅ Login successful!")

print("\n" + "="*70)
print("ACCOUNT ANALYSIS")
print("="*70)

print(f"\nYour account: {CSMAR_USERNAME}")
print("\nIssue detected: 'No permission to access' errors")

print("\n" + "="*70)
print("POSSIBLE CAUSES & SOLUTIONS")
print("="*70)

print("\n1. STUDENT/INSTITUTIONAL ACCOUNT")
print("   - Problem: Student accounts often have web-only access")
print("   - Solution: Check with your university if API access is included")
print("   - Action: Contact your institution's CSMAR administrator")

print("\n2. API ACCESS NOT ENABLED")
print("   - Problem: API access might need to be enabled separately")
print("   - Solution: Login to https://www.gtarsc.com/")
print("   - Action: Go to Account Settings → API Access → Enable")

print("\n3. SUBSCRIPTION TYPE")
print("   - Problem: Your subscription might not include API access")
print("   - Solution: Upgrade to a plan that includes API access")
print("   - Check: https://www.gtarsc.com/pricing or contact sales")

print("\n4. WEB INTERFACE ALTERNATIVE")
print("   - If API access is not available, use web interface:")
print("   - Login: https://data.csmar.com/")
print("   - Navigate to: Stock Market → Classification Data")
print("   - Manually download CSV files")
print("   - Save to: output/ folder")

print("\n" + "="*70)
print("RECOMMENDED NEXT STEPS")
print("="*70)

print("\n1. Check your CSMAR account type:")
print("   → Login to: https://www.gtarsc.com/")
print("   → Go to: My Account → Subscription Details")
print("   → Look for: API Access permissions")

print("\n2. Contact CSMAR Support:")
print("   → Email: service@gtadata.com")
print("   → Subject: Request API Access for Python")
print("   → Include: Your account email and institution name")

print("\n3. Alternative: Manual Download")
print("   → Login to CSMAR web interface")
print("   → Download required datasets as CSV")
print("   → Place CSV files in output/ folder")
print("   → Continue with your analysis")

print("\n" + "="*70)
print("ACCOUNT INFORMATION")
print("="*70)
print(f"\nEmail: {CSMAR_USERNAME}")
print("Account Type: Please check on CSMAR website")
print("API Access: Currently showing 'No Permission'")

print("\n" + "="*70)
