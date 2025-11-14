"""
Disney Trip Planning Agent - Clean Modern UI
Completely rebuilt frontend with proper layout, no overlapping elements,
and clean, professional Disney-inspired design.
"""


def apply_custom_styles() -> str:
    """
    Returns clean, modern CSS styling with proper layout and no overlapping issues.

    Fixes:
    - No overlapping buttons
    - Icons don't show text behind them
    - Clean sidebar with proper collapse
    - Proper spacing and layout
    - Modern, professional Disney theme

    Returns:
        str: Complete CSS within <style> tags
    """
    return """
<style>
    /* ============================================================================
       CLEAN MODERN DISNEY UI - REBUILT FROM SCRATCH
       No overlapping, clean layout, professional design
    ============================================================================ */

    /* Import clean modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ============================================================================
       ROOT RESET - Clean slate
    ============================================================================ */

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* ============================================================================
       DESIGN TOKENS - Professional Disney Palette
    ============================================================================ */

    :root {
        /* Brand Colors */
        --primary-blue: #1E40AF;
        --primary-teal: #0D9488;
        --accent-gold: #F59E0B;
        --accent-purple: #7C3AED;

        /* Neutrals */
        --white: #FFFFFF;
        --gray-50: #F9FAFB;
        --gray-100: #F3F4F6;
        --gray-200: #E5E7EB;
        --gray-300: #D1D5DB;
        --gray-400: #9CA3AF;
        --gray-500: #6B7280;
        --gray-600: #4B5563;
        --gray-700: #374151;
        --gray-800: #1F2937;
        --gray-900: #111827;

        /* Background */
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --bg-dark: #0F172A;

        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;

        /* Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-full: 9999px;

        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);

        /* Transitions */
        --transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ============================================================================
       BASE STYLES
    ============================================================================ */

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700;
        line-height: 1.2;
        color: var(--gray-900);
    }

    p {
        line-height: 1.6;
        color: var(--gray-700);
    }

    /* ============================================================================
       MAIN LAYOUT - Clean white background
    ============================================================================ */

    .main {
        background: var(--bg-secondary) !important;
        padding: var(--space-6) !important;
    }

    .main .block-container {
        max-width: 1400px !important;
        padding: var(--space-8) var(--space-6) !important;
    }

    /* ============================================================================
       SIDEBAR - Clean and professional
    ============================================================================ */

    [data-testid="stSidebar"] {
        background: var(--white) !important;
        border-right: 1px solid var(--gray-200) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    [data-testid="stSidebar"] > div {
        padding: var(--space-6) var(--space-4) !important;
    }

    /* Fix sidebar collapse button - hide the text */
    [data-testid="stSidebar"] button[kind="header"] {
        background: transparent !important;
        border: none !important;
        padding: var(--space-2) !important;
        color: var(--gray-600) !important;
        font-size: 0 !important; /* Hide text */
    }

    /* Show only the icon */
    [data-testid="stSidebar"] button[kind="header"]:before {
        font-size: 1.25rem !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem;
        color: var(--gray-900);
        margin-bottom: var(--space-6);
        padding-bottom: var(--space-4);
        border-bottom: 2px solid var(--primary-blue);
    }

    [data-testid="stSidebar"] h2 {
        font-size: 1.125rem;
        color: var(--gray-800);
        margin-top: var(--space-6);
        margin-bottom: var(--space-3);
    }

    [data-testid="stSidebar"] label {
        color: var(--gray-700) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ============================================================================
       HEADER - Clean and modern
    ============================================================================ */

    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        padding: var(--space-8) var(--space-6);
        border-radius: var(--radius-xl);
        margin-bottom: var(--space-8);
        text-align: center;
        box-shadow: var(--shadow-lg);
    }

    .main-header h1 {
        color: var(--white);
        font-size: 2.5rem;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--space-3);
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.125rem;
        margin-top: var(--space-3);
        margin-bottom: 0;
    }

    /* ============================================================================
       TABS - Clean modern tabs
    ============================================================================ */

    .stTabs {
        background: var(--white);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        box-shadow: var(--shadow);
        margin-bottom: var(--space-6);
    }

    [data-baseweb="tab-list"] {
        gap: var(--space-2);
        background: var(--gray-100) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-1) !important;
    }

    [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-5) !important;
        color: var(--gray-600) !important;
        font-weight: 500 !important;
        font-size: 0.9375rem !important;
        transition: var(--transition) !important;
        white-space: nowrap !important;
    }

    [data-baseweb="tab"]:hover {
        background: var(--white) !important;
        color: var(--gray-900) !important;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: var(--white) !important;
        color: var(--primary-blue) !important;
        box-shadow: var(--shadow-sm) !important;
        font-weight: 600 !important;
    }

    /* Hide the tab underline */
    [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* ============================================================================
       CARDS - Clean card design
    ============================================================================ */

    .card {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: var(--space-5);
        margin-bottom: var(--space-4);
        transition: var(--transition);
        box-shadow: var(--shadow-sm);
    }

    .card:hover {
        border-color: var(--primary-blue);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    /* Checklist card */
    .checklist-card {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-left: 4px solid var(--gray-300);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-3);
        transition: var(--transition);
    }

    .checklist-card:hover {
        border-left-color: var(--primary-blue);
        box-shadow: var(--shadow);
    }

    .checklist-card.completed {
        background: var(--gray-50);
        opacity: 0.7;
    }

    .checklist-card[data-priority="high"] {
        border-left-color: #EF4444;
    }

    .checklist-card[data-priority="medium"] {
        border-left-color: #F59E0B;
    }

    .checklist-card[data-priority="low"] {
        border-left-color: #10B981;
    }

    .checklist-card strong {
        color: var(--gray-900);
        font-size: 1rem;
        font-weight: 600;
        display: block;
        margin-bottom: var(--space-2);
    }

    .checklist-card small {
        color: var(--gray-500);
        font-size: 0.875rem;
    }

    /* ============================================================================
       BUTTONS - Proper spacing, no overlap
    ============================================================================ */

    .stButton {
        margin: 0 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-5) !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow) !important;
        cursor: pointer !important;
        width: 100% !important;
        text-align: center !important;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Secondary button */
    .stButton.secondary > button {
        background: var(--white) !important;
        color: var(--primary-blue) !important;
        border: 2px solid var(--primary-blue) !important;
    }

    /* Delete button - proper sizing, no overlap */
    .card-delete-btn {
        margin-left: auto !important;
        flex-shrink: 0 !important;
    }

    .card-delete-btn button {
        background: #EF4444 !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        padding: 0 !important;
        border-radius: var(--radius-full) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.125rem !important;
    }

    .card-delete-btn button:hover {
        background: #DC2626 !important;
        transform: scale(1.05);
    }

    /* Button row - proper flex layout to prevent overlap */
    .button-row {
        display: flex !important;
        gap: var(--space-3) !important;
        align-items: center !important;
        margin-top: var(--space-3) !important;
    }

    .button-row > * {
        flex: 1 1 auto !important;
    }

    .button-row .card-delete-btn {
        flex: 0 0 auto !important;
    }

    /* ============================================================================
       INPUTS - Clean form inputs
    ============================================================================ */

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background: var(--white) !important;
        border: 1px solid var(--gray-300) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-4) !important;
        font-size: 0.9375rem !important;
        color: var(--gray-900) !important;
        transition: var(--transition) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1) !important;
        outline: none !important;
    }

    /* ============================================================================
       CHECKBOXES - Modern checkbox style
    ============================================================================ */

    .stCheckbox {
        padding: var(--space-2) 0;
    }

    .stCheckbox > label {
        color: var(--gray-700) !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        gap: var(--space-3) !important;
    }

    .stCheckbox input[type="checkbox"] {
        width: 20px !important;
        height: 20px !important;
        border-radius: var(--radius-sm) !important;
        border: 2px solid var(--gray-300) !important;
        background: var(--white) !important;
        cursor: pointer !important;
        flex-shrink: 0 !important;
    }

    .stCheckbox input[type="checkbox"]:checked {
        background: var(--primary-blue) !important;
        border-color: var(--primary-blue) !important;
    }

    /* ============================================================================
       BADGES - Clean pill badges
    ============================================================================ */

    .badge {
        display: inline-flex;
        align-items: center;
        padding: var(--space-1) var(--space-3);
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }

    .badge-primary {
        background: rgba(30, 64, 175, 0.1);
        color: var(--primary-blue);
    }

    .badge-success {
        background: rgba(16, 185, 129, 0.1);
        color: #059669;
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #D97706;
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.1);
        color: #DC2626;
    }

    /* ============================================================================
       ALERTS - Clean notification style
    ============================================================================ */

    .stAlert {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-left: 4px solid var(--primary-blue) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-4) !important;
        margin: var(--space-4) 0 !important;
    }

    .stSuccess {
        border-left-color: #10B981 !important;
        background: #F0FDF4 !important;
    }

    .stWarning {
        border-left-color: #F59E0B !important;
        background: #FFFBEB !important;
    }

    .stError {
        border-left-color: #EF4444 !important;
        background: #FEF2F2 !important;
    }

    .stInfo {
        border-left-color: var(--primary-blue) !important;
        background: #EFF6FF !important;
    }

    /* ============================================================================
       CHAT INTERFACE - Clean message bubbles
    ============================================================================ */

    .stChatMessage {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-4) !important;
        margin-bottom: var(--space-3) !important;
    }

    .stChatMessage[data-testid="chat-message-user"] {
        background: #EFF6FF !important;
        border-color: var(--primary-blue) !important;
    }

    .stChatMessage[data-testid="chat-message-assistant"] {
        background: var(--gray-50) !important;
    }

    /* ============================================================================
       METRICS - Dashboard cards
    ============================================================================ */

    [data-testid="stMetric"] {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: var(--space-5);
        box-shadow: var(--shadow-sm);
    }

    [data-testid="stMetricLabel"] {
        color: var(--gray-600);
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }

    [data-testid="stMetricValue"] {
        color: var(--gray-900);
        font-size: 2rem;
        font-weight: 700;
        margin-top: var(--space-2);
    }

    /* ============================================================================
       PROGRESS BAR - Clean progress indicator
    ============================================================================ */

    .stProgress > div > div {
        background: var(--gray-200) !important;
        border-radius: var(--radius-full) !important;
        height: 8px !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--primary-teal) 100%) !important;
        border-radius: var(--radius-full) !important;
    }

    /* ============================================================================
       EXPANDER - Clean accordion
    ============================================================================ */

    .streamlit-expanderHeader {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-4) !important;
        font-weight: 600 !important;
        color: var(--gray-900) !important;
    }

    .streamlit-expanderHeader:hover {
        background: var(--gray-50) !important;
        border-color: var(--primary-blue) !important;
    }

    .streamlit-expanderContent {
        border: 1px solid var(--gray-200) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: var(--space-4) !important;
    }

    /* ============================================================================
       DATAFRAME - Clean table style
    ============================================================================ */

    .stDataFrame {
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    /* ============================================================================
       SCROLLBAR - Modern scrollbar
    ============================================================================ */

    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: var(--gray-100);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--gray-400);
        border-radius: var(--radius-md);
        border: 3px solid var(--gray-100);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--gray-500);
    }

    /* ============================================================================
       RESPONSIVE DESIGN
    ============================================================================ */

    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--space-4) var(--space-3) !important;
        }

        .main-header h1 {
            font-size: 1.75rem;
        }

        .main-header {
            padding: var(--space-6) var(--space-4);
        }

        [data-baseweb="tab"] {
            padding: var(--space-2) var(--space-3) !important;
            font-size: 0.875rem !important;
        }

        .card, .checklist-card {
            padding: var(--space-3);
        }
    }

    /* ============================================================================
       STREAMLIT-SPECIFIC FIXES
    ============================================================================ */

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fix toolbar */
    .stApp [data-testid="stToolbar"] {
        display: none;
    }

    /* Fix columns to prevent overlap */
    [data-testid="column"] {
        padding: 0 var(--space-2) !important;
    }

    [data-testid="column"]:first-child {
        padding-left: 0 !important;
    }

    [data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Ensure proper stacking context */
    .stButton,
    .stCheckbox,
    .stTextInput,
    .stSelectbox {
        position: relative;
        z-index: 1;
    }

    /* Fix spinner */
    .stSpinner > div {
        border-color: var(--primary-blue) transparent var(--primary-blue) transparent !important;
    }

    /* ============================================================================
       UTILITY CLASSES
    ============================================================================ */

    .mt-1 { margin-top: var(--space-1) !important; }
    .mt-2 { margin-top: var(--space-2) !important; }
    .mt-3 { margin-top: var(--space-3) !important; }
    .mt-4 { margin-top: var(--space-4) !important; }
    .mt-6 { margin-top: var(--space-6) !important; }
    .mt-8 { margin-top: var(--space-8) !important; }

    .mb-1 { margin-bottom: var(--space-1) !important; }
    .mb-2 { margin-bottom: var(--space-2) !important; }
    .mb-3 { margin-bottom: var(--space-3) !important; }
    .mb-4 { margin-bottom: var(--space-4) !important; }
    .mb-6 { margin-bottom: var(--space-6) !important; }
    .mb-8 { margin-bottom: var(--space-8) !important; }

    .flex { display: flex !important; }
    .items-center { align-items: center !important; }
    .justify-between { justify-content: space-between !important; }
    .gap-2 { gap: var(--space-2) !important; }
    .gap-3 { gap: var(--space-3) !important; }
    .gap-4 { gap: var(--space-4) !important; }

    .text-center { text-align: center !important; }
    .font-bold { font-weight: 700 !important; }
    .text-sm { font-size: 0.875rem !important; }
    .text-xs { font-size: 0.75rem !important; }

</style>
"""
