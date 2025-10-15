# Windows Setup Package - Quick Start

**Complete package for downloading CSMAR data on Windows PC**

---

## 📦 What's Included

```
windows_setup/
├── README.md                          # Full documentation
├── TRANSFER_BACK_TO_MAC.md           # Transfer instructions
├── setup_windows.bat                  # One-click setup script
├── download_csmar_classifications.py  # Main download script
├── test_csmar_api.py                  # Test installation
├── requirements.txt                   # Python dependencies
└── .env.example                       # Credential template
```

---

## 🚀 Quick Start (3 Steps)

### 1. Transfer to Windows PC

Copy this entire `windows_setup/` folder to your Windows PC using:

- USB drive, OR
- Cloud storage (OneDrive/Google Drive/Dropbox), OR
- Email (if folder is small)

### 2. Run Setup

On Windows PC:

1. Open Command Prompt in `windows_setup` folder
2. Run: `setup_windows.bat`
3. Follow on-screen instructions

### 3. Download Data

1. Edit `.env` with your credentials: `notepad .env`
2. Run: `python download_csmar_classifications.py`
3. Wait 15-30 minutes for download
4. Transfer CSV files back to Mac (see `TRANSFER_BACK_TO_MAC.md`)

---

## 📋 Prerequisites

**On Windows PC:**

- Windows 7/10/11 (any version)
- Python 3.8+ ([download](https://www.python.org/downloads/))
- CSMAR-PYTHON library ([download](https://data.csmar.com/static/python_3.6.0.rar))
- Internet connection
- 500MB free disk space

**CSMAR Account:**

- Personal registered account (not institutional)
- Valid username/password
- Access to "China Stock Market Series" database

---

## 📖 Detailed Instructions

See `README.md` in this folder for:

- Complete setup guide
- Troubleshooting
- CSMAR-PYTHON installation steps
- Expected output examples

---

## 🎯 What You'll Download

**6 Classification Datasets:**

1. Stock Market Classification (Shanghai/Shenzhen)
2. ST & Non-ST stocks
3. CSRC Industry 2012
4. Area Classification (Province/City)
5. SWS Industry 2021
6. CSRC Industry 2001

**Plus:**

- Merged classification file (all 6 combined)

**Time Period:** 2010-2024  
**Sample:** All A-share companies (~5,607 codes)

---

## ✅ Checklist

Before running download:

- [ ] Transferred `windows_setup/` folder to Windows PC
- [ ] Python 3.8+ installed
- [ ] CSMAR-PYTHON library installed
- [ ] Ran `setup_windows.bat`
- [ ] All tests passed
- [ ] Edited `.env` with credentials

After download:

- [ ] CSV files in `output/` folder
- [ ] Files look correct (not 0KB)
- [ ] Transferred back to Mac
- [ ] Files in Mac's `dataset/` folder

---

## 🆘 Help

**Setup issues?**

- Read `README.md` in this folder
- Check Troubleshooting section

**Download issues?**

- Verify CSMAR credentials at: https://www.gtarsc.com/
- Check internet connection
- See `README.md` → Troubleshooting

**Transfer issues?**

- See `TRANSFER_BACK_TO_MAC.md`
- Try different transfer method

---

## 🔄 Workflow Overview

```
Mac                Windows PC            Mac
 │                     │                  │
 ├─ Copy setup files ──→                 │
 │                     │                  │
 │                     ├─ Run setup      │
 │                     ├─ Download data  │
 │                     ├─ Save CSVs      │
 │                     │                  │
 │                 ←── Transfer CSVs ────┤
 │                     │                  │
 ├─ Regenerate dataset                   │
 ├─ Run regression                       │
 └─ Check results                        │
```

---

**Let's download that CSMAR data!** 🎉

Open `README.md` for detailed instructions.
