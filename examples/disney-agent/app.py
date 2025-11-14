"""
Disney Trip Planning Agent - Streamlit Web Application
A beautiful, user-friendly interface for planning your magical Disney vacation

ARCHITECTURE:
- Modular design with separated concerns
- Configuration-driven prompts and constants
- Structured logging and error handling
- Reusable UI components
"""
import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import pytz
import pickle
from pathlib import Path

# Core modules
from src.agents.trip_planner_agent import TripPlannerAgent
from src.models.trip_data import TripDetails, ChecklistItem, IdeaSuggestion
from src.utils.helpers import calculate_countdown, format_countdown, get_trip_phase
from src.utils.firebase_config import get_firebase_manager

# New modular architecture
from src.ui.styles import apply_custom_styles
from src.config.constants import (
    MAX_CHAT_HISTORY, MAX_IDEAS, MAX_PENDING_SUGGESTIONS,
    DATA_DIR, DATA_FILE, EMOJI, CHECKLIST_CATEGORIES,
    IDEA_CATEGORIES, PRIORITY_LEVELS
)
from src.utils.logger import (
    log_info, log_error, log_warning,
    show_error, show_warning, show_info, show_success,
    safe_execute
)

# Load environment variables
load_dotenv()

# Log application start
log_info("Disney Trip Planner application starting")

# Page configuration
st.set_page_config(
    page_title=f"{EMOJI['castle']} Disney Trip Planner",
    page_icon=EMOJI['castle'],
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles from modular UI component
log_info("Applying custom Disney castle theme")
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# Constants now imported from src.config.constants

# Data persistence functions

def save_trip_data():
    """Save trip data to Firebase and local disk"""
    # Limit chat history size to conserve memory
    chat_history = st.session_state.chat_history
    if len(chat_history) > MAX_CHAT_HISTORY:
        chat_history = chat_history[-MAX_CHAT_HISTORY:]  # Keep only last 50 messages
        st.session_state.chat_history = chat_history

    # Limit ideas list to conserve memory
    ideas = st.session_state.ideas
    if len(ideas) > MAX_IDEAS:
        ideas = ideas[-MAX_IDEAS:]  # Keep only last 30 ideas
        st.session_state.ideas = ideas

    # Limit pending suggestions to conserve memory
    pending_suggestions = st.session_state.get('pending_suggestions', [])
    if len(pending_suggestions) > MAX_PENDING_SUGGESTIONS:
        pending_suggestions = pending_suggestions[-MAX_PENDING_SUGGESTIONS:]
        st.session_state.pending_suggestions = pending_suggestions

    data = {
        'trip_details': st.session_state.trip_details,
        'checklist': st.session_state.checklist,
        'ideas': ideas,
        'chat_history': chat_history,
        'rejected_items': st.session_state.get('rejected_items', set()),
        'pending_suggestions': pending_suggestions
    }

    # Try Firebase first if trip code is set
    trip_code = st.session_state.get('trip_code')
    if trip_code:
        firebase = get_firebase_manager()
        if firebase.is_enabled():
            try:
                firebase.save_trip(trip_code, data)
            except Exception as e:
                pass  # Fail silently to avoid UI clutter

    # Always save locally as backup (but don't if it fails)
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)
    except Exception:
        pass  # Fail silently

def load_trip_data(trip_code: str = None):
    """Load trip data from Firebase or local disk"""
    # Try Firebase first if trip code is provided
    if trip_code:
        firebase = get_firebase_manager()
        if firebase.is_enabled():
            try:
                data = firebase.load_trip(trip_code)
                if data:
                    return data
            except Exception as e:
                st.warning(f"Could not load from cloud: {e}")

    # Fall back to local storage
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'rb') as f:
                data = pickle.load(f)
                return data
    except Exception as e:
        st.warning(f"Could not load locally: {e}")

    return None

