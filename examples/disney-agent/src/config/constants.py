"""
Application Constants for Disney Trip Planner
Centralized configuration for app-wide settings
"""
from pathlib import Path

# ============================================================================
# MEMORY LIMITS (Critical for Streamlit Cloud free tier - 1GB RAM)
# ============================================================================
MAX_CHAT_HISTORY = 50           # Max chat messages to retain
MAX_IDEAS = 30                   # Max idea suggestions to retain
MAX_PENDING_SUGGESTIONS = 20     # Max pending AI suggestions

# ============================================================================
# FILE PATHS
# ============================================================================
DATA_DIR = Path.home() / '.disney_trip_planner'
DATA_FILE = DATA_DIR / 'trip_data.pkl'

# ============================================================================
# OPENAI CONFIGURATION
# ============================================================================
DEFAULT_MODEL = "gpt-4-turbo-preview"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 2000

# ============================================================================
# UI THEME COLORS (Soft Princess Disney Aesthetic)
# ============================================================================
THEME_COLORS = {
    'sky_blue': '#87CEEB',
    'silver': '#C0C0C0',
    'pastel_pink': '#FFB6C1',
    'soft_purple': '#E6E6FA',
    'cream': '#FFF8DC',
    'gold': '#FFD700',
    'light_gold': '#FFF4CC',
}

# ============================================================================
# FONTS
# ============================================================================
HEADER_FONT = 'Cinzel'
BODY_FONT = 'Cormorant Garamond'

# ============================================================================
# CHECKLIST CATEGORIES
# ============================================================================
CHECKLIST_CATEGORIES = [
    "General",
    "Documents",
    "Clothing",
    "Toiletries",
    "Electronics",
    "Park Essentials",
    "Comfort Items",
    "Special Items"
]

# ============================================================================
# IDEA CATEGORIES
# ============================================================================
IDEA_CATEGORIES = [
    "dining",
    "activities",
    "photos",
    "surprises",
    "tips"
]

# ============================================================================
# PRIORITY LEVELS
# ============================================================================
PRIORITY_LEVELS = ["low", "medium", "high"]

# ============================================================================
# DISNEY DESTINATIONS
# ============================================================================
DISNEY_DESTINATIONS = [
    "Walt Disney World (Florida)",
    "Disneyland Resort (California)",
    "Disneyland Paris",
    "Tokyo Disney Resort",
    "Hong Kong Disneyland",
    "Shanghai Disneyland"
]

# ============================================================================
# INTERESTS/PREFERENCES
# ============================================================================
INTEREST_OPTIONS = [
    "Thrill rides",
    "Character meet & greets",
    "Shows and entertainment",
    "Dining experiences",
    "Photography",
    "Shopping",
    "Relaxation",
    "Educational experiences"
]

# ============================================================================
# SPECIAL NEEDS OPTIONS
# ============================================================================
SPECIAL_NEEDS_OPTIONS = [
    "Wheelchair accessibility",
    "Dietary restrictions",
    "Sensory sensitivities",
    "Medical needs",
    "Language assistance"
]

# ============================================================================
# EMOJI CONSTANTS (Consistent visual language)
# ============================================================================
EMOJI = {
    'castle': '🏰',
    'sparkle': '✨',
    'check': '✅',
    'party': '🎉',
    'idea': '💡',
    'chat': '💬',
    'calendar': '📅',
    'clock': '⏰',
    'star': '⭐',
    'magic': '🪄',
    'fireworks': '🎆',
    'search': '🔍',
    'plus': '➕',
    'trash': '🗑️',
    'save': '💾',
    'download': '⬇️',
    'share': '🔗',
    'warning': '⚠️',
    'info': 'ℹ️'
}

# ============================================================================
# TRIP PHASES (for contextual messaging)
# ============================================================================
TRIP_PHASES = {
    'early': 90,      # More than 90 days away
    'mid': 30,        # 30-90 days away
    'final': 7,       # 7-30 days away
    'imminent': 0     # Less than 7 days away
}
