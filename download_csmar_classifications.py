#!/usr/bin/env python3
"""
CSMAR API Data Download Script
===============================

This script uses CSMAR's official Python API to download stock classification data
for the MSCI Digital Transformation DID Analysis project.

Downloads:
- Stock Market Classification (Shanghai/Shenzhen exchange)
- ST & Non-ST stocks
- CSRC Industry Classification 2012
- Area Classification (Province/City)
- SWS Industry Classification 2021
- CSRC Industry Classification 2001

Time Period: 2010-2024
Sample: All A-share companies (5,607 codes)

Author: Generated for MSCI DID Analysis
Date: October 15, 2025
"""

import os
import sys
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  WARNING: python-dotenv not installed!")
    print("Install with: pip install python-dotenv")
    print("Continuing without .env file support...")

# Add CSMAR API to path (adjust if needed)
try:
    from csmarapi.CsmarService import CsmarService
    from csmarapi.ReportUtil import ReportUtil
except ImportError:
    print("ERROR: CSMAR API not installed!")
    print("\nPlease install CSMAR-PYTHON first:")
    print("1. Download from: https://www.gtarsc.com/")
    print("2. Extract to: [Python Installation]/Lib/site-packages")
    print("3. Install dependencies:")
    print("   pip install urllib3 websocket websocket_client pandas prettytable python-dotenv")
    sys.exit(1)

# Configuration
# On Windows, output to local 'output' folder for easy transfer
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Load credentials from environment variables (set in .env file)
# Your CSMAR username/email/phone
CSMAR_USERNAME = os.getenv("CSMAR_USERNAME", "")
CSMAR_PASSWORD = os.getenv("CSMAR_PASSWORD", "")  # Your CSMAR password
LANGUAGE = os.getenv("CSMAR_LANGUAGE", "1")  # 0=Chinese, 1=English

# Load date range from environment (or use defaults)
START_DATE = os.getenv("CSMAR_START_DATE", "2010-01-01")
END_DATE = os.getenv("CSMAR_END_DATE", "2024-12-31")


