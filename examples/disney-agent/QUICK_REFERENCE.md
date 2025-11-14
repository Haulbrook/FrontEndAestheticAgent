# 🚀 Disney Trip Planner - Quick Reference Guide

## 5-Minute Start Guide

### Local Development
```bash
# 1. Clone and setup
git clone https://github.com/Haulbrook/Disney-Agent.git
cd Disney-Agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Add API key
echo "OPENAI_API_KEY=sk-proj-YOUR_KEY" > .env

# 3. Run
streamlit run app.py
```

### Adding a New Checklist Category
```python
# In src/agents/trip_planner_agent.py, update prompt:
categories = [
    "planning",
    "packing",
    "day-of",
    "during-trip",
    "your-new-category"  # Add here
]
```

### Changing Theme Colors
```css
/* In app.py, lines ~31-1032, update: */
--primary-light: #87ceeb  /* Change this */
--accent-light: #ffb6c1   /* And this */
```

### Adding a New Tab
```python
# In app.py, around line 1165:
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✅ Checklists",
    "💡 Ideas",
    "🤖 AI Assistant",
    "📋 Trip Summary",
    "🎯 Your New Tab"  # Add here
])

# Then implement:
with tab5:
    st.header("Your New Feature")
    # Your code here
```

## CSS Cheat Sheet

### Making Something Circular
```css
.my-element {
    width: 100px !important;
    height: 100px !important;
    border-radius: 50% !important;  /* Key! */
}
```

### Making Something Pill-Shaped
```css
.my-button {
    border-radius: 50px !important;  /* Large radius */
    padding: 16px 40px !important;
}
```

### Adding Sparkle Animation
```css
.sparkly::before {
    content: '✨';
    animation: sparkle 2s infinite;
}

@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0); }
    50% { opacity: 1; transform: scale(1); }
}
```

### Overriding Streamlit Styles
```css
/* Always target the wrapper */
[data-testid="column"] {
    your-property: value !important;
}

/* For buttons */
.stButton>button {
    your-property: value !important;
}
```

## Common Tasks

### Add New AI Suggestion Type
```python
# 1. In src/agents/trip_planner_agent.py
def suggest_restaurants(self, trip_details: TripDetails) -> List[str]:
    prompt = f"""Suggest 5 restaurants for {trip_details.destination}..."""
    response = self.client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.split('\n')

# 2. In app.py, add button in ideas tab
if st.button("🍽️ Get Restaurant Ideas"):
    restaurants = st.session_state.agent.suggest_restaurants(st.session_state.trip_details)
    # Display restaurants
```

### Add New Filter Option
```python
# In app.py, checklist tab section:
with filter_col4:  # Add new column
    your_filter = st.multiselect(
        "Your Filter Name",
        ["Option 1", "Option 2"],
        default=["Option 1", "Option 2"]
    )

# In display loop:
if item.your_property not in your_filter:
    continue  # Skip this item
```

### Save Custom Data to Firebase
```python
# Add to session state
st.session_state.my_custom_data = [...]

# In save_trip_data() function:
data = {
    'trip_details': st.session_state.trip_details,
    'checklist': st.session_state.checklist,
    'my_custom_data': st.session_state.my_custom_data  # Add this
}

# In load_trip_data():
st.session_state.my_custom_data = data.get('my_custom_data', [])
```

## Debugging Commands

### Check Python Syntax
```bash
python3 -m py_compile app.py
```

### Test Imports
```bash
python3 -c "from src.agents.trip_planner_agent import TripPlannerAgent; print('OK')"
```

### Find CSS Line
```bash
grep -n "checklist-card" app.py
```

### Check Firebase Status
```python
# In app.py, add temporarily:
firebase = get_firebase_manager()
st.write(f"Firebase enabled: {firebase.is_enabled()}")
```

## Component Copy-Paste Templates

### New Button with Animation
```python
st.markdown("""
<style>
.my-btn>button {
    background: linear-gradient(135deg, #87ceeb 0%, #5dade2 100%) !important;
    border-radius: 50px !important;
    padding: 16px 40px !important;
    transition: all 0.3s ease !important;
}
.my-btn>button:hover {
    transform: scale(1.1) !important;
    animation: shimmy 0.5s ease-in-out !important;
}
</style>
<div class="my-btn">
""", unsafe_allow_html=True)

if st.button("✨ My Button"):
    # Your code

st.markdown('</div>', unsafe_allow_html=True)
```

### New Card Component
```python
st.markdown("""
<div style="
    border-radius: 20px;
    padding: 30px;
    background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
    border: 3px solid #87ceeb;
    box-shadow: 0 8px 20px rgba(135, 206, 235, 0.3);
    margin: 20px 0;
">
    <h3>Card Title</h3>
    <p>Card content goes here...</p>
</div>
""", unsafe_allow_html=True)
```

### New Checkbox Action Row
```python
st.markdown('<div class="card-action-row">', unsafe_allow_html=True)

col1, col2 = st.columns([7, 1], gap="small")
with col1:
    checked = st.checkbox("Label", key="unique_key")

with col2:
    st.markdown('<div class="card-delete-btn">', unsafe_allow_html=True)
    if st.button("🗑️", key="delete_key"):
        # Delete action
        pass
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```

## Git Workflow

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

### Deploy to Streamlit Cloud
```bash
# 1. Push to GitHub
git push origin your-branch-name

# 2. In Streamlit Cloud:
# - Change branch to your-branch-name
# - Click "Reboot app"
# - Wait 2-3 minutes
```

### Rollback to Working Version
```bash
# Find working commit
git log --oneline

# Deploy specific commit
# In Streamlit Cloud: Settings → Branch: commit-hash
```

## Troubleshooting Shortcuts

| Issue | Quick Fix |
|-------|-----------|
| CSS not applying | Add `!important`, check line order |
| Button overlap | Verify `[7, 1]` ratio, check wrapper div |
| Mickey Ears missing | Add `appearance: none !important` |
| Firebase not syncing | Check secrets, verify credentials |
| Spinning forever | Check logs, clear cache + reboot |
| Set/List error | Add `set()` conversion after loading |

## File Locations

| What | Where |
|------|-------|
| Main app | `app.py` |
| CSS styling | `app.py` lines 31-1032 |
| Checklist grid | `app.py` lines ~1450-1520 |
| AI agent | `src/agents/trip_planner_agent.py` |
| Data models | `src/models/trip_data.py` |
| Firebase | `src/utils/firebase_config.py` |
| Helpers | `src/utils/helpers.py` |
| Dependencies | `requirements.txt` |
| Secrets | `.streamlit/secrets.toml` (deployment) |

## Emergency Contacts

**Full Documentation:** `HANDOFF_PACKET.md`

**Firebase Setup:** `FIREBASE_SETUP.md`

**Streamlit Docs:** https://docs.streamlit.io/

**OpenAI Docs:** https://platform.openai.com/docs/

---

**💡 Tip:** Bookmark this file for quick reference while coding!
