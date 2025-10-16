# CSMAR Data Acquisition Scripts

This folder contains scripts for downloading data from CSMAR database using the official Python API.

## 📁 Files

### Complete Data Downloads

- **`download_all_chinese_listed_firms.py`** - ⭐ **NEW** Download ALL data from Chinese Listed Firms Research Series (2010-2024)
- **`explore_csmar_tables.py`** - Explore available CSMAR tables and columns

### Specific Data Downloads

- **`download_csmar_classifications.py`** - Download stock classification data (6 types)
- **`test_csmar_api.py`** - Test script to verify CSMAR API installation
- **`setup_csmar_api.sh`** - Bash script to install Python dependencies

## 🚀 Quick Start

### Option A: Download EVERYTHING (Recommended)

**Use `download_all_chinese_listed_firms.py` to get complete Chinese Listed Firms data:**

- All financial statements (balance sheet, income, cash flow)
- All financial ratios (ROA, ROE, Tobin's Q, profitability, liquidity, leverage)
- Board characteristics (size, independence, meetings)
- Shareholder structure (ownership concentration, top shareholders)
- Executive compensation, M&A, IPO/delisting data
- **Time period: 2010-2024 (15 years)**
- **Expected size: 2-5 GB**
- **Expected time: 1-3 hours**

[Jump to Complete Download Instructions](#complete-data-download-2010-2024)

### Option B: Download Only Classifications

**Use `download_csmar_classifications.py` for stock classifications only:**

- Market type, ST status, industry codes, area codes
- **Time period: All historical data**
- **Expected size: <100 MB**
- **Expected time: 5-15 minutes**

[Jump to Classification Download Instructions](#classification-data-download)

---

## Prerequisites

1. **CSMAR Account** - Personal registered account (not institutional)
2. **Python 3.6+** - Check with `python3 --version`
3. **Windows OS** - CSMAR-PYTHON currently only works on Windows

### Step 1: Install Dependencies

```bash
cd /Users/ekd/Desktop/Desktop/Others/Patience/code
chmod +x setup_csmar_api.sh
./setup_csmar_api.sh
```

This installs:

- urllib3
- websocket
- websocket_client
- pandas
- prettytable

### Step 2: Install CSMAR-PYTHON Library

1. **Login to CSMAR:** https://www.gtarsc.com/
2. **Navigate to:** Data Download → API Interface
3. **Download:** CSMAR-PYTHON.zip
4. **Extract to:** `[Python Installation]/Lib/site-packages/`

   ```bash
   # Find Python installation
   python3 -c "import sys; print(sys.executable)"
   # Example: /usr/local/bin/python3

   # Extract to site-packages
   # Example: /usr/local/lib/python3.9/site-packages/csmarapi/
   ```

### Step 3: Test Installation

```bash
python3 test_csmar_api.py
```

Expected output:

```
======================================================================
CSMAR API Installation Test
======================================================================

Test 1: Checking if CSMAR API is installed...
✅ CSMAR API modules found!

Test 2: Checking required dependencies...
  ✅ urllib3
  ✅ websocket
  ✅ pandas
  ✅ prettytable

✅ All dependencies installed!

Test 3: Creating CSMAR service instance...
✅ CsmarService instance created!

======================================================================
✅ ALL TESTS PASSED!
======================================================================
```

### Step 4: Configure Credentials

Edit `download_csmar_classifications.py`:

```bash
nano download_csmar_classifications.py
```

Update lines 44-46:

```python
CSMAR_USERNAME = "enoch.dongbo@stu.ujn.edu.cn"  # Your CSMAR login
CSMAR_PASSWORD = "your_password_here"           # Your password
LANGUAGE = "1"  # 0=Chinese, 1=English
```

### Step 5: Run Download

```bash
python3 download_csmar_classifications.py
```

---

## 🌟 Complete Data Download (2010-2024)

### What You'll Get

The `download_all_chinese_listed_firms.py` script downloads **EVERYTHING** from CSMAR's "China Listed Firms Research Series":

#### 1. **Basic Info** (基本信息)

- Company profiles (name, listing date, location, registered capital)
- Listing status (trading status, market type, board type)
- ST status (special treatment stocks)
- Industry classifications (CSRC, SWS)

#### 2. **Financial Data** (财务数据)

- Balance sheet (assets, liabilities, equity)
- Income statement (revenue, profit, expenses, R&D)
- Cash flow statement (operating, investing, financing)
- Financial indicators (liquidity ratios, leverage ratios)
- Profitability ratios (ROA, ROE, profit margins)
- Growth ratios (YoY growth rates)

#### 3. **Equity & Governance** (股权治理)

- Board characteristics (size, independence, meetings)
- Shareholder structure (top shareholders, ownership concentration)
- Executive compensation (salary, bonuses, equity)
- Subsidiary structure (active holdings, exits) and core staff roster
- Institutional ownership (funds, QFII, social security)

#### 4. **Financing & Distribution** (融资分配)

- IPO data (offering details, pricing, allocation)
- SEO data (seasoned equity offerings)
- Dividends (cash dividends, stock dividends, payout ratio)
- Debt financing (bond issuance, bank loans)

#### 5. **Major Events** (重大事件)

- M&A activities (mergers, acquisitions, restructuring)
- Related party transactions
- Litigation and disputes
- Corporate name changes

#### 6. **Feature Topics** (特色专题)

- Digital transformation indicators
- ESG metrics (environmental, social, governance)
- Innovation metrics (patents, R&D intensity)

#### 7. **Text Analysis** (文本分析)

- Annual report sentiment analysis
- Management discussion & analysis (MD&A) topics

#### 8. **Stock Market Data** (股票市场数据)

- Market valuation (Tobin's Q, P/E, P/B ratios)
- Trading summary (volume, turnover, volatility)
- Stock returns (annual returns, beta)

### Time Period

- **Start:** 2010-01-01
- **End:** 2024-12-31
- **Total:** 15 years of data

### Setup Environment Variables

Create a `.env` file in project root:

```bash
cd /Users/ekd/Desktop/Desktop/Others/Patience/code
nano .env
```

Add these lines:

```bash
# CSMAR API Credentials
CSMAR_USERNAME=your_email@example.com
CSMAR_PASSWORD=your_password_here
CSMAR_LANGUAGE=1  # 0=Chinese, 1=English

# Date range (2010-2024)
CSMAR_START_DATE=2010-01-01
CSMAR_END_DATE=2024-12-31
```

Save and exit (Ctrl+X, Y, Enter)

### Run Complete Download

```bash
cd /Users/ekd/Desktop/Desktop/Others/Patience/code
python3 src/python/data_acquisition/download_all_chinese_listed_firms.py
```

**What happens:**

1. Script prompts for confirmation (shows expected size and time)
2. Logs in to CSMAR API
3. Downloads data from 9 major categories
4. Each category saved to `dataset/csmar_data/{category}/`
5. Progress shown for each table
6. Summary statistics displayed at end

### Expected Output

```
================================================================================
DOWNLOADING COMPLETE CHINESE LISTED FIRMS RESEARCH SERIES
================================================================================
Time period: 2010-01-01 to 2024-12-31
Stock filter: A-shares only (0%, 3%, 6% codes)
Output: dataset/csmar_data/
================================================================================

Progress: 1/40 tables

--------------------------------------------------------------------------------
📊 DOWNLOADING: Balance sheet - annual
--------------------------------------------------------------------------------
Category: financial_data
Table: FS_Balance_Sheet
Columns: Stkcd, Date, TotalAssets, TotalLiabilities, ...
Time-varying: True
Expected records: 75,000
Downloading... ✅ SUCCESS
   Records: 74,856
   Size: 125.43 MB
   Columns: ['Stkcd', 'Date', 'TotalAssets', ...]

...

================================================================================
DOWNLOAD SUMMARY
================================================================================
Successful downloads: 38/40
Failed downloads: 2/40 (table names may need updating)
Total records: 3,245,678
Total size: 2,847.52 MB (2.78 GB)
================================================================================
```

### Output Structure

```
dataset/csmar_data/
├── basic_info/
│   ├── company_profile_20251016_143052.csv
│   ├── listing_status_20251016_143052.csv
│   ├── st_status_20251016_143052.csv
│   └── industry_classification_20251016_143052.csv
├── financial_data/
│   ├── balance_sheet_20251016_143052.csv
│   ├── income_statement_20251016_143052.csv
│   ├── cash_flow_20251016_143052.csv
│   ├── financial_indicators_20251016_143052.csv
│   ├── profitability_ratios_20251016_143052.csv
│   └── growth_ratios_20251016_143052.csv
├── equity_governance/
│   ├── board_characteristics_20251016_143052.csv
│   ├── shareholder_structure_20251016_143052.csv
│   ├── executive_compensation_20251016_143052.csv
│   └── institutional_ownership_20251016_143052.csv
├── financing_distribution/
│   ├── ipo_data_20251016_143052.csv
│   ├── seo_data_20251016_143052.csv
│   ├── dividends_20251016_143052.csv
│   └── debt_financing_20251016_143052.csv
├── major_events/
│   ├── ma_activities_20251016_143052.csv
│   ├── related_party_20251016_143052.csv
│   └── litigation_20251016_143052.csv
├── feature_topics/
│   ├── digital_transformation_20251016_143052.csv
│   ├── esg_metrics_20251016_143052.csv
│   └── innovation_20251016_143052.csv
├── text_analysis/
│   ├── sentiment_analysis_20251016_143052.csv
│   └── mda_topics_20251016_143052.csv
├── stock_market/
│   ├── market_value_20251016_143052.csv
│   ├── trading_summary_20251016_143052.csv
│   └── stock_returns_20251016_143052.csv
└── manifest_20251016_143052.json  # Download metadata
```

### Troubleshooting Complete Download

#### Some Tables Failed to Download

**Cause:** Table names in script don't match your CSMAR subscription

**Solution:** Explore available tables first:

```bash
python3 src/python/data_acquisition/explore_csmar_tables.py
```

This shows all tables you have access to. Update table names in `download_all_chinese_listed_firms.py` accordingly.

#### Download Taking Too Long

**Cause:** 2-5 GB is a lot of data

**Solutions:**

1. **Run overnight** - Let it complete while you sleep
2. **Use faster internet** - University/office connection is better
3. **Download in batches** - Comment out some categories in the script
4. **Target specific tables** - Only download what you need

#### Out of Memory Error

**Cause:** Loading large tables into RAM

**Solution:** The script processes tables one at a time and saves to disk immediately, so this is rare. If it happens:

```python
# Edit download_all_chinese_listed_firms.py
# Add chunking for very large tables (>1GB)
```

---

## 📋 Classification Data Download

This will:

1. Login to CSMAR API
2. Download 6 classification types:
   - Stock Market Classification (Shanghai/Shenzhen)
   - ST & Non-ST stocks
   - CSRC Industry 2012
   - Area Classification
   - SWS Industry 2021
   - CSRC Industry 2001
3. Save individual CSVs to `../../dataset/`
4. Merge all into one master file

**Expected time:** 5-15 minutes depending on network speed

## 📊 Output Files

All files saved to `dataset/` folder:

- `csmar_market_classification_YYYYMMDD_HHMMSS.csv` (~5,607 records)
- `csmar_st_classification_YYYYMMDD_HHMMSS.csv` (~80,000+ records)
- `csmar_csrc_industry_2012_YYYYMMDD_HHMMSS.csv` (~80,000+ records)
- `csmar_area_classification_YYYYMMDD_HHMMSS.csv` (~5,607 records)
- `csmar_sws_industry_2021_YYYYMMDD_HHMMSS.csv` (~80,000+ records)
- `csmar_csrc_industry_2001_YYYYMMDD_HHMMSS.csv` (~80,000+ records)
- `csmar_classifications_merged_YYYYMMDD_HHMMSS.csv` (master file)

## 🔧 Customization

### Download Different Tables

Edit the `download_all_classifications()` method:

```python
# Example: Add market index data
df_index = self.download_classification_data(
    table_name='STK_Market_Index',  # Check with getListTables()
    columns=['Date', 'IndexCode', 'ClosePrice'],  # Check with getListFields()
    condition="IndexCode like 'SH000001'",  # Shanghai Composite
    description="Market Index Data"
)
datasets['market_index'] = df_index
```

### Change Date Range

Edit lines 41-42:

```python
START_DATE = "2015-01-01"  # Change start date
END_DATE = "2023-12-31"    # Change end date
```

### Download Specific Companies Only

Modify the `condition` parameter:

```python
# Original (all A-shares)
condition="Stkcd like '0%' or Stkcd like '3%' or Stkcd like '6%'"

# Only Shanghai Stock Exchange
condition="Stkcd like '6%'"

# Only specific company
condition="Stkcd='000001'"

# Multiple specific companies
condition="Stkcd in ('000001', '000002', '600000')"
```

## 🆘 Troubleshooting

### Error: "CSMAR API not installed"

**Cause:** CSMAR-PYTHON not in Python's site-packages

**Solution:**

```bash
# Check if csmarapi folder exists
ls [Python]/Lib/site-packages/csmarapi

# If not found, re-download and extract CSMAR-PYTHON.zip
```

### Error: "Login failed"

**Possible causes:**

1. Wrong username/password
2. Using institutional account (need personal account)
3. Account not verified
4. Network issue

**Solution:** Verify credentials at https://www.gtarsc.com/

### Error: "No records found"

**Possible causes:**

1. Wrong table name
2. Wrong column names
3. No permission for that table

**Solution:** Explore available tables:

```python
from csmarapi.CsmarService import CsmarService
csmar = CsmarService()
csmar.login('username', 'password', '1')

# List all databases
databases = csmar.getListDbs()

# List tables in a database
tables = csmar.getListTables('China Stock Market Series')

# List fields in a table
fields = csmar.getListFields('STK_MKT_Type')
```

### Error: "Same query only allowed once in 30 minutes"

**Cause:** CSMAR rate limiting

**Solution:** Wait 30 minutes before running identical query again

### Error: "More than 200,000 records"

**Cause:** CSMAR API has 200K record limit per query

**Solution:** Use pagination (automatically handled in script, but you can customize):

```python
# First batch
df1 = csmar.query_df(columns, "Stkcd like '0%' limit 0,200000", table_name)

# Second batch
df2 = csmar.query_df(columns, "Stkcd like '0%' limit 200000,200000", table_name)

# Combine
df = pd.concat([df1, df2], ignore_index=True)
```

## 📚 API Documentation

See full documentation in: `../../docs/CSMAR_DATA_DOWNLOAD_GUIDE.md`

### Key Functions

```python
from csmarapi.CsmarService import CsmarService
csmar = CsmarService()

# Login
csmar.login('username', 'password', '1')  # 1=English, 0=Chinese

# List databases
databases = csmar.getListDbs()

# List tables
tables = csmar.getListTables('China Stock Market Series')

# List fields
fields = csmar.getListFields('STK_MKT_Type')

# Count records
count = csmar.queryCount(columns, condition, table_name, start_date, end_date)

# Download data as DataFrame
df = csmar.query_df(columns, condition, table_name, start_date, end_date)
```

## 🔗 Resources

- **CSMAR Website:** https://www.gtarsc.com/
- **API Documentation:** https://www.gtarsc.com/api/ (login required)
- **Technical Support:** service@gtarsc.com
- **Phone:** +86 (0755) 8670 3017

## 📝 Notes

1. **Windows Only:** CSMAR-PYTHON currently only works on Windows
2. **Personal Accounts Only:** Institutional accounts don't support API access
3. **Rate Limiting:** 30-minute cooldown between identical queries
4. **Record Limit:** 200,000 records per query (use pagination for more)
5. **Subscription Required:** You must have active CSMAR subscription

## 🎯 Next Steps

After downloading classification data:

1. **Verify downloads:**

   ```bash
   ls -lh ../../dataset/csmar_*.csv
   wc -l ../../dataset/csmar_*.csv
   ```

2. **Integrate into pipeline:**

   ```bash
   cd ../..
   python3 regenerate_analysis_dataset.py
   ```

3. **Run baseline regression:**
   ```bash
   python3 run_corrected_baseline_analysis.py
   ```

---

## 🎯 Recommended Workflow

### For Complete Analysis (Recommended)

```bash
# 1. Download ALL data (2010-2024)
python3 src/python/data_acquisition/download_all_chinese_listed_firms.py

# 2. Merge with existing master dataset
python3 merge_csmar_complete_data.py  # To be created

# 3. Re-run analysis with complete data
python3 run_corrected_baseline_analysis.py
```

### For Quick Classification Update

```bash
# 1. Download classifications only
python3 src/python/data_acquisition/download_csmar_classifications.py

# 2. Integrate into pipeline
python3 regenerate_analysis_dataset.py

# 3. Run baseline regression
python3 run_corrected_baseline_analysis.py
```

---

**Last Updated:** October 16, 2025  
**Time Period:** 2010-2024 (15 years)  
**Project:** MSCI Digital Transformation DID Analysis  
**Author:** Enoch Dongbo (enoch.dongbo@stu.ujn.edu.cn)