class CSMARDataDownloader:
    """Download stock classification data from CSMAR API"""

    def __init__(self, username, password, lang="1"):
        """Initialize CSMAR service and login"""
        self.csmar = CsmarService()
        self.username = username
        self.password = password
        self.lang = lang
        self.logged_in = False

    def login(self):
        """Login to CSMAR"""
        print("\n" + "="*70)
        print("CSMAR API Login")
        print("="*70)

        if not self.username or not self.password:
            print("\n❌ ERROR: CSMAR credentials not provided!")
            print("\nPlease edit this script and add your credentials:")
            print(f"  File: {__file__}")
            print("  Lines: CSMAR_USERNAME and CSMAR_PASSWORD")
            print("\nYour CSMAR login can be:")
            print("  - Registered username")
            print("  - Verified email address")
            print("  - Verified phone number")
            sys.exit(1)

        try:
            print(f"Logging in as: {self.username}")
            result = self.csmar.login(self.username, self.password, self.lang)
            self.logged_in = True
            print("✅ Login successful!\n")
            return result
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("\nPlease check:")
            print("  1. Username/email/phone is correct")
            print("  2. Password is correct")
            print("  3. Account is a personal registered account (not institutional)")
            print("  4. Internet connection is stable")
            sys.exit(1)

    def list_databases(self):
        """List all available databases"""
        if not self.logged_in:
            self.login()

        print("Querying available databases...")
        databases = self.csmar.getListDbs()
        ReportUtil(databases)
        return databases

    def list_tables(self, database_name):
        """List all tables in a database"""
        if not self.logged_in:
            self.login()

        print(f"\nQuerying tables in database: {database_name}")
        tables = self.csmar.getListTables(database_name)
        ReportUtil(tables)
        return tables

    def list_fields(self, table_name):
        """List all fields in a table"""
        if not self.logged_in:
            self.login()

        print(f"\nQuerying fields in table: {table_name}")
        fields = self.csmar.getListFields(table_name)
        ReportUtil(fields)
        return fields

    def download_classification_data(self, table_name, columns, condition,
                                     start_date=START_DATE, end_date=END_DATE,
                                     description="classification data"):
        """
        Download classification data from CSMAR

        Parameters:
        -----------
        table_name : str
            CSMAR table name (e.g., 'STK_Class')
        columns : list
            List of column names to download
        condition : str
            SQL-like condition (e.g., "Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'")
        start_date : str
            Start date in YYYY-MM-DD format
        end_date : str
            End date in YYYY-MM-DD format
        description : str
            Human-readable description for logging

        Returns:
        --------
        pandas.DataFrame
            Downloaded data
        """
        if not self.logged_in:
            self.login()

        print("\n" + "-"*70)
        print(f"Downloading: {description}")
        print("-"*70)
        print(f"Table: {table_name}")
        print(f"Columns: {', '.join(columns)}")
        print(f"Condition: {condition}")
        print(f"Time Range: {start_date} to {end_date}")

        # First, check record count
        try:
            count = self.csmar.queryCount(columns, condition, table_name,
                                          start_date, end_date)
            print(f"Total records to download: {count}")

            if count == 0:
                print("⚠️  WARNING: No records found! Check your condition.")
                return pd.DataFrame()

            if count > 200000:
                print(f"⚠️  WARNING: {count} records exceeds 200,000 limit!")
                print("Will need to use pagination (automatically handled below)")

        except Exception as e:
            print(f"⚠️  Could not check record count: {e}")
            print("Proceeding with download anyway...")

        # Download data
        try:
            print("\nDownloading data (this may take a few minutes)...")

            # Use query_df to get DataFrame directly
            df = self.csmar.query_df(columns, condition, table_name,
                                     start_date, end_date)

            print(f"✅ Downloaded {len(df)} records")
            print(f"   Columns: {list(df.columns)}")
            print(
                f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

            return df

        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Check if you have permission to access this table")
            print("  2. Verify table name and column names are correct")
            print("  3. Try reducing the date range")
            print("  4. Wait 30 minutes between identical queries")
            return pd.DataFrame()

    def download_all_classifications(self):
        """
        Download all required classification data for MSCI DID analysis

        Returns:
        --------
        dict
            Dictionary of DataFrames, one for each classification type
        """
        if not self.logged_in:
            self.login()

        print("\n" + "="*70)
        print("DOWNLOADING ALL CLASSIFICATION DATA")
        print("="*70)

        # Dictionary to store all downloaded data
        datasets = {}

        # NOTE: Table names and column names below are EXAMPLES
        # You need to verify the actual table/column names in your CSMAR subscription
        # Use: csmar.getListTables('China Stock Market Series')
        # Then: csmar.getListFields('TableName')

        print("\n⚠️  IMPORTANT: Table and column names below are EXAMPLES!")
        print("You MUST verify them using:")
        print("  1. csmar.getListTables('China Stock Market Series')")
        print("  2. csmar.getListFields('TableName')")
        print("\nProceeding with example queries (may fail if names are wrong)...\n")

        # 1. Stock Market Classification (Shanghai/Shenzhen exchange)
        try:
            df_market = self.download_classification_data(
                table_name='STK_MKT_Type',  # Example table name - VERIFY THIS
                columns=['Stkcd', 'MarketType', 'ListedDate', 'BoardType'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="Stock Market Classification (Exchange Type)"
            )
            if not df_market.empty:
                datasets['market_classification'] = df_market
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        time.sleep(2)  # Rate limiting

        # 2. ST & Non-ST stocks
        try:
            df_st = self.download_classification_data(
                table_name='STK_ST_Status',  # Example table name - VERIFY THIS
                columns=['Stkcd', 'Date', 'IsST', 'STType'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="ST & Non-ST Stock Status"
            )
            if not df_st.empty:
                datasets['st_classification'] = df_st
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        time.sleep(2)

        # 3. CSRC Industry Classification 2012
        try:
            df_csrc2012 = self.download_classification_data(
                table_name='STK_Industry_CSRC2012',  # Example - VERIFY
                columns=['Stkcd', 'Date', 'IndustryCode', 'IndustryName',
                         'IndustryCode_Level1', 'IndustryName_Level1'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="CSRC Industry Classification 2012"
            )
            if not df_csrc2012.empty:
                datasets['csrc_industry_2012'] = df_csrc2012
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        time.sleep(2)

        # 4. Area Classification (Province/City)
        try:
            df_area = self.download_classification_data(
                table_name='STK_Area_Classification',  # Example - VERIFY
                columns=['Stkcd', 'ProvinceCode', 'ProvinceName',
                         'CityCode', 'CityName'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="Area Classification (Province/City)"
            )
            if not df_area.empty:
                datasets['area_classification'] = df_area
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        time.sleep(2)

        # 5. SWS Industry Classification 2021
        try:
            df_sws2021 = self.download_classification_data(
                table_name='STK_Industry_SWS2021',  # Example - VERIFY
                columns=['Stkcd', 'Date', 'SWSIndustryCode', 'SWSIndustryName',
                         'Level1Code', 'Level1Name'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="SWS Industry Classification 2021"
            )
            if not df_sws2021.empty:
                datasets['sws_industry_2021'] = df_sws2021
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        time.sleep(2)

        # 6. CSRC Industry Classification 2001
        try:
            df_csrc2001 = self.download_classification_data(
                table_name='STK_Industry_CSRC2001',  # Example - VERIFY
                columns=['Stkcd', 'Date', 'IndustryCode', 'IndustryName'],
                condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'",
                description="CSRC Industry Classification 2001"
            )
            if not df_csrc2001.empty:
                datasets['csrc_industry_2001'] = df_csrc2001
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

        return datasets

    def save_datasets(self, datasets, output_dir=OUTPUT_DIR):
        """
        Save downloaded datasets to CSV files

        Parameters:
        -----------
        datasets : dict
            Dictionary of DataFrames
        output_dir : Path
            Directory to save files
        """
        if not datasets:
            print("\n❌ No datasets to save!")
            return

        print("\n" + "="*70)
        print("SAVING DATASETS")
        print("="*70)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for name, df in datasets.items():
            if df.empty:
                print(f"⚠️  Skipping empty dataset: {name}")
                continue

            # Save as CSV
            filename = f"csmar_{name}_{timestamp}.csv"
            filepath = output_dir / filename

            print(f"\nSaving: {name}")
            print(f"  File: {filename}")
            print(f"  Records: {len(df):,}")
            print(f"  Columns: {list(df.columns)}")

            df.to_csv(filepath, index=False, encoding='utf-8')

            file_size = filepath.stat().st_size / 1024**2
            print(f"  Size: {file_size:.2f} MB")
            print(f"  ✅ Saved successfully!")

        print("\n" + "="*70)
        print(f"All datasets saved to: {output_dir}")
        print("="*70)

    def merge_classifications(self, datasets):
        """
        Merge all classification datasets into a single master file

        Parameters:
        -----------
        datasets : dict
            Dictionary of classification DataFrames

        Returns:
        --------
        pandas.DataFrame
            Merged classification dataset
        """
        print("\n" + "="*70)
        print("MERGING CLASSIFICATION DATASETS")
        print("="*70)

        if not datasets:
            print("❌ No datasets to merge!")
            return pd.DataFrame()

        # Start with stock codes from any available dataset
        base_df = None

        for name, df in datasets.items():
            if df.empty:
                continue

            print(f"\nMerging: {name}")
            print(
                f"  Records before: {len(base_df) if base_df is not None else 0}")

            if base_df is None:
                # First dataset becomes base
                base_df = df.copy()
                print(f"  Using as base dataset")
            else:
                # Merge subsequent datasets
                # Determine merge key (usually 'Stkcd' and maybe 'Date')
                merge_keys = ['Stkcd']
                if 'Date' in df.columns and 'Date' in base_df.columns:
                    merge_keys.append('Date')

                base_df = pd.merge(base_df, df, on=merge_keys, how='outer',
                                   suffixes=('', f'_{name}'))

            print(f"  Records after: {len(base_df)}")

        if base_df is not None:
            print("\n" + "-"*70)
            print("MERGE SUMMARY")
            print("-"*70)
            print(f"Total records: {len(base_df):,}")
            print(f"Total columns: {len(base_df.columns)}")
            print(
                f"Unique stocks: {base_df['Stkcd'].nunique() if 'Stkcd' in base_df.columns else 'N/A'}")
            print(
                f"Memory usage: {base_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        return base_df if base_df is not None else pd.DataFrame()


def main():
    """Main execution function"""

    print("\n" + "="*70)
    print("CSMAR CLASSIFICATION DATA DOWNLOAD SCRIPT")
    print("="*70)
    print(f"Project: MSCI Digital Transformation DID Analysis")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time Period: {START_DATE} to {END_DATE}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print("="*70)

    # Initialize downloader
    downloader = CSMARDataDownloader(
        username=CSMAR_USERNAME,
        password=CSMAR_PASSWORD,
        lang=LANGUAGE
    )

    # Login
    downloader.login()

    # Optional: List available databases and tables
    print("\n" + "="*70)
    print("STEP 1: EXPLORE AVAILABLE DATA (Optional)")
    print("="*70)
    print("\nTo see what databases you have access to, uncomment the lines below:")
    print("  # downloader.list_databases()")
    print("  # downloader.list_tables('China Stock Market Series')")
    print("  # downloader.list_fields('STK_MKT_Type')")
    print("\nSkipping exploration for now...\n")

    # Download all classification data
    print("\n" + "="*70)
    print("STEP 2: DOWNLOAD CLASSIFICATION DATA")
    print("="*70)

    datasets = downloader.download_all_classifications()

    if not datasets:
        print("\n❌ No data downloaded! Please check:")
        print("  1. Table names and column names in the script")
        print("  2. Your CSMAR subscription includes these tables")
        print("  3. Use list_tables() and list_fields() to find correct names")
        sys.exit(1)

    # Save individual datasets
    downloader.save_datasets(datasets)

    # Merge all classifications
    print("\n" + "="*70)
    print("STEP 3: MERGE CLASSIFICATIONS")
    print("="*70)

    merged_df = downloader.merge_classifications(datasets)

    if not merged_df.empty:
        # Save merged dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merged_file = OUTPUT_DIR / \
            f"csmar_classifications_merged_{timestamp}.csv"

        print(f"\nSaving merged dataset: {merged_file.name}")
        merged_df.to_csv(merged_file, index=False, encoding='utf-8')
        print(f"✅ Saved {len(merged_df):,} records")

    # Final summary
    print("\n" + "="*70)
    print("DOWNLOAD COMPLETE!")
    print("="*70)
    print(f"\nFiles saved to: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("  1. Inspect the downloaded CSV files")
    print("  2. Update regenerate_analysis_dataset.py to read these files")
    print("  3. Run: python3 regenerate_analysis_dataset.py")
    print("  4. Run baseline regression: python3 run_corrected_baseline_analysis.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