# Get API key from Streamlit secrets or environment
def get_api_key():
    """Get API key from secrets or environment"""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        if 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
    except:
        pass

    # Fall back to environment variable (for local)
    return os.getenv('OPENAI_API_KEY')

# Initialize session state
if 'agent' not in st.session_state:
    api_key = get_api_key()
    if api_key:
        st.session_state.agent = TripPlannerAgent(api_key)
    else:
        st.session_state.agent = None

if 'trip_details' not in st.session_state:
    # Try to load saved data
    saved_data = load_trip_data()
    if saved_data:
        st.session_state.trip_details = saved_data.get('trip_details')
        st.session_state.checklist = saved_data.get('checklist', [])

        # Limit loaded data to conserve memory
        ideas = saved_data.get('ideas', [])
        st.session_state.ideas = ideas[-MAX_IDEAS:] if len(ideas) > MAX_IDEAS else ideas

        chat_history = saved_data.get('chat_history', [])
        st.session_state.chat_history = chat_history[-MAX_CHAT_HISTORY:] if len(chat_history) > MAX_CHAT_HISTORY else chat_history

        # Ensure rejected_items is always a set (Firebase returns it as a list)
        rejected = saved_data.get('rejected_items', set())
        st.session_state.rejected_items = set(rejected) if isinstance(rejected, (list, set)) else set()

        pending_suggestions = saved_data.get('pending_suggestions', [])
        st.session_state.pending_suggestions = pending_suggestions[-MAX_PENDING_SUGGESTIONS:] if len(pending_suggestions) > MAX_PENDING_SUGGESTIONS else pending_suggestions
    else:
        st.session_state.trip_details = None
        st.session_state.checklist = []
        st.session_state.ideas = []
        st.session_state.chat_history = []
        st.session_state.rejected_items = set()
        st.session_state.pending_suggestions = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = []

if 'ideas' not in st.session_state:
    st.session_state.ideas = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'rejected_items' not in st.session_state:
    st.session_state.rejected_items = set()
else:
    # Ensure it's always a set, even if it somehow became a list
    if not isinstance(st.session_state.rejected_items, set):
        st.session_state.rejected_items = set(st.session_state.rejected_items)

if 'pending_suggestions' not in st.session_state:
    st.session_state.pending_suggestions = []


