# SETUP FIX - App Won't Load? Read This!

## The Problem
Your Disney Trip Planning app wasn't loading because **the required Python dependencies were not installed**.

## The Solution

Follow these steps IN ORDER to get your app working:

### Step 1: Install Dependencies

Open your terminal/command prompt in the Disney-Agent folder and run:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Streamlit (the web framework)
- OpenAI (for AI features)
- Firebase Admin (for multi-user collaboration)
- And many other dependencies

**This step is REQUIRED before the app can run!**

### Step 2: Set Up Your OpenAI API Key

The app REQUIRES an OpenAI API key to function. You have two options:

#### Option A: Using .env File (Recommended for Local Use)

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

#### Option B: Using Streamlit Secrets (For Deployment)

1. Create a `.streamlit` folder if it doesn't exist
2. Create a `secrets.toml` file inside it
3. Add your API key:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-key-here"
   ```

### Step 3: Run the App

Once dependencies are installed and API key is configured:

```bash
streamlit run app.py
```

The app should now open in your browser at `http://localhost:8501`

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** You didn't install the dependencies. Run `pip install -r requirements.txt`

### Issue: "OpenAI API key not found" or "OpenAI API key not configured"
**Solution:**
- Make sure you created the `.env` file (not `.env.example`)
- Check that your API key starts with `sk-`
- Ensure there are no extra spaces in the `.env` file
- Try restarting the app after adding the key

### Issue: App loads but shows blank/white screen
**Solution:**
- Check your browser console for errors (F12 → Console tab)
- Try clearing your browser cache
- Try a different browser
- Make sure port 8501 isn't being used by another app

### Issue: "Connection error" or "Network error"
**Solution:**
- Check your internet connection (required for OpenAI API calls)
- Verify your OpenAI API key is valid and has credits
- Check if you're behind a firewall/proxy

### Issue: Firebase errors
**Solution:**
- Firebase is OPTIONAL for multi-user features
- The app will work fine without Firebase
- You can ignore Firebase warnings/errors

## Verifying the Fix

To test if everything is working:

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with your API key
3. Run: `python -c "import streamlit; import openai; print('Success!')"`
4. If that works, run: `streamlit run app.py`

## Still Not Working?

If you've followed all steps and it's still not loading:

1. **Check Python version:** Run `python --version` (need 3.8 or higher)
2. **Try using a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. **Check the terminal output** for specific error messages
4. **Look for typos** in your `.env` file

## Quick Checklist

- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Created `.env` file (not `.env.example`)
- [ ] Added valid OpenAI API key to `.env`
- [ ] Confirmed Python 3.8+ (`python --version`)
- [ ] No other app using port 8501
- [ ] Internet connection working

## What Was Wrong?

The app uses many Python libraries (Streamlit, OpenAI, Firebase, etc.) that don't come pre-installed with Python. Without running `pip install -r requirements.txt`, none of these libraries were available, causing the app to fail immediately when trying to import them.

Think of it like trying to bake a cake without buying the ingredients first!

---

**Need more help?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.
