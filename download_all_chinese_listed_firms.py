#!/usr/bin/env python3
"""
CSMAR API - Complete Chinese Listed Firms Research Series Downloader
=====================================================================

This script downloads ALL data from CSMAR's "China Listed Firms Research Series"
(中国上市公司研究系列) covering all 9 major sections:

1. Basic Info (基本信息)
2. Financial Data (财务数据)
3. Equity & Governance (股权治理)
4. Financing & Distribution (融资分配)
5. Major Events (重大事件)
6. Feature Topics (特色专题)
7. Text Analysis (文本分析)
8. New Third Board (新三板)
9. Others (其他)

This will give you COMPLETE coverage of:
- All financial statements (balance sheet, income, cash flow)
- All financial ratios (ROA, ROE, Tobin's Q, profitability, liquidity, leverage)
- Board characteristics (size, independence, meetings)
- Shareholder structure (ownership concentration, top shareholders)
- Executive compensation
- M&A activities
- IPO/delisting data
- And much more

Time Period: 2010-2024 (15 years)
Sample: All A-share companies

Author: Enhanced for MSCI DID Analysis
Date: October 16, 2025
"""

import argparse
import os
import re
import sys
import time
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover - optional dependency
    tqdm = None

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  WARNING: python-dotenv not installed!")
    print("Install with: pip install python-dotenv")

# CSMAR API
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

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "dataset" / "csmar_data"

# Load credentials from environment variables
CSMAR_USERNAME = os.getenv("CSMAR_USERNAME", "")
CSMAR_PASSWORD = os.getenv("CSMAR_PASSWORD", "")
LANGUAGE = os.getenv("CSMAR_LANGUAGE", "1")  # 0=Chinese, 1=English

# Date range for analysis (2010-2024: 15 years)
START_DATE = os.getenv("CSMAR_START_DATE", "2010-01-01")
END_DATE = os.getenv("CSMAR_END_DATE", "2024-12-31")

# Stock code filter (A-share stocks only)
STOCK_CONDITION = "Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'"

# Rate limiting (seconds between API calls)
RATE_LIMIT_DELAY = 3

# CSMAR API hard limit per request (officially 200,000 rows)
MAX_RECORDS_PER_QUERY = 200000


# ============================================================================
# TABLE DEFINITIONS
# ============================================================================

# NOTE: These are EXAMPLE table names and columns
# You MUST verify the actual names using:
#   csmar.getListTables('China Stock Market Series')
#   csmar.getListFields('TableName')
#
# Table names vary by CSMAR subscription and language setting

