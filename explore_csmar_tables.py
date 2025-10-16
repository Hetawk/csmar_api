#!/usr/bin/env python3
"""
CSMAR Table Explorer
====================

This script helps you discover what tables and fields are available
in your CSMAR subscription. Use this BEFORE running the main download script
to verify table names and column names.

Usage:
    python3 explore_csmar_tables.py

Author: MSCI DID Analysis
Date: October 16, 2025
"""

import argparse
import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  WARNING: python-dotenv not installed!")

# CSMAR API
try:
    from csmarapi.CsmarService import CsmarService
    from csmarapi.ReportUtil import ReportUtil
except ImportError:
    print("ERROR: CSMAR API not installed!")
    print("\nPlease install CSMAR-PYTHON first:")
    print("1. Download from: https://www.gtarsc.com/")
    print("2. Extract to: [Python Installation]/Lib/site-packages")
    sys.exit(1)

# Configuration
CSMAR_USERNAME = os.getenv("CSMAR_USERNAME", "")
CSMAR_PASSWORD = os.getenv("CSMAR_PASSWORD", "")
LANGUAGE = os.getenv("CSMAR_LANGUAGE", "1")  # 0=Chinese, 1=English


def list_databases(csmar):
    """List all databases"""
    print("\n" + "-"*80)
    print("AVAILABLE DATABASES")
    print("-"*80)
    databases = csmar.getListDbs()
    ReportUtil(databases)
    return databases


def list_tables(csmar, database_name: str):
    """List all tables in a database"""
    print(f"\n{'-'*80}")
    print(f"TABLES IN: {database_name}")
    print("-"*80)
    tables = csmar.getListTables(database_name)
    ReportUtil(tables)
    return tables


def list_fields(csmar, table_name: str):
    """List fields in a table"""
    print(f"\n{'-'*80}")
    print(f"FIELDS IN: {table_name}")
    print("-"*80)
    fields = csmar.getListFields(table_name)
    ReportUtil(fields)
    return fields


def search_tables(csmar, keyword: str):
    """Search table names and descriptions for a keyword"""
    print(f"\n{'-'*80}")
    print(f"SEARCHING FOR: {keyword}")
    print("-"*80)
    print("(Searching across databases and table descriptions)")

    databases = csmar.getListDbs()
    matches = []

    for db_info in databases:
        db_name = db_info.get('Database', db_info.get('数据库', ''))
        if not db_name:
            continue

        try:
            tables = csmar.getListTables(db_name)
            for table_info in tables:
                table_name = table_info.get('Table', table_info.get('表名', ''))
                description = table_info.get(
                    'Description', table_info.get('描述', ''))

                haystacks = [table_name or "", description or ""]
                if any(keyword.lower() in text.lower() for text in haystacks):
                    matches.append({
                        'database': db_name,
                        'table': table_name,
                        'description': description
                    })
        except Exception:
            continue

    if not matches:
        print(f"No tables found matching '{keyword}'")
    else:
        for match in matches:
            print(f"\nFound: {match['table']}")
            print(f"  Database: {match['database']}")
            print(f"  Description: {match['description']}")

    return matches


def interactive_menu(csmar):
    """Interactive CLI menu"""
    while True:
        print("\n" + "="*80)
        print("MENU")
        print("="*80)
        print("1. List all databases")
        print("2. List tables in a database")
        print("3. List fields in a table")
        print("4. Search for table by keyword")
        print("5. Exit")
        print("="*80)

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            try:
                list_databases(csmar)
                print("\nTIP: Look for 'China Listed Firms Research Series' or similar")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            db_name = input("\nEnter database name: ").strip()
            if not db_name:
                print("Database name cannot be empty!")
                continue

            try:
                list_tables(csmar, db_name)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            table_name = input("\nEnter table name: ").strip()
            if not table_name:
                print("Table name cannot be empty!")
                continue

            try:
                list_fields(csmar, table_name)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            keyword = input("\nEnter search keyword: ").strip()
            if not keyword:
                print("Keyword cannot be empty!")
                continue

            try:
                search_tables(csmar, keyword)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("\nExiting...")
            break

        else:
            print("Invalid choice! Please enter 1-5.")


def main():
    """Explore CSMAR tables and fields"""

    parser = argparse.ArgumentParser(
        description="Explore available databases, tables, and fields in your CSMAR subscription"
    )
    parser.add_argument("--list-dbs", action="store_true",
                        help="List all available databases")
    parser.add_argument("--list-tables", metavar="DATABASE",
                        help="List tables in the specified database")
    parser.add_argument("--list-fields", metavar="TABLE",
                        help="List fields for the specified table")
    parser.add_argument("--search", metavar="KEYWORD",
                        help="Search table names and descriptions for a keyword")

    args = parser.parse_args()

    print("\n" + "="*80)
    print("CSMAR TABLE EXPLORER")
    print("="*80)

    # Login
    print("\nLogging in to CSMAR...")
    csmar = CsmarService()

    try:
        csmar.login(CSMAR_USERNAME, CSMAR_PASSWORD, LANGUAGE)
        print("✅ Login successful!\n")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        sys.exit(1)

    # Non-interactive mode
    if args.list_dbs or args.list_tables or args.list_fields or args.search:
        try:
            if args.list_dbs:
                list_databases(csmar)

            if args.list_tables:
                list_tables(csmar, args.list_tables)

            if args.list_fields:
                list_fields(csmar, args.list_fields)

            if args.search:
                search_tables(csmar, args.search)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    # Interactive fallback
    interactive_menu(csmar)


if __name__ == "__main__":
    main()
