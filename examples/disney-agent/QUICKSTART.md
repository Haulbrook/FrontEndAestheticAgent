# Quick Start Guide - 5 Minutes to Your First Trip Plan! ⚡

## Fastest Way to Use the App

### Step 1: Get Your OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. **Important:** Keep this key private!

### Step 2: Set Up the App (1 minute)

1. Open the `Disney-Agent` folder in your file explorer
2. Find the file named `.env.example`
3. Create a copy and rename it to `.env` (remove the `.example`)
4. Open `.env` in any text editor (Notepad, TextEdit, etc.)
5. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-abc123yourkeyhere
   ```
6. Save the file

### Step 3: Install & Run (2 minutes)

**Open Terminal/Command Prompt:**
- Windows: Press `Win + R`, type `cmd`, press Enter
- Mac: Press `Cmd + Space`, type "terminal", press Enter

**Run these commands:**

```bash
# Go to the project folder
cd path/to/Disney-Agent

# Install dependencies (one-time only)
pip install -r requirements.txt

# Start the app
streamlit run app.py
```

**That's it!** Your browser will open automatically with the app running.

---

## Using the App

### 1. Enter Your Trip Details (left sidebar)
- Select your Disney destination
- Pick your travel dates
- Enter party size and ages
- Choose interests and budget

### 2. Generate Your Plan
- Click **"Create/Update Trip Plan"** button
- Wait 10-20 seconds for AI to generate everything

### 3. Explore Features

**✅ Checklists Tab**
- See your personalized checklist
- Check off items as you complete them
- Click "Find Forgotten Items" for extras

**💡 Ideas Tab**
- Browse AI-generated trip ideas
- Click "Generate New Ideas" for more
- Save your favorites

**🤖 AI Assistant Tab**
- Ask questions like:
  - "What should we pack for weather?"
  - "Best dining for a 5-year-old?"
  - "Tips for first-time visitors?"

**📋 Trip Summary Tab**
- See your planning progress
- Track completed tasks

---

## Example Questions to Ask the AI

- "What are some hidden gems at Magic Kingdom?"
- "How can we save money on food?"
- "What time should we get to the park?"
- "Best rides for a 3-year-old?"
- "Is Genie+ worth it for our trip?"
- "What should we do on a rainy day?"
- "Character dining recommendations?"
- "Best spots for fireworks?"

---

## Tips for Best Results

✨ **Be specific about ages** - The AI tailors suggestions for your party

✨ **Update as trip approaches** - Regenerate checklist for time-sensitive items

✨ **Use the chat** - The AI knows A LOT about Disney parks

✨ **Check forgotten items** - Catches things you might miss

✨ **Try different idea focuses** - Generate ideas for dining, activities, photos, etc.

---

## Sharing with Family

**Want family members to access it too?**

**Option A: Local Access**
- They need to be on same WiFi network
- Share your computer's IP address and port (shown in terminal)

**Option B: Online Deployment** (Recommended)
- Deploy to Streamlit Cloud (free!)
- Everyone gets a web link
- Access from any device, anywhere
- See `DEPLOYMENT_GUIDE.md` for instructions

---

## Troubleshooting

**"OpenAI API key not found"**
- Check that your `.env` file exists and has the correct key
- Make sure there are no extra spaces around the key

**"Module not found"**
- Run: `pip install -r requirements.txt` again
- Make sure you're in the Disney-Agent folder

**App won't start**
- Check Python version: `python --version` (need 3.8+)
- Try: `python -m streamlit run app.py`

**Too slow/expensive**
- Edit `.env` and change to cheaper model:
  ```
  OPENAI_MODEL=gpt-3.5-turbo
  ```

---

## What's Next?

1. **Create your first trip plan!**
2. **Customize** the checklist with your own items
3. **Ask the AI** all your Disney questions
4. **Share** with family members planning with you
5. **Deploy online** for access anywhere (see DEPLOYMENT_GUIDE.md)

---

## Cost Estimate

**Typical planning session:**
- Generating checklist: ~$0.01
- Generating ideas: ~$0.01-0.02
- Chat messages: ~$0.001 each
- **Total for complete trip planning: $0.10-0.50**

Much cheaper than a Disney guidebook! 😄

---

## Support

Questions? Check:
- `README.md` - Full documentation
- `DEPLOYMENT_GUIDE.md` - Publishing options
- GitHub Issues - Report bugs or ask for help

---

**Happy Planning! Your magical Disney adventure awaits! 🏰✨**
