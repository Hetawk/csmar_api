#!/usr/bin/env python3
"""
CSMAR API Explorer
==================

This script helps you discover what databases and tables you have access to.
"""

import os
from dotenv import load_dotenv
from csmarapi.CsmarService import CsmarService
from csmarapi.ReportUtil import ReportUtil

# Load credentials
load_dotenv()
CSMAR_USERNAME = os.getenv("CSMAR_USERNAME", "")
CSMAR_PASSWORD = os.getenv("CSMAR_PASSWORD", "")

print("\n" + "="*70)
print("CSMAR API EXPLORER")
print("="*70)

# Login
csmar = CsmarService()
print(f"\nLogging in as: {CSMAR_USERNAME}")
csmar.login(CSMAR_USERNAME, CSMAR_PASSWORD, "1")
print("✅ Login successful!\n")

# List all databases
print("\n" + "="*70)
print("AVAILABLE DATABASES")
print("="*70)
try:
    databases = csmar.getListDbs()
    ReportUtil(databases)
    print("\n")
except Exception as e:
    print(f"Note: {e}")
    print("This might be normal - continuing to check specific databases...")

# Try common database names for Chinese stock market data
print("\n" + "="*70)
print("CHECKING COMMON DATABASE NAMES")
print("="*70)

common_databases = [
    "China Stock Market Series",
    "Stock Market Series",
    "中国股票市场系列研究数据库",
    "StockMarket",
    "CSMAR",
]

for db_name in common_databases:
    print(f"\n{'='*70}")
    print(f"Database: {db_name}")
    print("="*70)
    try:
        tables = csmar.getListTables(db_name)
        if tables:
            print(f"✅ Access granted! Found {len(tables)} tables")
            ReportUtil(tables)

            # Save table names to file
            with open(f"tables_{db_name.replace(' ', '_')}.txt", 'w', encoding='utf-8') as f:
                f.write(f"Database: {db_name}\n")
                f.write(f"Tables ({len(tables)}):\n")
                f.write("="*70 + "\n")
                for table in tables:
                    f.write(f"{table}\n")
            print(
                f"\n✅ Table list saved to: tables_{db_name.replace(' ', '_')}.txt")
        else:
            print("❌ No tables found or no access")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*70)
print("EXPLORATION COMPLETE")
print("="*70)
print("\nNext steps:")
print("1. Check the tables_*.txt files for available tables")
print("2. Look for tables related to:")
print("   - Stock classification")
print("   - Industry classification")
print("   - ST status")
print("   - Area/Province classification")
print("3. Update download_csmar_classifications.py with correct table names")
