# Transfer Downloaded Data Back to Mac

After the download completes successfully on Windows, you need to transfer the CSV files back to your macOS computer.

---

## 📂 Files to Transfer

After download, you'll find CSV files in:

```
windows_setup/output/
├── csmar_market_classification_YYYYMMDD_HHMMSS.csv
├── csmar_st_classification_YYYYMMDD_HHMMSS.csv
├── csmar_csrc_industry_2012_YYYYMMDD_HHMMSS.csv
├── csmar_area_classification_YYYYMMDD_HHMMSS.csv
├── csmar_sws_industry_2021_YYYYMMDD_HHMMSS.csv
├── csmar_csrc_industry_2001_YYYYMMDD_HHMMSS.csv
└── csmar_classifications_merged_YYYYMMDD_HHMMSS.csv  ← Most important!
```

**You need ALL CSV files** (6 individual + 1 merged = 7 files total)

---

## 🔄 Transfer Methods

### Method 1: USB Drive (Recommended)

**On Windows PC:**

```
1. Insert USB drive
2. Open File Explorer
3. Navigate to: windows_setup\output\
4. Select all CSV files (Ctrl+A)
5. Copy (Ctrl+C)
6. Navigate to USB drive (usually D:\ or E:\)
7. Create folder: CSMAR_Data_2025
8. Paste files (Ctrl+V)
9. Wait for copy to complete
10. Safely eject USB drive
```

**On Mac:**

```bash
# USB drive should appear as /Volumes/YOUR_USB_NAME
cd /Volumes/YOUR_USB_NAME/CSMAR_Data_2025

# Copy to dataset folder
cp *.csv /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/

# Verify files copied
ls -lh /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/csmar_*.csv
```

### Method 2: Cloud Storage

**On Windows PC:**

**OneDrive:**

```
1. Open OneDrive folder: C:\Users\YourName\OneDrive
2. Create folder: CSMAR_Data_2025
3. Copy all CSV files to this folder
4. Wait for sync to complete (check OneDrive icon in taskbar)
```

**Google Drive:**

```
1. Open browser: https://drive.google.com
2. Upload → Folder → Select windows_setup\output folder
3. Wait for upload to complete
```

**Dropbox:**

```
1. Open Dropbox folder: C:\Users\YourName\Dropbox
2. Create folder: CSMAR_Data_2025
3. Copy all CSV files to this folder
4. Wait for sync
```

**On Mac:**

**OneDrive:**

```bash
# If OneDrive installed
cd ~/OneDrive/CSMAR_Data_2025
cp *.csv /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/
```

**Google Drive:**

```bash
# Download from web, then:
cd ~/Downloads/output
cp *.csv /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/
```

**Dropbox:**

```bash
# If Dropbox installed
cd ~/Dropbox/CSMAR_Data_2025
cp *.csv /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/
```

### Method 3: Email (for small files)

**On Windows PC:**

```
1. Open Windows Explorer
2. Navigate to: windows_setup\output\
3. Right-click on output folder
4. Send to → Compressed (zipped) folder
5. Creates: output.zip
6. Email output.zip to yourself
7. Keep email size under 25MB (Gmail limit)
```

**On Mac:**

```bash
# Download attachment from email
cd ~/Downloads

# Extract zip
unzip output.zip

# Copy to dataset folder
cp output/*.csv /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset/
```

### Method 4: Network Share (same network)

**Prerequisites:**

- Windows PC and Mac on same WiFi/network
- File sharing enabled

**On Windows PC:**

```
1. Right-click output folder
2. Properties → Sharing → Advanced Sharing
3. Check "Share this folder"
4. Set permissions: Everyone → Read
5. Note the network path: \\COMPUTER-NAME\output
```

**On Mac:**

```bash
# In Finder:
1. Go → Connect to Server (Cmd+K)
2. Enter: smb://WINDOWS-PC-IP/output
3. Connect with Windows credentials
4. Copy files to dataset folder
```

---

## ✅ Verify Transfer

After copying files to Mac, verify they're complete:

```bash
cd /Users/ekd/Desktop/Desktop/Others/Patience/code/dataset

# Check files exist
ls -lh csmar_*.csv

# Should see 7 files (6 individual + 1 merged)
# Example output:
# -rw-r--r--  1 ekd  staff   2.1M Oct 15 14:30 csmar_area_classification_20251015_143135.csv
# -rw-r--r--  1 ekd  staff   8.5M Oct 15 14:32 csmar_classifications_merged_20251015_143242.csv
# -rw-r--r--  1 ekd  staff   1.8M Oct 15 14:31 csmar_csrc_industry_2001_20251015_143220.csv
# -rw-r--r--  1 ekd  staff   2.3M Oct 15 14:31 csmar_csrc_industry_2012_20251015_143110.csv
# -rw-r--r--  1 ekd  staff   0.9M Oct 15 14:30 csmar_market_classification_20251015_143022.csv
# -rw-r--r--  1 ekd  staff   1.2M Oct 15 14:30 csmar_st_classification_20251015_143045.csv
# -rw-r--r--  1 ekd  staff   2.7M Oct 15 14:31 csmar_sws_industry_2021_20251015_143158.csv

# Check file contents (first few lines)
head -n 5 csmar_classifications_merged_20251015_143242.csv

# Should show CSV headers and data rows
```

**Expected file sizes:**

