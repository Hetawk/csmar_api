# CSMAR API Manual Installation Guide

## Issue

The `python_3.6.0.rar` file from CSMAR only contains a Python 3.6 installer, NOT the csmarapi library itself.

## Solution

You need to download the **CSMAR API library separately**.

## Download the correct CSMAR API:

1. **Option 1: CSMAR Website (Recommended)**

   - Login to: https://www.gtarsc.com/ or https://data.csmar.com/
   - Go to: Help → API Documentation → Python API
   - Download the **csmarapi library** (NOT just Python installer)
   - Look for a file like: `csmarapi.zip` or `CSMAR-PYTHON.zip`

2. **Option 2: Direct Link (if available)**

   - Try: https://data.csmar.com/download/csmarapi.zip
   - Or contact CSMAR support for the correct API library download link

3. **What you're looking for:**
   - A ZIP/RAR file containing a folder named `csmarapi`
   - Inside should be files like:
     - `CsmarService.py`
     - `ReportUtil.py`
     - Other Python modules

## Once you have the correct csmarapi files:

1. Extract the ZIP/RAR
2. Copy the `csmarapi` folder to:

   ```
   D:\coding_env\py\windows_setup\.venv\Lib\site-packages\
   ```

3. Verify installation:
   ```powershell
   python test_csmar_api.py
   ```

## Alternative: Use System Python (if API is already installed elsewhere)

If you have the CSMAR API working in another Python installation:

1. Find the csmarapi folder
2. Copy it to the venv site-packages folder above

## Contact CSMAR Support

If you cannot find the API library:

- Email: service@gtadata.com
- Request the **Python API library** (csmarapi) download link
- Mention you have Python 3.12 and need the API module files
