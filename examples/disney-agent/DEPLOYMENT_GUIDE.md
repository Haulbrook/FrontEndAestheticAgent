# Deployment & Usage Guide

## Option 1: Use Locally (Quickest - 5 minutes)

This is the fastest way to start using the app right now on your computer.

### Steps:

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Version 3.8 or higher required

2. **Open Terminal/Command Prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: Press `Ctrl + Alt + T`

3. **Navigate to the project folder**
   ```bash
   cd path/to/Disney-Agent
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your OpenAI API Key**

   Create a `.env` file:
   ```bash
   # Copy the example file
   cp .env.example .env
   ```

   Open `.env` in a text editor and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

   **Get an OpenAI API Key:**
   - Go to [platform.openai.com](https://platform.openai.com/api-keys)
   - Sign up/Login
   - Click "Create new secret key"
   - Copy the key to your `.env` file

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

7. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually open that URL in your browser

**You're done!** The app is now running on your computer.

---

## Option 2: Deploy Online (Free - Streamlit Cloud) ⭐ RECOMMENDED

Deploy your app for free so you can access it from anywhere (phone, tablet, any computer).

### Prerequisites:
- GitHub account (free)
- OpenAI API key

### Steps:

#### 1. Push Code to GitHub

If you haven't already:

```bash
# The code is already pushed to your branch!
# Just make sure it's up to date
git status
```

#### 2. Sign up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up"
3. Sign in with your GitHub account
4. Authorize Streamlit to access your repositories

#### 3. Deploy Your App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: `Haulbrook/Disney-Agent`
   - **Branch**: `claude/create-trip-planning-agent-011CUYcpyA764NQCZvCdBK2F` (or `main` if you've merged)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (e.g., `my-disney-planner`)

3. Click **"Advanced settings"** (optional but recommended)
   - Python version: `3.11`

4. Add your **Secrets** (API Key):
   - Click "Advanced settings" → "Secrets"
   - Add this in the secrets text box:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-api-key-here"
     OPENAI_MODEL = "gpt-4-turbo-preview"
     ```

5. Click **"Deploy!"**

#### 4. Wait for Deployment

- Streamlit will install dependencies and launch your app
- Takes about 2-3 minutes
- You'll see a build log

#### 5. Access Your App

- Once deployed, you'll get a URL like: `https://my-disney-planner.streamlit.app`
- **This URL works from any device!** Share it with family members planning the trip
- The app is always online and accessible

### Benefits of Streamlit Cloud:
- ✅ **Free** for public repositories
- ✅ **No server management** required
- ✅ **Auto-updates** when you push changes
- ✅ **Access from anywhere** (phone, tablet, laptop)
- ✅ **Share with others** via simple URL
- ✅ **HTTPS** secure by default

---

## Option 3: Deploy to Other Platforms

### Heroku (More Control)

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Deploy:
   ```bash
   heroku create my-disney-planner
   heroku config:set OPENAI_API_KEY=your_key_here
   git push heroku main
   ```

**Cost:** Free tier available, $7/month for better performance

### Railway.app (Modern & Simple)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `Disney-Agent` repository
5. Add environment variables in dashboard
6. Deploy automatically

**Cost:** $5/month with free trial credits

### Google Cloud Run (Scalable)

1. Containerize with Docker
2. Push to Google Container Registry
3. Deploy to Cloud Run

**Cost:** Free tier available, pay per use

### AWS EC2 (Full Control)

1. Launch EC2 instance
2. Install dependencies
3. Run with systemd or screen
4. Configure security groups

**Cost:** Free tier available for 1 year

---

## Recommendation

**For most users:** Use **Streamlit Cloud** (Option 2)
- It's free
- Super easy (5 minutes to deploy)
- Perfect for family/personal use
- No maintenance required
- Professional URL you can share

**For local-only use:** Use **Local setup** (Option 1)
- If you don't want to share online
- Testing and development
- Complete privacy

---

## Updating Your Deployed App

Once deployed on Streamlit Cloud:

1. Make changes to your code locally
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update features"
   git push
   ```
3. **Streamlit Cloud auto-deploys!** Your app updates in ~2 minutes

---

## Troubleshooting

### "Module not found" errors
- Make sure `requirements.txt` includes all dependencies
- In Streamlit Cloud, click "Reboot app" to reinstall

### "OpenAI API key not found"
- Check your `.env` file (local) or Secrets (Streamlit Cloud)
- Make sure the key is valid and has credits

### App is slow
- GPT-4 can be slow on first use
- Consider using `gpt-3.5-turbo` for faster responses (edit `.env`)
- Streamlit Cloud free tier has some limitations

### Can't access from phone
- If using local setup (Option 1), you need to be on same WiFi network
- Use `streamlit run app.py --server.address=0.0.0.0` and access via your computer's IP
- **Better solution:** Deploy to Streamlit Cloud for universal access

---

## Security Notes

- **Never commit your `.env` file** (it's in `.gitignore` already)
- **Don't share your OpenAI API key** publicly
- In Streamlit Cloud, use the Secrets manager (not in code)
- Monitor your OpenAI usage at [platform.openai.com/usage](https://platform.openai.com/usage)

---

## Cost Considerations

### OpenAI API Costs:
- GPT-4 Turbo: ~$0.01 per checklist generation
- GPT-3.5 Turbo: ~$0.001 per checklist (much cheaper)
- Typical planning session: $0.05-$0.20
- Set spending limits in OpenAI dashboard

### Hosting Costs:
- **Streamlit Cloud:** Free for public repos
- **Local:** Free (runs on your computer)
- **Other platforms:** $0-$7/month typically

---

## Next Steps

1. Choose your deployment method
2. Get your OpenAI API key
3. Deploy/run the app
4. Start planning your magical Disney trip! ✨

Need help? Check the main README.md or open an issue on GitHub.