- Individual CSVs: 0.5 - 10 MB each
- Merged CSV: 5 - 50 MB
- **Total: ~20-150 MB** (depends on date range and records)

**If files are 0 KB or missing:**

- Download failed or incomplete
- Re-run download script on Windows
- Check download script output for errors

---

## 📝 Next Steps on Mac

After files are transferred and verified:

### 1. Inspect the Data

```bash
# Quick look at merged file
cd /Users/ekd/Desktop/Desktop/Others/Patience/code

# Check columns
head -n 1 dataset/csmar_classifications_merged_20251015_143242.csv

# Count records
wc -l dataset/csmar_classifications_merged_20251015_143242.csv

# Load in Python to inspect
python3 -c "
import pandas as pd
df = pd.read_csv('dataset/csmar_classifications_merged_20251015_143242.csv')
print(f'Records: {len(df):,}')
print(f'Columns: {list(df.columns)}')
print(f'Unique stocks: {df[\"Stkcd\"].nunique():,}')
print(df.head())
"
```

### 2. Update Regenerate Script

Edit `regenerate_analysis_dataset.py` to use the new CSMAR data:

```python
# Add at top
CSMAR_CLASSIFICATIONS = 'dataset/csmar_classifications_merged_20251015_143242.csv'

# Read CSMAR data
csmar_df = pd.read_csv(CSMAR_CLASSIFICATIONS)

# Merge with existing master dataset
master_df = pd.merge(master_df, csmar_df,
                     on='Stkcd',
                     how='left')
```

### 3. Regenerate Analysis Dataset

```bash
# Run regeneration script
python3 regenerate_analysis_dataset.py

# Check output
head -n 5 dataset/analysis_ready_dataset.csv

# Verify new columns exist
python3 -c "
import pandas as pd
df = pd.read_csv('dataset/analysis_ready_dataset.csv')
print('Columns:', df.columns.tolist())
"
```

### 4. Run Baseline Regression

```bash
# Run corrected baseline analysis
python3 run_corrected_baseline_analysis.py

# Check results
cat output/baseline_regression_results.txt

# Look for:
# - Coefficients
# - Standard errors
# - P-values
# - R-squared
```

### 5. Verify Results

```bash
# Compare with previous results
diff output/baseline_regression_results_old.txt output/baseline_regression_results.txt

# Check if coefficients are now significant
grep "did_indicator" output/baseline_regression_results.txt
```

---

## 🔒 Security Note

After transfer, on Windows PC:

```cmd
REM Delete credentials file
del .env

REM Or clear password
notepad .env
REM Set: CSMAR_PASSWORD=DELETED
```

This prevents your password from remaining on a shared/lab computer.

---

## 🐛 Troubleshooting

### "Permission denied" on Mac

```bash
# Fix permissions
chmod 644 dataset/csmar_*.csv

# Try copy again
cp output/*.csv dataset/
```

### "No space left on device"

```bash
# Check disk space
df -h

# Clean up if needed
rm -rf ~/Downloads/old_files
```

### Files won't copy from USB

```bash
# Check if USB is mounted
ls /Volumes/

# If not visible:
# 1. Unplug USB
# 2. Replug USB
# 3. Check Finder → Locations
```

### CSV files corrupted

**Signs:**

- File size 0 KB
- Can't open in Excel/Numbers
- Python read_csv() fails

**Fix:**

- Re-download on Windows
- Check download script completed without errors
- Verify internet was stable during download
- Try different transfer method

---

## 📊 File Format Details

### Individual Classification Files

**Columns (example for market_classification):**

```csv
Stkcd,MarketType,ListedDate,BoardType
000001,SZSE,1991-04-03,Main Board
000002,SZSE,1991-01-29,Main Board
600000,SSE,1999-11-10,Main Board
```

**Key:**

- `Stkcd`: 6-digit stock code
- `MarketType`: SZSE (Shenzhen) or SSE (Shanghai)
- `ListedDate`: IPO date
- `BoardType`: Main Board, SME Board, ChiNext, STAR

### Merged Classification File

**Structure:**

```csv
Stkcd,Date,MarketType,IsST,IndustryCode_CSRC2012,ProvinceCode,...
000001,2010-01-01,SZSE,0,J66,440000,...
000001,2011-01-01,SZSE,0,J66,440000,...
```

**Features:**

- One row per stock per year (if time-varying)
- All classifications merged on `Stkcd` (and `Date` if applicable)
- Missing values filled with appropriate defaults
- Duplicate columns renamed with suffixes

---

## 🎯 Success Criteria

You've successfully transferred when:

- ✅ All 7 CSV files in dataset/ folder on Mac
- ✅ Files have reasonable sizes (not 0 KB)
- ✅ Can open CSV in Excel/Numbers/TextEdit
- ✅ Python can read CSV without errors
- ✅ Data has expected columns (Stkcd, classification fields)
- ✅ Record counts match expectations (thousands of rows)
- ✅ Unique stock codes match A-share universe (~5,000-6,000)

---

## 📞 Need Help?

If transfer fails:

1. **Check disk space** on both Mac and Windows
2. **Try different transfer method** (USB vs cloud vs email)
3. **Compress files** to reduce size: `zip -r csmar_data.zip output/`
4. **Transfer one file at a time** if batch transfer fails
5. **Use terminal** instead of Finder if GUI has issues

---

**Ready to continue your analysis!** 🎉

Next: Update `regenerate_analysis_dataset.py` to use new CSMAR data
