# 📦 Installation Guide

## Super Quick (3 Commands)

```bash
chmod +x quickstart.sh
./quickstart.sh
python app.py
```

Open: http://localhost:5000

**Done!** 🎉

---

## Step-by-Step (If Quickstart Doesn't Work)

### 1. Check Python

```bash
python --version
# or
python3 --version
```

**Need Python?**
- **macOS:** `brew install python@3.12`
- **Ubuntu:** `sudo apt install python3 python3-pip`
- **Windows:** Download from [python.org](https://www.python.org/downloads/)

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

**Activated?** Your prompt should now show `(venv)`.

### 4. Upgrade Pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Pandas (data analysis)

### 6. Run the App

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### 7. Open in Browser

Go to: http://localhost:5000

---

## Common Issues

### Issue: "python: command not found"

**Solution:**
Try `python3` instead of `python`:
```bash
python3 app.py
```

### Issue: "pip: command not found"

**Solution:**
Try `pip3` or use Python module:
```bash
pip3 install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

### Issue: "Permission denied" on quickstart.sh

**Solution:**
```bash
chmod +x quickstart.sh
```

### Issue: Dependencies fail to install

**Solution:**
Upgrade pip first:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:**
Edit `app.py` and change the port:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed from 5000
```

---

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 512MB minimum
- **Disk:** 50MB for app + dependencies
- **OS:** macOS, Linux, Windows

---

## What Gets Installed

```
Flask==3.0.0       (~2MB)
pandas==2.1.4      (~35MB)
+ their dependencies
Total: ~40-50MB
```

---

## Manual Installation (Without Quickstart)

If you prefer to do everything manually:

```bash
# 1. Navigate to project directory
cd llm-observatory

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 4. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 5. Install dependencies
pip install Flask==3.0.0 pandas==2.1.4

# 6. Run
python app.py

# 7. Open browser
# http://localhost:5000
```

---

## Verify Installation

### Quick Test

```bash
# Should show Flask version
python -c "import flask; print(flask.__version__)"

# Should show Pandas version
python -c "import pandas; print(pandas.__version__)"

# Should show "Running on..."
python app.py
```

### Upload Test

1. Open http://localhost:5000
2. Click the upload zone
3. Select `example-anthropic-usage.csv`
4. Should see dashboard with data

**If you see data, installation is successful!** ✅

---

## Uninstall

```bash
# Just delete the folder
cd ..
rm -rf llm-observatory

# Or remove just the virtual environment
rm -rf llm-observatory/venv
```

---

## Need Help?

1. Check the error message
2. Try the solutions above
3. Open an issue on GitHub
4. Include:
   - Your OS
   - Python version
   - Error message

We'll help you get it working! 🤝