def main():
    """Main application"""
    # Header
    st.markdown('<h1 class="main-header">🏰 Disney Trip Planning Agent ✨</h1>', unsafe_allow_html=True)

    # Check for API key
    if not st.session_state.agent:
        st.error("⚠️ OpenAI API key not configured!")
        st.info("The API key should be configured in Streamlit Cloud secrets or your .env file")
        st.markdown("""
        **For Streamlit Cloud:** Add `OPENAI_API_KEY` in your app settings → Secrets

        **For Local:** Create a `.env` file with `OPENAI_API_KEY=your_key_here`
        """)
        return

    # Trip Code Setup - Multi-User Collaboration
    if 'trip_code' not in st.session_state:
        st.session_state.trip_code = None

    # Show trip code input if not set or if user wants to change
    if not st.session_state.trip_code:
        st.markdown("---")
        st.subheader("🔐 Trip Code for Multi-User Collaboration")
        st.info("💡 **Share your trip with family and friends!** Enter a trip code to collaborate on planning together. Everyone with the same code can view and edit the trip.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Create New Trip**")
            new_trip_code = st.text_input(
                "Enter your trip code",
                value="",
                max_chars=50,
                placeholder="e.g., 'Ohboy' or 'DisneyDreams'",
                help="This code will be shared with your travel companions"
            )

            if st.button("🎉 Create New Trip", use_container_width=True):
                if new_trip_code and len(new_trip_code) >= 3:
                    firebase = get_firebase_manager()
                    if firebase.is_enabled():
                        if firebase.trip_exists(new_trip_code):
                            st.error(f"❌ Trip code '{new_trip_code}' already exists! Use 'Join Existing Trip' instead.")
                        else:
                            st.session_state.trip_code = new_trip_code
                            st.success(f"✅ Created trip with code: **{new_trip_code}**")
                            st.info("🔗 Share this code with your travel companions so they can join!")
                            st.rerun()
                    else:
                        # Firebase not configured - use local only
                        st.session_state.trip_code = new_trip_code
                        st.warning("⚠️ Cloud sync not configured. Trip will be saved locally only.")
                        st.rerun()
                else:
                    st.error("Trip code must be at least 3 characters long")

        with col2:
            st.markdown("**Join Existing Trip**")
            join_trip_code = st.text_input(
                "Enter trip code to join",
                value="",
                max_chars=50,
                placeholder="Enter your friend's trip code",
                help="Get this code from your travel companion"
            )

            if st.button("🤝 Join Trip", use_container_width=True):
                if join_trip_code:
                    firebase = get_firebase_manager()
                    if firebase.is_enabled():
                        if firebase.trip_exists(join_trip_code):
                            st.session_state.trip_code = join_trip_code
                            # Load the trip data
                            trip_data = load_trip_data(join_trip_code)
                            if trip_data:
                                st.session_state.trip_details = trip_data.get('trip_details')
                                st.session_state.checklist = trip_data.get('checklist', [])
                                st.session_state.ideas = trip_data.get('ideas', [])
                                st.session_state.chat_history = trip_data.get('chat_history', [])
                                # Ensure rejected_items is always a set (Firebase returns it as a list)
                                rejected = trip_data.get('rejected_items', set())
                                st.session_state.rejected_items = set(rejected) if isinstance(rejected, (list, set)) else set()
                                st.session_state.pending_suggestions = trip_data.get('pending_suggestions', [])
                            st.success(f"✅ Joined trip: **{join_trip_code}**")
                            st.rerun()
                        else:
                            st.error(f"❌ Trip code '{join_trip_code}' not found!")
                    else:
                        st.error("⚠️ Cloud sync not configured. Cannot join remote trips.")
                else:
                    st.error("Please enter a trip code")

        st.markdown("---")
        return

    # Display current trip code - DIAMOND SHAPE!
    st.markdown(f"""
    <div class="trip-code-diamond">
        <h3>💎 Trip Code: {st.session_state.trip_code} 💎</h3>
        <p>Share this code with your travel companions!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Change Trip Code"):
            st.session_state.trip_code = None
            st.rerun()

    # Sidebar - Trip Setup
    with st.sidebar:
        st.header("🎯 Your Trip Details")

        # Load saved values if available
        default_destination = st.session_state.trip_details.destination if st.session_state.trip_details else "Walt Disney World"
        default_start = st.session_state.trip_details.start_date.date() if st.session_state.trip_details else datetime.now().date() + timedelta(days=90)
        default_end = st.session_state.trip_details.end_date.date() if st.session_state.trip_details else datetime.now().date() + timedelta(days=94)
        default_party = st.session_state.trip_details.party_size if st.session_state.trip_details else 4
        default_ages = ", ".join(map(str, st.session_state.trip_details.ages)) if st.session_state.trip_details else "8, 10, 35, 37"
        default_interests = st.session_state.trip_details.interests if st.session_state.trip_details else ["Character Meet & Greets", "Fireworks & Parades"]
        default_budget = st.session_state.trip_details.budget_range if st.session_state.trip_details else "Moderate"
        default_needs = st.session_state.trip_details.special_needs if st.session_state.trip_details else []

        destination = st.selectbox(
            "Destination",
            ["Walt Disney World", "Disneyland Resort", "Disneyland Paris",
             "Tokyo Disney Resort", "Hong Kong Disneyland", "Shanghai Disney Resort"],
            index=["Walt Disney World", "Disneyland Resort", "Disneyland Paris",
                   "Tokyo Disney Resort", "Hong Kong Disneyland", "Shanghai Disney Resort"].index(default_destination)
        )

        trip_date = st.date_input(
            "Trip Start Date",
            value=default_start,
            min_value=datetime.now().date()
        )

        trip_end_date = st.date_input(
            "Trip End Date",
            value=default_end,
            min_value=trip_date
        )

        party_size = st.number_input("Party Size", min_value=1, max_value=20, value=default_party)

        ages_input = st.text_input("Ages (comma-separated)", default_ages)
        ages = [int(age.strip()) for age in ages_input.split(',') if age.strip().isdigit()]

        interests = st.multiselect(
            "Interests",
            ["Thrill Rides", "Character Meet & Greets", "Shows & Entertainment",
             "Dining Experiences", "Shopping", "Relaxation", "Photography",
             "Fireworks & Parades", "Water Parks", "Resort Activities"],
            default=default_interests
        )

        budget = st.selectbox(
            "Budget Range",
            ["Budget-Friendly", "Moderate", "Deluxe", "No Budget Constraints"],
            index=["Budget-Friendly", "Moderate", "Deluxe", "No Budget Constraints"].index(default_budget)
        )

        special_needs = st.multiselect(
            "Special Considerations",
            ["Wheelchair Access", "Dietary Restrictions", "First-Time Visitors",
             "Celebrating Special Occasion", "Traveling with Toddlers", "Traveling with Teens"],
            default=default_needs
        )

        if st.button("🚀 Create/Update Trip Plan", use_container_width=True):
            with st.spinner("Creating your magical trip plan..."):
                # Convert dates to datetime
                start_dt = datetime.combine(trip_date, datetime.min.time())
                end_dt = datetime.combine(trip_end_date, datetime.min.time())
                start_dt = pytz.UTC.localize(start_dt)
                end_dt = pytz.UTC.localize(end_dt)

                st.session_state.trip_details = TripDetails(
                    destination=destination,
                    start_date=start_dt,
                    end_date=end_dt,
                    party_size=party_size,
                    ages=ages,
                    interests=interests,
                    budget_range=budget,
                    special_needs=special_needs
                )

                # Generate checklist
                st.session_state.checklist = st.session_state.agent.generate_comprehensive_checklist(
                    st.session_state.trip_details
                )

                # Generate initial ideas
                st.session_state.ideas = st.session_state.agent.brainstorm_ideas(
                    st.session_state.trip_details
                )

                # Save data
                save_trip_data()

                st.success("✅ Trip plan created and saved!")
                st.rerun()

    # Main content
    if not st.session_state.trip_details:
        st.info("👈 Start by entering your trip details in the sidebar and click 'Create Trip Plan'")
        st.markdown("""
        ### Welcome to Your Disney Trip Planning Agent! 🎉

        This AI-powered assistant will help you with:
        - ✅ **Comprehensive packing checklists** (never forget the essentials!)
        - 💡 **Creative trip ideas** and suggestions
        - ⏰ **Countdown timer** to your magical adventure
        - 🤖 **AI assistant** for all your Disney questions

        ### 💾 Your Trip is Always Saved!
        - **Everything is saved automatically** - trip details, checklists, checked items, chat history
        - **Come back anytime** - your trip will be right here waiting for you
        - **No login needed** - your data is securely saved on your device
        - **Close and reopen** - everything will be exactly as you left it!
        """)
        return

    # Countdown Timer
    st.markdown("---")
    days, hours, minutes, seconds = calculate_countdown(st.session_state.trip_details.start_date)
    countdown_text = format_countdown(days, hours, minutes, seconds)

    st.markdown(f"""
    <div class="countdown-box">
        ⏰ {countdown_text} until your magical adventure! 🎉
    </div>
    """, unsafe_allow_html=True)

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "✅ Checklists",
        "💡 Ideas & Suggestions",
        "🤖 AI Assistant",
        "📋 Trip Summary"
    ])

    # Tab 1: Checklists
    with tab1:
        st.header("Trip Planning Checklist")

        # Top row: Subheader on left, Add Custom Item on right - MOBILE OPTIMIZED
        top_col1, top_col2 = st.columns([3, 2])
        with top_col1:
            st.subheader("Your Personalized Checklist")
        with top_col2:
            # Add custom item - compact version
            with st.expander("➕ Add Item", expanded=False):
                new_item_text = st.text_input("Item description", key="new_item", placeholder="e.g., Pack sunscreen")
                new_col1, new_col2 = st.columns(2)
                with new_col1:
                    new_item_category = st.text_input("Category", "custom", key="new_category")
                with new_col2:
                    new_item_priority = st.selectbox("Priority", ["high", "medium", "low"], key="new_priority")

                if st.button("Add to Checklist", use_container_width=True) and new_item_text:
                    from src.utils.helpers import generate_checklist_id
                    new_item = ChecklistItem(
                        id=generate_checklist_id(),
                        text=new_item_text,
                        category=new_item_category,
                        priority=new_item_priority,
                        completed=False
                    )
                    st.session_state.checklist.append(new_item)
                    save_trip_data()
                    st.success(f"✅ Added: {new_item_text}")
                    st.rerun()

        # Action buttons row - MOBILE OPTIMIZED (simplified layout)
        if st.button("🔍 Find Forgotten Items", use_container_width=True):
            with st.spinner("Analyzing checklist..."):
                # Get AI suggestions
                forgotten = st.session_state.agent.suggest_forgotten_items(
                    st.session_state.checklist
                )

                if forgotten:
                    # Get current checklist item texts (lowercase for comparison)
                    existing_items = {item.text.lower().strip() for item in st.session_state.checklist}

                    # Filter out duplicates and rejected items
                    new_items = []
                    for item_text in forgotten:
                        item_lower = item_text.lower().strip()
                        if item_lower not in existing_items and item_lower not in st.session_state.rejected_items:
                            new_items.append(item_text)

                    if new_items:
                        # Add new items to checklist
                        from src.utils.helpers import generate_checklist_id
                        for item_text in new_items:
                            new_item = ChecklistItem(
                                id=generate_checklist_id(),
                                text=item_text,
                                category="forgotten-items",
                                priority="medium",
                                completed=False
                            )
                            st.session_state.checklist.append(new_item)

                        # Save data
                        save_trip_data()

                        st.success(f"✅ Added {len(new_items)} forgotten item{'s' if len(new_items) != 1 else ''} to your checklist!")
                        st.rerun()
                    else:
                        st.info("✨ Great job! You haven't forgotten anything important.")

        # Collapsible Filter options - EASY TO FIND
        with st.expander("🔍 Filters", expanded=False):
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            with filter_col1:
                show_completed = st.checkbox("Show Completed", value=True)
            with filter_col2:
                priority_filter = st.multiselect(
                    "Filter by Priority",
                    ["high", "medium", "low"],
                    default=["high", "medium", "low"]
                )
            with filter_col3:
                category_filter = st.multiselect(
                    "Filter by Category",
                    list(set([item.category for item in st.session_state.checklist])),
                    default=list(set([item.category for item in st.session_state.checklist]))
                )

        # Display checklist - 3 Cards Per Row Grid
        filtered_items = []
        for idx, item in enumerate(st.session_state.checklist):
            if not show_completed and item.completed:
                continue
            if item.priority not in priority_filter:
                continue
            if item.category not in category_filter:
                continue
            filtered_items.append((idx, item))

        # Display in rows of 3
        for row_idx in range(0, len(filtered_items), 3):
            cols = st.columns(3)

            for col_idx in range(3):
                if row_idx + col_idx < len(filtered_items):
                    idx, item = filtered_items[row_idx + col_idx]

                    with cols[col_idx]:
                        completed_class = "completed" if item.completed else ""
                        priority_class = f"priority-{item.priority}"

                        # Card with checkbox inside
                        st.markdown(f"""
                        <div class="checklist-card {completed_class} {priority_class}">
                            <div class="checklist-card-content">
                                <strong>{item.text}</strong>
                                <small>📁 {item.category} | ⭐ {item.priority.upper()}
                                {f"| 📅 {item.deadline}" if item.deadline else ""}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Checkbox and delete button below the card - wrapped for proper layout
                        st.markdown('<div class="card-action-row">', unsafe_allow_html=True)

                        action_col1, action_col2 = st.columns([7, 1], gap="small")
                        with action_col1:
                            checked = st.checkbox(
                                "Complete",
                                value=item.completed,
                                key=f"check_{idx}",
                                label_visibility="visible"
                            )
                            if checked != item.completed:
                                st.session_state.checklist[idx].completed = checked
                                save_trip_data()

                        with action_col2:
                            st.markdown('<div class="card-delete-btn">', unsafe_allow_html=True)
                            if st.button("🗑️", key=f"delete_{idx}", use_container_width=False):
                                deleted_text = st.session_state.checklist[idx].text.lower().strip()
                                st.session_state.rejected_items.add(deleted_text)
                                st.session_state.checklist.pop(idx)
                                save_trip_data()
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: Ideas & Suggestions
    with tab2:
        st.header("💡 Trip Ideas & Suggestions")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Brainstormed Ideas for Your Trip")
        with col2:
            focus = st.selectbox(
                "Focus",
                ["general", "dining", "activities", "surprises", "budget-friendly", "photos"]
            )
            if st.button("🔄 Generate New Ideas"):
                with st.spinner("Brainstorming magical ideas..."):
                    new_ideas = st.session_state.agent.brainstorm_ideas(
                        st.session_state.trip_details,
                        focus=focus
                    )
                    st.session_state.ideas.extend(new_ideas)
                    save_trip_data()
                    st.rerun()

        # Display ideas
        for idx, idea in enumerate(st.session_state.ideas):
            st.markdown(f"""
            <div class="idea-card">
                <h3>{idea.title}</h3>
                <p>{idea.description}</p>
                <small>🏷️ {idea.category} | Tags: {', '.join(idea.tags)}</small>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([6, 1])
            with col2:
                if st.button("💾" if not idea.saved else "❤️", key=f"save_idea_{idx}"):
                    st.session_state.ideas[idx].saved = not idea.saved
                    save_trip_data()
                    st.rerun()

    # Tab 3: AI Assistant
    with tab3:
        st.header("🤖 AI Trip Planning Assistant")
        st.write("Ask me anything about your Disney trip!")
        st.info("💡 **Pro tip:** I can help you add items to your checklist! Just tell me what you need to remember, or I'll proactively suggest items based on our conversation.")

        # Chat interface
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Display any pending suggested items from the last AI response
        if 'pending_suggestions' in st.session_state and st.session_state.pending_suggestions:
            st.markdown("---")
            st.markdown("### ✨ Suggested Checklist Items")
            st.write("The AI assistant has some suggestions for your checklist:")

            for idx, suggestion in enumerate(st.session_state.pending_suggestions):
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    emoji = priority_emoji.get(suggestion.get('priority', 'medium'), '🟡')
                    st.markdown(f"{emoji} **{suggestion['text']}**")
                    st.caption(f"Category: {suggestion['category']} | Priority: {suggestion['priority']}")
                with col2:
                    if st.button("➕ Add", key=f"add_suggestion_{idx}"):
                        # Add to checklist
                        from src.utils.helpers import generate_checklist_id
                        new_item = ChecklistItem(
                            id=generate_checklist_id(),
                            text=suggestion['text'],
                            category=suggestion['category'],
                            priority=suggestion['priority'],
                            completed=False
                        )
                        st.session_state.checklist.append(new_item)

                        # Remove this suggestion from pending
                        st.session_state.pending_suggestions.pop(idx)

                        # Save data
                        save_trip_data()

                        st.success(f"✅ Added '{suggestion['text']}' to your checklist!")
                        st.rerun()
                with col3:
                    if st.button("❌ Skip", key=f"skip_suggestion_{idx}"):
                        # Add to rejected items
                        rejected_text = suggestion['text'].lower().strip()
                        st.session_state.rejected_items.add(rejected_text)

                        # Remove this suggestion from pending
                        st.session_state.pending_suggestions.pop(idx)

                        # Save data
                        save_trip_data()
                        st.rerun()

            if st.button("❌ Skip All Suggestions"):
                # Add all to rejected items
                for suggestion in st.session_state.pending_suggestions:
                    rejected_text = suggestion['text'].lower().strip()
                    st.session_state.rejected_items.add(rejected_text)

                st.session_state.pending_suggestions = []
                save_trip_data()
                st.rerun()

            st.markdown("---")

        # User input
        user_question = st.chat_input("Ask a question about your trip...")

        if user_question:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # Get AI response
            with st.spinner("Thinking..."):
                response = st.session_state.agent.get_personalized_suggestion(
                    st.session_state.trip_details,
                    user_question
                )

            # Parse response for suggested items
            from src.agents.trip_planner_agent import TripPlannerAgent
            cleaned_response, suggested_items = TripPlannerAgent.parse_item_suggestions(response)

            # Filter out duplicates and rejected items
            if suggested_items:
                existing_items = {item.text.lower().strip() for item in st.session_state.checklist}
                filtered_suggestions = []

                for suggestion in suggested_items:
                    suggestion_lower = suggestion['text'].lower().strip()
                    if suggestion_lower not in existing_items and suggestion_lower not in st.session_state.rejected_items:
                        filtered_suggestions.append(suggestion)

                # Store filtered suggestions in session state
                st.session_state.pending_suggestions = filtered_suggestions

            # Add cleaned assistant message (without [ADD_ITEM...] tags)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": cleaned_response
            })

            # Save chat history
            save_trip_data()

            st.rerun()

    # Tab 4: Trip Summary
    with tab4:
        st.header("📋 Trip Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Trip Details")
            st.write(f"**Destination:** {st.session_state.trip_details.destination}")
            st.write(f"**Start Date:** {st.session_state.trip_details.start_date.strftime('%B %d, %Y')}")
            st.write(f"**End Date:** {st.session_state.trip_details.end_date.strftime('%B %d, %Y')}")
            trip_length = (st.session_state.trip_details.end_date - st.session_state.trip_details.start_date).days
            st.write(f"**Trip Length:** {trip_length} days")
            st.write(f"**Party Size:** {st.session_state.trip_details.party_size}")
            st.write(f"**Ages:** {', '.join(map(str, st.session_state.trip_details.ages))}")

        with col2:
            st.subheader("Planning Progress")
            total_items = len(st.session_state.checklist)
            completed_items = sum(1 for item in st.session_state.checklist if item.completed)
            progress = (completed_items / total_items * 100) if total_items > 0 else 0

            st.metric("Checklist Progress", f"{progress:.0f}%")
            st.progress(progress / 100)

            st.metric("Total Tasks", total_items)
            st.metric("Completed", completed_items)
            st.metric("Remaining", total_items - completed_items)

        st.markdown("---")
        st.subheader("Interests & Preferences")
        st.write(f"**Interests:** {', '.join(st.session_state.trip_details.interests)}")
        st.write(f"**Budget:** {st.session_state.trip_details.budget_range}")
        if st.session_state.trip_details.special_needs:
            st.write(f"**Special Considerations:** {', '.join(st.session_state.trip_details.special_needs)}")

        st.markdown("---")
        st.subheader("Data Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Trip Data"):
                save_trip_data()
                st.success("Trip data saved!")
        with col2:
            if st.button("🗑️ Clear All Data"):
                st.session_state.trip_details = None
                st.session_state.checklist = []
                st.session_state.ideas = []
                st.session_state.chat_history = []
                if DATA_FILE.exists():
                    DATA_FILE.unlink()
                st.success("All data cleared!")
                st.rerun()


if __name__ == "__main__":
    main()