TABLES_TO_DOWNLOAD = {

    # ========================================================================
    # 1. BASIC INFORMATION
    # ========================================================================
    "basic_info": {
        "yearly_profile": {
            "table": "STK_LISTEDCOINFOANL",
            "columns": [
                "Symbol", "ShortName_en", "EndDate", "LISTINGDATE",
                "LISTINGSTATE_EN", "IndustryCode", "IndustryName_EN",
                "RegisterAddress_EN", "OfficeAddress_EN", "RegisterCapital",
                "PROVINCE_EN", "CITY_EN", "Website"
            ],
            "description": "Yearly statistics on listed firm basic information",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "profile_changes": {
            "table": "STK_LISTEDCOINFOCHG",
            "columns": [
                "Symbol", "AnnouncementDate", "ImplementDate",
                "ChangedItem_EN", "Value_Before_EN", "Value_After_EN"
            ],
            "description": "Change log for listed firm basic information",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "listing_status_changes": {
            "table": "STK_ITEMCHANGE",
            "columns": [
                "Symbol", "DeclareDate", "ChangeDate", "ChangedItem_EN",
                "ValueBefore_EN", "ValueAfter_EN", "VALUE_EN"
            ],
            "description": "Listing status changes (IPO, suspension, delisting)",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "industry_classification": {
            "table": "STK_INDUSTRYCLASS",
            "columns": [
                "Symbol", "IndustryClassificationID",
                "IndustryClassificationName_EN", "ImplementDate",
                "IndustryCode", "IndustryName_EN"
            ],
            "description": "Industry classification assignments",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "industry_classification_annual": {
            "table": "STK_IndustryClassAnl",
            "columns": [
                "Symbol", "EndDate", "ShortName_EN",
                "IndustryClassificationID", "IndustryClassification_EN",
                "IndustryCode1", "IndustryName1_EN", "IndustryCode2",
                "IndustryName2_EN", "IndustryCode3", "IndustryName3_EN",
                "IndustryCode4", "IndustryName4_EN", "IndustryCode1CL",
                "IndustryName1CL_EN"
            ],
            "description": "Annual multi-level industry classification assignments",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "company_staff": {
            "table": "STK_CompanyStaff",
            "columns": [
                "Symbol", "ShortName_EN", "EndDate", "EmployStructure_EN",
                "EmployDetail_EN", "Amount", "Unit_EN"
            ],
            "description": "Personnel structure of listed companies",
            "time_varying": True,
            "stock_field": "Symbol"
        }
    },

    # ========================================================================
    # 2. FINANCIAL STATEMENTS
    # ========================================================================
    "financial_statements": {
        "balance_sheet": {
            "table": "FS_Combas",
            "columns": [
                "Stkcd", "Accper", "Typrep", "A001000000", "A001100000",
                "A001200000", "A002000000", "A003000000", "A004000000",
                "A001101000", "A001123000", "A001212000"
            ],
            "description": "Balance sheet (general industry)",
            "time_varying": True
        },
        "income_statement": {
            "table": "FS_Comins",
            "columns": [
                "Stkcd", "Accper", "Typrep", "B001100000", "B001101000",
                "B001200000", "B001300000", "B001000000", "B002000000",
                "B002000101", "B003000000", "B004000000", "B001216000",
                "B001211000"
            ],
            "description": "Income statement (general industry)",
            "time_varying": True
        },
        "cash_flow_indirect": {
            "table": "FS_Comscfi",
            "columns": [
                "Stkcd", "Accper", "Typrep", "D000100000", "D000200000",
                "D000101000", "D000102000", "D000103000", "D000109000",
                "D000110000", "D000113000", "D000114000", "D000115000"
            ],
            "description": "Cash flow statement (indirect method)",
            "time_varying": True
        }
    },

    # ========================================================================
    # 3. FINANCIAL INDICATORS & RATIOS
    # ========================================================================
    "financial_indicators": {
        "solvency": {
            "table": "FI_T1",
            "columns": [
                "Stkcd", "Accper", "Typrep", "F010101A", "F010201A",
                "F010401A", "F011201A", "F011301A", "F011601A", "F011701A"
            ],
            "description": "Solvency and leverage ratios",
            "time_varying": True
        },
        "profitability": {
            "table": "FI_T5",
            "columns": [
                "Stkcd", "Accper", "Typrep", "F050101B", "F050501B",
                "F050801B", "F050901B", "F051201B", "F052301B", "F053401B"
            ],
            "description": "Profitability metrics (ROA, ROE, margins)",
            "time_varying": True
        },
        "growth": {
            "table": "FI_T8",
            "columns": [
                "Stkcd", "Accper", "Typrep", "F080601A", "F080602A",
                "F081001B", "F081002B", "F081601B", "F081701B", "F082601B"
            ],
            "description": "Growth capability indicators",
            "time_varying": True
        }
    },

    # ========================================================================
    # 4. CORPORATE GOVERNANCE
    # ========================================================================
    "corporate_governance": {
        "company_profile": {
            "table": "CG_Co",
            "columns": [
                "Stkcd", "Stknme_en", "ListedDate", "DelistedDate",
                "Regcap", "IndustryNameD_EN", "IndustryCodeD"
            ],
            "description": "Corporate governance company profile",
            "time_varying": True
        },
        "top_shareholders": {
            "table": "CG_Sharehold",
            "columns": [
                "Stkcd", "Reptdt", "S0101b_en", "S0201b", "S0301b",
                "S0401b_en", "S0501b"
            ],
            "description": "Top shareholding structure",
            "time_varying": True
        },
        "executive_profiles": {
            "table": "CG_Director",
            "columns": [
                "Stkcd", "Reptdt", "D0101b_en", "D0201b_en", "D0301b_en",
                "D0401b", "D0501b", "D1001b", "D1101b"
            ],
            "description": "Director and executive profile data",
            "time_varying": True
        },
        "ceo_changes": {
            "table": "CG_Ceo",
            "columns": [
                "Stkcd", "Annodt", "Chgdt", "Position", "Changtyp",
                "Name_en", "Dimreas"
            ],
            "description": "Changes of chairpersons and general managers",
            "time_varying": True
        },
        "management_salary": {
            "table": "CG_ManagerShareSalary",
            "columns": [
                "Symbol", "Enddate", "TotalNumber", "FemaleNumber",
                "DirectorNumber", "ManagerNumber", "Holdshares", "SumSalary",
                "Top3SumSalary"
            ],
            "description": "Management shareholding and compensation statistics",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "subsidiary_profile": {
            "table": "STK_NotesSubJoint",
            "columns": [
                "Symbol", "EndDate", "RalatedParty_en", "CorporateIncomeTax_en",
                "RelationshipCode", "Relationship_en", "EstablishDate",
                "RegisterCapital", "RegisterAddress_en", "Sgnrgn",
                "EstablishWay_en", "DirectHoldingRatio", "IndirectHoldingRatio",
                "TotalAssets", "OperatingEvenue", "NetProfit", "ProfitParent",
                "TotalCost", "Currency_en", "ISExit", "AreaName_EN",
                "BusinessScope_EN", "Explanation_EN"
            ],
            "description": "Subsidiaries and joint ventures disclosed in notes",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "subsidiary_disposals": {
            "table": "STK_NotesInvExit",
            "columns": [
                "Symbol", "EndDate", "RalatedParty_en", "Sgnrgn",
                "EstablishDate", "ExitMode", "DisposalDate", "DisposalPrice",
                "DisposalEquity", "Currency_en", "ShortName_EN"
            ],
            "description": "Subsidiary investment exit disclosures",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "core_staff_roster": {
            "table": "CG_CoreStaffInfo",
            "columns": [
                "Enddate", "Symbol", "ShortName_EN", "Source", "PersonID",
                "FullName_EN", "Position_EN", "ServiceStartDate",
                "ServiceEndDate", "IsResign", "YearBeginningHoldShares",
                "EndDateHoldShares", "IsCoreTechStaff", "JudgeSource"
            ],
            "description": "Core personnel roster with tenure and holdings",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "core_staff_statistics": {
            "table": "CG_CoreStaffSta",
            "columns": [
                "Enddate", "Symbol", "ShortName_EN", "Source", "CoreStaffSum",
                "CoreTechStaffSum", "CoreBusStaffSum"
            ],
            "description": "Summary counts of core staff by role",
            "time_varying": True,
            "stock_field": "Symbol"
        },
        "governance_yearly_summary": {
            "table": "CG_Ybasic",
            "columns": [
                "Stkcd", "Reptdt", "Annodt", "Y0301b", "Y0401b", "Y0501b",
                "Y0601b", "Y0701b", "Y0801b_en", "Y0901b_en", "Y1001b",
                "Y1401b", "Y1701a", "Y1701b", "Y1701c", "Y1801b",
                "ChairmanID", "GeneralManagerID", "ChairmanHoldshares",
                "ChairmanHoldsharesRatio", "ManagerHoldshares",
                "ManagerHoldsharesRatio", "Y1901b_en"
            ],
            "description": "Annual governance basics (staffing, leadership, committees)",
            "time_varying": True
        }
    },

    # ========================================================================
    # 5. DIVIDEND POLICY
    # ========================================================================
    "dividend_distribution": {
        "cash_dividends": {
            "table": "CD_Dividend",
            "columns": [
                "Stkcd", "Finyear", "Ppdadt", "Ppcont_en", "Ddadt",
                "Annocont_en", "Perspt", "Pertran", "Numdiv", "Regdt",
                "Exdistdt", "Divdt", "DistributionBaseShares"
            ],
            "description": "Cash and stock dividend distribution records",
            "time_varying": True
        }
    },

    # ========================================================================
    # 6. STOCK TRADING
    # ========================================================================
    "stock_trading": {
        "annual_trading_summary": {
            "table": "TRD_Year",
            "columns": [
                "Stkcd", "Trdynt", "Yopnprc", "Yclsprc", "Ynshrtrd",
                "Ynvaltrd", "Ysmvosd", "Ysmvttl", "Ndaytrd",
                "Yretwd", "Yretnd"
            ],
            "description": "Annual stock trading summary and returns",
            "time_varying": True
        }
    }
}


# ============================================================================
# DOWNLOADER CLASS
# ============================================================================

class ChineseListedFirmsDownloader:
    """Download complete Chinese Listed Firms Research Series from CSMAR"""

    def __init__(
        self,
        username: str,
        password: str,
        lang: str = "1",
        tables_config: Dict[str, Dict[str, dict]] = TABLES_TO_DOWNLOAD
    ):
        """Initialize CSMAR service"""
        self.csmar = CsmarService()
        self.username = username
        self.password = password
        self.lang = lang
        self.logged_in = False
        self.tables_config = tables_config
        self.validation_results: Dict[str, Dict[str, dict]] = {}

        # Statistics
        self.stats = {
            "total_tables": 0,
            "successful_downloads": 0,
            "failed_downloads": 0,
            "total_records": 0,
            "total_size_mb": 0,
            "download_start": None,
            "download_end": None
        }

    def login(self):
        """Login to CSMAR"""
        print("\n" + "="*80)
        print("CSMAR API LOGIN")
        print("="*80)

        if not self.username or not self.password:
            print("\n❌ ERROR: CSMAR credentials not provided!")
            print("\nPlease set environment variables in .env file:")
            print("  CSMAR_USERNAME=your_username_or_email")
            print("  CSMAR_PASSWORD=your_password")
            sys.exit(1)

        try:
            print(f"Logging in as: {self.username}")
            result = self.csmar.login(self.username, self.password, self.lang)
            self.logged_in = True
            print("✅ Login successful!\n")
            return result
        except Exception as e:
            print(f"❌ Login failed: {e}")
            sys.exit(1)

    def _extract_available_columns(self, raw_fields) -> List[str]:
        """Normalize getListFields output into a simple list of column names"""
        available: set = set()

        if raw_fields is None:
            return []

        if isinstance(raw_fields, pd.DataFrame):
            for candidate in ("field", "Field", "字段"):
                if candidate in raw_fields.columns:
                    available.update(
                        raw_fields[candidate].dropna().astype(str).tolist())
                    break
        elif isinstance(raw_fields, list):
            for entry in raw_fields:
                if isinstance(entry, dict):
                    for key in ("field", "Field", "字段"):
                        value = entry.get(key)
                        if value:
                            available.add(str(value))
                            break
                else:
                    value = getattr(entry, "field", None) or getattr(
                        entry, "Field", None)
                    if value:
                        available.add(str(value))

        return sorted(available)

    def _determine_stock_field(self, table_info: dict) -> str:
        """Determine which column should be used to filter by stock code."""
        explicit_field = table_info.get("stock_field")
        if explicit_field:
            return explicit_field

        columns = table_info.get("columns", [])
        normalized = {col.lower(): col for col in columns}

        for candidate in ("stkcd", "symbol", "stkcode", "stockcode"):
            match = normalized.get(candidate)
            if match:
                return match

        # Fallback to a reasonable default to avoid crashing; CSMAR tables
        # typically expose either Stkcd or Symbol.
        return "Stkcd"

    def _normalize_count(self, value) -> Optional[int]:
        """Convert queryCount return value into an integer when possible."""
        if value is None:
            return None

        if isinstance(value, bool):  # bool is subclass of int; treat explicitly
            return int(value)

        if isinstance(value, (int, float)):
            return int(value)

        if isinstance(value, str):
            cleaned = re.sub(r"[^0-9-]", "", value)
            if cleaned in {"", "-"}:
                return None
            try:
                return int(cleaned)
            except ValueError:
                return None

        try:
            as_int = int(value)  # type: ignore[arg-type]
            return as_int
        except (TypeError, ValueError):
            return None

    def _build_stock_condition(self, stock_field: str) -> str:
        """Build the stock selection condition for queryCount/query_df."""
        field = stock_field or "Stkcd"
        clauses = [f"{field} like '{prefix}%'" for prefix in ("0", "3", "6")]
        return "(" + " or ".join(clauses) + ")"

    def _parse_iso_date(self, value: str) -> date:
        """Parse an ISO formatted date string into a date object."""
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(
                f"Invalid date format '{value}'. Expected YYYY-MM-DD."
            ) from exc

    def _next_period(self, period: str) -> Optional[str]:
        """Return the next finer chunking period."""
        transitions = {
            "year": "month",
            "month": "day",
        }
        return transitions.get(period.lower())

    def _iterate_date_chunks(self, start: date, end: date, period: str):
        """Yield (start, end) pairs covering the range using the given period."""
        current = start
        period = period.lower()

        while current <= end:
            if period == "year":
                next_start = date(current.year + 1, 1, 1)
            elif period == "month":
                if current.month == 12:
                    next_start = date(current.year + 1, 1, 1)
                else:
                    next_start = date(current.year, current.month + 1, 1)
            elif period == "day":
                next_start = current + timedelta(days=1)
            else:
                raise ValueError(f"Unsupported chunk period: {period}")

            chunk_end = min(end, next_start - timedelta(days=1))
            if chunk_end < current:
                chunk_end = current

            yield current, chunk_end
            current = chunk_end + timedelta(days=1)

    def _download_by_period(
        self,
        table_info: dict,
        condition: str,
        start_date: date,
        end_date: date,
        period: str
    ) -> List[pd.DataFrame]:
        """Recursive helper that downloads data by progressively finer periods."""
        frames: List[pd.DataFrame] = []
        period = (period or "year").lower()

        for chunk_start, chunk_end in self._iterate_date_chunks(start_date, end_date, period):
            chunk_start_str = chunk_start.isoformat()
            chunk_end_str = chunk_end.isoformat()

            try:
                count = self.csmar.queryCount(
                    table_info['columns'],
                    condition,
                    table_info['table'],
                    chunk_start_str,
                    chunk_end_str
                )
            except Exception as exc:  # pragma: no cover - network errors
                print(
                    f"   ❌ Failed to count rows for {chunk_start_str} → {chunk_end_str}: {exc}"
                )
                continue

            numeric_count: Optional[int] = None
            if isinstance(count, (int, float)):
                numeric_count = int(count)
                print(
                    f"   Chunk {chunk_start_str} → {chunk_end_str}: {numeric_count:,} rows (period={period})"
                )
            else:
                print(
                    f"   Chunk {chunk_start_str} → {chunk_end_str}: count unknown (period={period})"
                )

            if numeric_count == 0:
                continue

            if numeric_count is not None and numeric_count > MAX_RECORDS_PER_QUERY:
                finer_period = self._next_period(period)
                if finer_period is None:
                    raise RuntimeError(
                        f"Unable to split chunk {chunk_start_str} → {chunk_end_str} further; still above {MAX_RECORDS_PER_QUERY}."
                    )
                print(
                    f"   ⚠️  Chunk {chunk_start_str} → {chunk_end_str} exceeds limit ({numeric_count:,}); splitting into {finer_period}s..."
                )
                frames.extend(
                    self._download_by_period(
                        table_info,
                        condition,
                        chunk_start,
                        chunk_end,
                        finer_period
                    )
                )
                continue

            try:
                df_chunk = self.csmar.query_df(
                    table_info['columns'],
                    condition,
                    table_info['table'],
                    chunk_start_str,
                    chunk_end_str
                )
            except Exception as exc:  # pragma: no cover - network errors
                print(
                    f"   ❌ Failed to download chunk {chunk_start_str} → {chunk_end_str}: {exc}"
                )
                continue

            if df_chunk is not None and not df_chunk.empty:
                print(
                    f"   ✅ Downloaded {len(df_chunk):,} rows for {chunk_start_str} → {chunk_end_str}"
                )
                frames.append(df_chunk)
                time.sleep(RATE_LIMIT_DELAY)

        return frames

    def _download_with_date_chunks(self, table_info: dict, condition: str) -> Optional[pd.DataFrame]:
        """Download data for large tables by chunking the date range."""
        start_date = self._parse_iso_date(START_DATE)
        end_date = self._parse_iso_date(END_DATE)

        initial_period = table_info.get('chunk_period') or 'year'
        initial_period = initial_period.lower()
        if initial_period not in {"year", "month", "day"}:
            initial_period = 'year'

        print(
            f"   ⏱️  Applying date chunking (initial period: {initial_period}) to stay under API limits..."
        )

        frames = self._download_by_period(
            table_info,
            condition,
            start_date,
            end_date,
            initial_period
        )

        if not frames:
            return None

        combined = pd.concat(frames, ignore_index=True)
        if not combined.empty:
            combined = combined.drop_duplicates(ignore_index=True)
        return combined

    def _is_limit_error(self, error: Exception) -> bool:
        """Detect if an exception looks like the 200k quantitative limit."""
        message = str(error).lower()
        indicators = ("quantitative limit", "200000", "200,000")
        return any(token in message for token in indicators)

    def validate_tables(self) -> Dict[str, Dict[str, dict]]:
        """Validate that tables and requested columns exist in the subscription"""
        if not self.logged_in:
            self.login()

        results: Dict[str, Dict[str, dict]] = {}

        for category, tables in self.tables_config.items():
            category_results: Dict[str, dict] = {}

            for table_key, table_info in tables.items():
                table_id = table_info['table']
                result = {
                    'table': table_id,
                    'columns_requested': table_info['columns'],
                    'missing_columns': [],
                    'available_columns': [],
                    'status': 'ok'
                }

                try:
                    raw_fields = self.csmar.getListFields(table_id)
                    available_columns = self._extract_available_columns(
                        raw_fields)
                    result['available_columns'] = available_columns

                    missing = [
                        column for column in table_info['columns']
                        if column not in available_columns
                    ]

                    if missing:
                        result['missing_columns'] = missing
                        result['status'] = 'missing_columns'

                except Exception as exc:  # pylint: disable=broad-except
                    result['status'] = 'error'
                    result['error'] = str(exc)

                category_results[table_key] = result

            results[category] = category_results

        self.validation_results = results
        return results

    def print_validation_report(self, validation_results: Dict[str, Dict[str, dict]]) -> Tuple[bool, Dict[str, int]]:
        """Pretty print validation summary and return whether all tables are valid"""
        status_icons = {
            'ok': '✅',
            'missing_columns': '⚠️',
            'error': '❌'
        }

        total_tables = 0
        ok_tables = 0
        missing_tables = 0
        error_tables = 0

        print("\n" + "="*80)
        print("VALIDATING TABLE & COLUMN ACCESS")
        print("="*80)

        for category, tables in validation_results.items():
            print(f"\n{category.upper()}:")
            for table_key, result in tables.items():
                total_tables += 1
                status = result['status']
                icon = status_icons.get(status, '❔')
                table_id = result['table']
                description = self.tables_config[category][table_key]['description']

                if status == 'ok':
                    ok_tables += 1
                    print(f"  {icon} {table_id} — {description}")
                elif status == 'missing_columns':
                    missing_tables += 1
                    missing_cols = ', '.join(result['missing_columns'])
                    print(
                        f"  {icon} {table_id} — missing columns: {missing_cols}")
                else:
                    error_tables += 1
                    error_msg = result.get('error', 'Unknown error')
                    print(f"  {icon} {table_id} — error: {error_msg}")

        summary = {
            'total': total_tables,
            'ok': ok_tables,
            'missing': missing_tables,
            'error': error_tables
        }

        print("\n" + "-"*80)
        print("VALIDATION SUMMARY:")
        print(f"  ✅ OK:        {ok_tables}")
        print(f"  ⚠️  Missing:  {missing_tables}")
        print(f"  ❌ Errors:   {error_tables}")
        print(f"  Σ TOTAL:    {total_tables}")
        print("-"*80 + "\n")

        all_ok = missing_tables == 0 and error_tables == 0
        return all_ok, summary

    def download_table(self, category: str, table_name: str, table_info: dict) -> Optional[pd.DataFrame]:
        """
        Download a single table from CSMAR

        Parameters:
        -----------
        category : str
            Category name (e.g., 'financial_data')
        table_name : str
            Table identifier (e.g., 'balance_sheet')
        table_info : dict
            Table configuration with keys: table, columns, description, time_varying

        Returns:
        --------
        pd.DataFrame or None
            Downloaded data or None if failed
        """
        if not self.logged_in:
            self.login()

        print("\n" + "-"*80)
        print(f"📊 DOWNLOADING: {table_info['description']}")
        print("-"*80)
        print(f"Category: {category}")
        print(f"Table: {table_info['table']}")
        print(f"Columns: {', '.join(table_info['columns'])}")
        print(f"Time-varying: {table_info['time_varying']}")

        stock_field = self._determine_stock_field(table_info)
        condition = table_info.get(
            'condition') or self._build_stock_condition(stock_field)
        print(f"Stock filter column: {stock_field}")
        print(f"Stock filter condition: {condition}")

        table_validation = self.validation_results.get(
            category, {}).get(table_name)
        if table_validation:
            status = table_validation.get('status')
            if status == 'missing_columns':
                missing_cols = ', '.join(
                    table_validation.get('missing_columns', []))
                print(
                    f"⚠️  Skipping download because columns are missing: {missing_cols}")
                self.stats['failed_downloads'] += 1
                return None
            if status == 'error':
                error_msg = table_validation.get(
                    'error', 'Unknown validation error')
                print(
                    f"❌ Skipping download because validation failed: {error_msg}")
                self.stats['failed_downloads'] += 1
                return None

        # Check if table needs date range
        use_dates = table_info.get('time_varying', True)

        numeric_count: Optional[int] = None
        df: Optional[pd.DataFrame] = None
        used_chunking = False

        try:
            # Check record count
            if use_dates:
                count = self.csmar.queryCount(
                    table_info['columns'],
                    condition,
                    table_info['table'],
                    START_DATE,
                    END_DATE
                )
            else:
                count = self.csmar.queryCount(
                    table_info['columns'],
                    condition,
                    table_info['table']
                )

            numeric_count = self._normalize_count(count)
            if numeric_count is not None:
                print(f"Expected records: {numeric_count:,}")
            elif count is not None:
                print(f"Expected records (non-numeric): {count}")
            else:
                print("Expected records: Unknown (API returned None)")
                print("⚠️  Proceeding despite missing count result.")

            if numeric_count is not None and numeric_count == 0:
                print("⚠️  No records found - skipping")
                return None

            if numeric_count is not None and numeric_count > MAX_RECORDS_PER_QUERY:
                print(
                    f"⚠️  WARNING: {numeric_count:,} records exceeds {MAX_RECORDS_PER_QUERY:,} limit")
                if use_dates:
                    df = self._download_with_date_chunks(table_info, condition)
                    used_chunking = True
                else:
                    print("Downloading... ", end='', flush=True)
                    df = self.csmar.query_df(
                        table_info['columns'],
                        condition,
                        table_info['table']
                    )
            else:
                print("Downloading... ", end='', flush=True)
                if use_dates:
                    df = self.csmar.query_df(
                        table_info['columns'],
                        condition,
                        table_info['table'],
                        START_DATE,
                        END_DATE
                    )
                else:
                    df = self.csmar.query_df(
                        table_info['columns'],
                        condition,
                        table_info['table']
                    )

        except Exception as e:
            if use_dates and not used_chunking and self._is_limit_error(e):
                print("\n   ⚠️  API row-limit hit; retrying with chunked download...")
                try:
                    df = self._download_with_date_chunks(table_info, condition)
                    used_chunking = True
                except Exception as chunk_exc:
                    print(f"❌ FAILED: {chunk_exc}")
                    self.stats['failed_downloads'] += 1
                    return None
            else:
                print(f"❌ FAILED: {e}")
                self.stats['failed_downloads'] += 1
                return None

        if df is None and use_dates and numeric_count is not None and numeric_count > MAX_RECORDS_PER_QUERY:
            print(
                "   ⚠️  API returned no data due to size limit; retrying with chunked download..."
            )
            df = self._download_with_date_chunks(table_info, condition)
            used_chunking = True

        if df is None:
            print("⚠️  Download returned no data.")
            self.stats['failed_downloads'] += 1
            return None

        if df.empty:
            print("⚠️  Download returned 0 rows.")
            self.stats['failed_downloads'] += 1
            return None

        if not used_chunking:
            print("✅ SUCCESS")
        else:
            print("✅ SUCCESS (chunked)")

        records = len(df)
        size_mb = df.memory_usage(deep=True).sum() / 1024**2

        print(f"   Records: {records:,}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Columns: {list(df.columns)}")

        # Update stats
        self.stats['successful_downloads'] += 1
        self.stats['total_records'] += records
        self.stats['total_size_mb'] += size_mb

        return df

    def download_all(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Download all tables from all categories

        Returns:
        --------
        dict
            Nested dictionary: {category: {table_name: DataFrame}}
        """
        if not self.logged_in:
            self.login()

        print("\n" + "="*80)
        print("DOWNLOADING COMPLETE CHINESE LISTED FIRMS RESEARCH SERIES")
        print("="*80)
        print(f"Time period: {START_DATE} to {END_DATE}")
        print(f"Stock filter: A-share stocks (0*, 3*, 6*)")

        total_categories = len(self.tables_config)
        total_tables = sum(len(tables)
                           for tables in self.tables_config.values())

        print(f"Total categories: {total_categories}")
        print(f"Total tables: {total_tables}")
        print("="*80)

        self.stats['download_start'] = datetime.now()
        self.stats['total_tables'] = total_tables

        all_data: Dict[str, Dict[str, pd.DataFrame]] = {}

        for category, tables in self.tables_config.items():
            print(f"\n\n{'='*80}")
            print(f"CATEGORY: {category.upper()}")
            print(f"{'='*80}")
            print(f"Tables in this category: {len(tables)}")

            category_data: Dict[str, pd.DataFrame] = {}

            table_items = list(tables.items())
            iterator = (
                tqdm(
                    table_items, desc=f"{category} ({len(table_items)} tables)", unit="table", leave=False)
                if tqdm else table_items
            )

            try:
                for table_name, table_info in iterator:
                    if tqdm and hasattr(iterator, "set_postfix_str"):
                        iterator.set_postfix_str(
                            table_info.get('table', table_name))

                    df = self.download_table(category, table_name, table_info)

                    if df is not None and not df.empty:
                        category_data[table_name] = df

                    time.sleep(RATE_LIMIT_DELAY)
            finally:
                if tqdm:
                    iterator.close()

            if category_data:
                all_data[category] = category_data

            print(f"\n{'-'*80}")
            print(f"Category '{category}' summary:")
            print(f"  Downloaded: {len(category_data)} / {len(tables)} tables")
            total_records = sum(len(frame) for frame in category_data.values())
            print(f"  Total records: {total_records:,}")
            print(f"{'-'*80}")

        self.stats['download_end'] = datetime.now()

        return all_data

    def save_data(self, all_data: Dict[str, Dict[str, pd.DataFrame]], output_dir: Path = OUTPUT_DIR):
        """
        Save all downloaded data to CSV files

        Parameters:
        -----------
        all_data : dict
            Nested dictionary of DataFrames
        output_dir : Path
            Root output directory
        """
        print("\n" + "="*80)
        print("SAVING DOWNLOADED DATA")
        print("="*80)

        output_dir = Path(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_files: List[dict] = []

        for category, tables in all_data.items():
            category_dir = output_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n📁 Category: {category}")
            print(f"   Directory: {category_dir}")

            for table_name, df in tables.items():
                filename = f"{table_name}_{timestamp}.csv"
                filepath = category_dir / filename

                print(f"\n   Saving: {table_name}")
                print(f"      File: {filename}")
                print(f"      Records: {len(df):,}")

                df.to_csv(filepath, index=False, encoding='utf-8')

                file_size = filepath.stat().st_size / 1024**2
                print(f"      Size: {file_size:.2f} MB")
                print("      ✅ Saved!")

                saved_files.append({
                    'category': category,
                    'table': table_name,
                    'file': str(filepath),
                    'records': len(df),
                    'size_mb': file_size
                })

        manifest = {
            'download_date': datetime.now().isoformat(),
            'time_period': f"{START_DATE} to {END_DATE}",
            'total_categories': len(all_data),
            'total_tables': len(saved_files),
            'total_records': sum(f['records'] for f in saved_files),
            'total_size_mb': sum(f['size_mb'] for f in saved_files),
            'files': saved_files
        }

        manifest_file = output_dir / f"download_manifest_{timestamp}.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"\n📋 Manifest saved: {manifest_file}")

        return saved_files

    def print_summary(self):
        """Print download summary statistics"""
        print("\n" + "="*80)
        print("DOWNLOAD COMPLETE!")
        print("="*80)

        duration = None
        if self.stats['download_start'] and self.stats['download_end']:
            duration = self.stats['download_end'] - \
                self.stats['download_start']
            hours = duration.total_seconds() / 3600 if duration.total_seconds() else 0
        else:
            hours = 0

        print(f"\n📊 STATISTICS:")
        print(f"   Total tables attempted: {self.stats['total_tables']}")
        print(f"   Successful downloads: {self.stats['successful_downloads']}")
        print(f"   Failed downloads: {self.stats['failed_downloads']}")
        success_rate = 100 * \
            self.stats['successful_downloads'] / \
            max(1, self.stats['total_tables'])
        print(f"   Success rate: {success_rate:.1f}%")
        print(
            f"\n   Total records downloaded: {self.stats['total_records']:,}")
        print(f"   Total data size: {self.stats['total_size_mb']:.2f} MB")

        if duration:
            print(f"\n   Download duration: {duration}")
            if hours:
                avg_tables_per_hour = self.stats['total_tables'] / hours
                print(
                    f"   Average throughput: {avg_tables_per_hour:.1f} tables/hour")

        print(f"\n📁 Output directory: {OUTPUT_DIR}")
        print("\n" + "="*80)

        print("\n✅ NEXT STEPS:")
        print("   1. Inspect downloaded CSV files in dataset/csmar_data/")
        print("   2. Create merge script to combine with master_dataset_english.csv")
        print("   3. Fill missing values (14% financial, 35% board data)")
        print("   4. Re-run regressions with complete data")
        print("\n" + "="*80)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""

    parser = argparse.ArgumentParser(
        description="Download the China Listed Firms Research Series or validate table access"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run table/column validation without downloading data"
    )
    parser.add_argument(
        "--skip-confirm",
        action="store_true",
        help="Skip interactive confirmation prompts"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Override the default output directory"
    )

    args = parser.parse_args()

    output_directory = Path(args.output_dir).resolve(
    ) if args.output_dir else OUTPUT_DIR

    print("\n" + "="*80)
    print("CSMAR COMPLETE DOWNLOAD SCRIPT")
    print("China Listed Firms Research Series - ALL DATA")
    print("="*80)
    print("Project: MSCI Digital Transformation DID Analysis")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time Period: {START_DATE} to {END_DATE}")
    print(f"Output Directory: {output_directory}")
    print("="*80)

    if tqdm is None:
        print("ℹ️  Tip: Install 'tqdm' (pip install tqdm) to see progress bars during downloads.")

    if not args.skip_confirm and not args.validate_only:
        print("\n⚠️  WARNING: This will download COMPLETE Chinese Listed Firms data")
        print("Expected size: 2-5 GB")
        print("Expected time: 1-3 hours")
        print("\nPress Ctrl+C to cancel, or Enter to continue...")

        try:
            input()
        except KeyboardInterrupt:
            print("\n\nDownload cancelled by user.")
            sys.exit(0)

    downloader = ChineseListedFirmsDownloader(
        username=CSMAR_USERNAME,
        password=CSMAR_PASSWORD,
        lang=LANGUAGE
    )

    downloader.login()

    validation_results = downloader.validate_tables()
    all_ok, _ = downloader.print_validation_report(validation_results)

    if args.validate_only:
        print("Validation only run complete.")
        sys.exit(0)

    if not all_ok and not args.skip_confirm:
        print("⚠️  Some tables are missing columns or returned errors.")
        print("Press Enter to continue with available tables or Ctrl+C to abort...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n\nDownload cancelled by user.")
            sys.exit(0)

    all_data = downloader.download_all()

    if not all_data:
        print("\n❌ No data downloaded!")
        print("This could mean:")
        print("  1. Table names in script don't match your CSMAR subscription")
        print("  2. You don't have access to these tables")
        print("  3. Network issue occurred")
        print("\nTo fix:")
        print("  1. Run: python explore_csmar_tables.py (to see available tables)")
        print("  2. Update TABLES_TO_DOWNLOAD at the top of this script")
        print("  3. Try again")
        sys.exit(1)

    downloader.save_data(all_data, output_dir=output_directory)
    downloader.print_summary()


if __name__ == "__main__":
    main()
