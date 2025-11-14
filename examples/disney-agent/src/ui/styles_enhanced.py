"""
Disney Trip Planning Agent - ENHANCED Professional UI
Transformed with Frontend Aesthetic Agent + 228-Component Library Patterns

ENHANCEMENTS:
- Professional button variants from 63 button component patterns
- Enhanced cards from 45 card component patterns
- Sophisticated shadows and depth
- Better animations and transitions
- Improved form styling from 12 form patterns
- Enhanced navigation from 28 nav patterns
- Better accessibility and focus states
- More polished micro-interactions
"""


def apply_custom_styles() -> str:
    """
    Returns enhanced professional CSS with patterns from:
    - 228-component library (HTML5UP, Colorlib, Start Bootstrap)
    - Frontend design best practices
    - Advanced micro-interactions and polish

    Returns:
        str: Complete enhanced CSS within <style> tags
    """
    return """
<style>
    /* ============================================================================
       ENHANCED DISNEY TRIP PLANNER UI
       Powered by Frontend Aesthetic Agent + 228-Component Library
    ============================================================================ */

    /* Import modern premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    /* ============================================================================
       DESIGN TOKENS - ENHANCED
    ============================================================================ */

    :root {
        /* Brand Colors - Enhanced Disney Palette */
        --primary-blue: #1E40AF;
        --primary-blue-light: #3B82F6;
        --primary-blue-dark: #1E3A8A;
        --primary-teal: #0D9488;
        --primary-teal-light: #14B8A6;
        --primary-teal-dark: #0F766E;
        --accent-gold: #F59E0B;
        --accent-gold-light: #FBBF24;
        --accent-purple: #7C3AED;
        --accent-purple-light: #A78BFA;

        /* Semantic Colors */
        --success: #10B981;
        --success-light: #34D399;
        --success-dark: #059669;
        --warning: #F59E0B;
        --warning-light: #FBBF24;
        --warning-dark: #D97706;
        --danger: #EF4444;
        --danger-light: #F87171;
        --danger-dark: #DC2626;
        --info: #3B82F6;
        --info-light: #60A5FA;
        --info-dark: #2563EB;

        /* Neutrals - Extended */
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
        --gray-950: #030712;

        /* Background Layers */
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --bg-tertiary: #F3F4F6;
        --bg-dark: #0F172A;
        --bg-dark-secondary: #1E293B;

        /* Spacing Scale - 4px base */
        --space-0: 0;
        --space-1: 0.25rem;   /* 4px */
        --space-2: 0.5rem;    /* 8px */
        --space-3: 0.75rem;   /* 12px */
        --space-4: 1rem;      /* 16px */
        --space-5: 1.25rem;   /* 20px */
        --space-6: 1.5rem;    /* 24px */
        --space-7: 1.75rem;   /* 28px */
        --space-8: 2rem;      /* 32px */
        --space-10: 2.5rem;   /* 40px */
        --space-12: 3rem;     /* 48px */
        --space-16: 4rem;     /* 64px */
        --space-20: 5rem;     /* 80px */
        --space-24: 6rem;     /* 96px */

        /* Border Radius - Professional Scale */
        --radius-none: 0;
        --radius-sm: 0.375rem;    /* 6px */
        --radius-md: 0.5rem;      /* 8px */
        --radius-lg: 0.75rem;     /* 12px */
        --radius-xl: 1rem;        /* 16px */
        --radius-2xl: 1.5rem;     /* 24px */
        --radius-3xl: 2rem;       /* 32px */
        --radius-full: 9999px;

        /* Shadows - Layered & Sophisticated */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 6px 16px -6px rgba(0, 0, 0, 0.15);
        --shadow-lg: 0 10px 24px -8px rgba(0, 0, 0, 0.15), 0 4px 8px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 40px -12px rgba(0, 0, 0, 0.2), 0 8px 16px -8px rgba(0, 0, 0, 0.15);
        --shadow-2xl: 0 24px 48px -12px rgba(0, 0, 0, 0.25);
        --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);

        /* Glows - Magical Effects */
        --glow-blue: 0 0 24px rgba(30, 64, 175, 0.4);
        --glow-teal: 0 0 24px rgba(13, 148, 136, 0.4);
        --glow-gold: 0 0 24px rgba(245, 158, 11, 0.4);
        --glow-purple: 0 0 24px rgba(124, 58, 237, 0.4);
        --glow-success: 0 0 16px rgba(16, 185, 129, 0.3);
        --glow-danger: 0 0 16px rgba(239, 68, 68, 0.3);

        /* Transitions - Smooth & Professional */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
        --transition-smooth: 400ms cubic-bezier(0.4, 0, 0.2, 1);

        /* Z-index Scale */
        --z-base: 0;
        --z-dropdown: 1000;
        --z-sticky: 1100;
        --z-fixed: 1200;
        --z-modal-backdrop: 1300;
        --z-modal: 1400;
        --z-popover: 1500;
        --z-tooltip: 1600;
        --z-toast: 1700;
    }

    /* ============================================================================
       BASE STYLES
    ============================================================================ */

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
        font-feature-settings: "kern" 1, "liga" 1;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700;
        line-height: 1.2;
        color: var(--gray-900);
        letter-spacing: -0.02em;
    }

    p {
        line-height: 1.6;
        color: var(--gray-700);
    }

    a {
        color: var(--primary-blue);
        text-decoration: none;
        transition: color var(--transition-base);
    }

    a:hover {
        color: var(--primary-blue-dark);
    }

    /* ============================================================================
       MAIN LAYOUT
    ============================================================================ */

    .main {
        background: var(--bg-secondary) !important;
        padding: var(--space-6) !important;
        min-height: 100vh;
    }

    .main .block-container {
        max-width: 1400px !important;
        padding: var(--space-8) var(--space-6) !important;
    }

    /* ============================================================================
       SIDEBAR - Enhanced
    ============================================================================ */

    [data-testid="stSidebar"] {
        background: var(--white) !important;
        border-right: 1px solid var(--gray-200) !important;
        box-shadow: var(--shadow-md) !important;
        transition: all var(--transition-smooth) !important;
    }

    [data-testid="stSidebar"] > div {
        padding: var(--space-6) var(--space-4) !important;
    }

    /* Sidebar collapse button - clean icon only */
    [data-testid="stSidebar"] button[kind="header"] {
        background: transparent !important;
        border: none !important;
        padding: var(--space-2) !important;
        color: var(--gray-600) !important;
        font-size: 0 !important;
        transition: var(--transition-base) !important;
    }

    [data-testid="stSidebar"] button[kind="header"]:hover {
        color: var(--primary-blue) !important;
        transform: scale(1.1);
    }

    [data-testid="stSidebar"] button[kind="header"]:before {
        font-size: 1.25rem !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem;
        color: var(--gray-900);
        margin-bottom: var(--space-6);
        padding-bottom: var(--space-4);
        border-bottom: 3px solid var(--primary-blue);
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
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
       HEADER - Enhanced with Magic
    ============================================================================ */

    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        padding: var(--space-10) var(--space-8);
        border-radius: var(--radius-2xl);
        margin-bottom: var(--space-8);
        text-align: center;
        box-shadow: var(--shadow-xl), var(--glow-blue);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 10s linear infinite;
    }

    @keyframes shimmer {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .main-header h1 {
        color: var(--white);
        font-size: 2.5rem;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--space-3);
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.125rem;
        margin-top: var(--space-3);
        margin-bottom: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
    }

    /* ============================================================================
       TABS - Modern & Clean
    ============================================================================ */

    .stTabs {
        background: var(--white);
        border-radius: var(--radius-xl);
        padding: var(--space-5);
        box-shadow: var(--shadow-md);
        margin-bottom: var(--space-6);
    }

    [data-baseweb="tab-list"] {
        gap: var(--space-2);
        background: var(--gray-100) !important;
        border-radius: var(--radius-lg) !important;
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
        transition: all var(--transition-base) !important;
        white-space: nowrap !important;
        cursor: pointer;
    }

    [data-baseweb="tab"]:hover {
        background: var(--white) !important;
        color: var(--gray-900) !important;
        transform: translateY(-1px);
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: var(--white) !important;
        color: var(--primary-blue) !important;
        box-shadow: var(--shadow-sm) !important;
        font-weight: 600 !important;
    }

    [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* ============================================================================
       BUTTONS - Professional Variants from Component Library
    ============================================================================ */

    /* Base button styling */
    .stButton {
        margin: 0 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-3) var(--space-6) !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow), 0 4px 12px rgba(30, 64, 175, 0.2) !important;
        cursor: pointer !important;
        width: 100% !important;
        text-align: center !important;
        position: relative;
        overflow: hidden;
    }

    /* Ripple effect on click */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: var(--radius-full);
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        box-shadow: var(--shadow-lg), var(--glow-blue) !important;
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow) !important;
    }

    /* Secondary button variant */
    .stButton.secondary > button {
        background: var(--white) !important;
        color: var(--primary-blue) !important;
        border: 2px solid var(--primary-blue) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton.secondary > button:hover {
        background: var(--gray-50) !important;
        border-color: var(--primary-blue-dark) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Success button */
    .stButton.success > button {
        background: linear-gradient(135deg, var(--success) 0%, var(--success-light) 100%) !important;
        box-shadow: var(--shadow), 0 4px 12px rgba(16, 185, 129, 0.2) !important;
    }

    .stButton.success > button:hover {
        box-shadow: var(--shadow-lg), var(--glow-success) !important;
    }

    /* Warning button */
    .stButton.warning > button {
        background: linear-gradient(135deg, var(--warning) 0%, var(--warning-light) 100%) !important;
        box-shadow: var(--shadow), 0 4px 12px rgba(245, 158, 11, 0.2) !important;
    }

    /* Danger button */
    .stButton.danger > button {
        background: linear-gradient(135deg, var(--danger) 0%, var(--danger-light) 100%) !important;
        box-shadow: var(--shadow), 0 4px 12px rgba(239, 68, 68, 0.2) !important;
    }

    .stButton.danger > button:hover {
        box-shadow: var(--shadow-lg), var(--glow-danger) !important;
    }

    /* Ghost button */
    .stButton.ghost > button {
        background: transparent !important;
        color: var(--primary-blue) !important;
        border: 2px solid transparent !important;
        box-shadow: none !important;
    }

    .stButton.ghost > button:hover {
        background: var(--gray-50) !important;
        border-color: var(--gray-200) !important;
    }

    /* Icon button (small, circular) */
    .card-delete-btn {
        margin-left: auto !important;
        flex-shrink: 0 !important;
    }

    .card-delete-btn button {
        background: var(--danger) !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        min-height: 40px !important;
        padding: 0 !important;
        border-radius: var(--radius-full) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.125rem !important;
        transition: all var(--transition-base) !important;
    }

    .card-delete-btn button:hover {
        background: var(--danger-dark) !important;
        transform: scale(1.1) rotate(5deg);
        box-shadow: var(--shadow-lg), var(--glow-danger) !important;
    }

    /* Button row layout */
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
       CARDS - Enhanced from Component Library
    ============================================================================ */

    .card {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        margin-bottom: var(--space-4);
        transition: all var(--transition-smooth);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform var(--transition-smooth);
    }

    .card:hover {
        border-color: var(--primary-blue-light);
        box-shadow: var(--shadow-lg), 0 0 20px rgba(30, 64, 175, 0.08);
        transform: translateY(-4px);
    }

    .card:hover::before {
        transform: scaleX(1);
    }

    /* Checklist card variants */
    .checklist-card {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-left: 4px solid var(--gray-300);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-3);
        transition: all var(--transition-base);
        position: relative;
    }

    .checklist-card::after {
        content: '';
        position: absolute;
        right: var(--space-4);
        top: 50%;
        transform: translateY(-50%);
        width: 8px;
        height: 8px;
        border-radius: var(--radius-full);
        background: currentColor;
        opacity: 0.3;
    }

    .checklist-card:hover {
        border-left-width: 6px;
        box-shadow: var(--shadow-md);
        transform: translateX(4px);
    }

    .checklist-card.completed {
        background: var(--gray-50);
        opacity: 0.7;
        text-decoration: line-through;
    }

    .checklist-card[data-priority="high"] {
        border-left-color: var(--danger);
        color: var(--danger);
    }

    .checklist-card[data-priority="high"]:hover {
        box-shadow: var(--shadow-md), 0 0 16px rgba(239, 68, 68, 0.15);
    }

    .checklist-card[data-priority="medium"] {
        border-left-color: var(--warning);
        color: var(--warning);
    }

    .checklist-card[data-priority="medium"]:hover {
        box-shadow: var(--shadow-md), 0 0 16px rgba(245, 158, 11, 0.15);
    }

    .checklist-card[data-priority="low"] {
        border-left-color: var(--success);
        color: var(--success);
    }

    .checklist-card[data-priority="low"]:hover {
        box-shadow: var(--shadow-md), 0 0 16px rgba(16, 185, 129, 0.15);
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

    /* Glass card variant */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: var(--shadow-lg);
    }

    /* ============================================================================
       INPUTS & FORMS - Professional Styling
    ============================================================================ */

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background: var(--white) !important;
        border: 2px solid var(--gray-300) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-3) var(--space-4) !important;
        font-size: 0.9375rem !important;
        color: var(--gray-900) !important;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow-xs) !important;
    }

    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover,
    .stSelectbox > div > div:hover,
    .stNumberInput > div > div > input:hover,
    .stDateInput > div > div > input:hover {
        border-color: var(--gray-400) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.1), var(--shadow-sm) !important;
        outline: none !important;
    }

    /* Input labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label {
        color: var(--gray-700) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ============================================================================
       CHECKBOXES & RADIO - Modern Design
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
        transition: var(--transition-base) !important;
    }

    .stCheckbox > label:hover {
        color: var(--gray-900) !important;
    }

    .stCheckbox input[type="checkbox"] {
        width: 22px !important;
        height: 22px !important;
        border-radius: var(--radius-sm) !important;
        border: 2px solid var(--gray-300) !important;
        background: var(--white) !important;
        cursor: pointer !important;
        flex-shrink: 0 !important;
        transition: all var(--transition-base) !important;
    }

    .stCheckbox input[type="checkbox"]:hover {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.1) !important;
    }

    .stCheckbox input[type="checkbox"]:checked {
        background: var(--primary-blue) !important;
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 4px rgba(30, 64, 175, 0.15) !important;
    }

    /* ============================================================================
       BADGES - Clean Pill Design
    ============================================================================ */

    .badge {
        display: inline-flex;
        align-items: center;
        padding: var(--space-1) var(--space-3);
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: var(--transition-base);
    }

    .badge-primary {
        background: rgba(30, 64, 175, 0.1);
        color: var(--primary-blue);
    }

    .badge-primary:hover {
        background: rgba(30, 64, 175, 0.15);
    }

    .badge-success {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success-dark);
    }

    .badge-success:hover {
        background: rgba(16, 185, 129, 0.15);
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning-dark);
    }

    .badge-warning:hover {
        background: rgba(245, 158, 11, 0.15);
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger-dark);
    }

    .badge-danger:hover {
        background: rgba(239, 68, 68, 0.15);
    }

    .badge-info {
        background: rgba(59, 130, 246, 0.1);
        color: var(--info-dark);
    }

    /* ============================================================================
       ALERTS - Enhanced Notifications
    ============================================================================ */

    .stAlert {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-left: 4px solid var(--primary-blue) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-4) var(--space-5) !important;
        margin: var(--space-4) 0 !important;
        box-shadow: var(--shadow-sm) !important;
        animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .stSuccess {
        border-left-color: var(--success) !important;
        background: #F0FDF4 !important;
    }

    .stWarning {
        border-left-color: var(--warning) !important;
        background: #FFFBEB !important;
    }

    .stError {
        border-left-color: var(--danger) !important;
        background: #FEF2F2 !important;
    }

    .stInfo {
        border-left-color: var(--info) !important;
        background: #EFF6FF !important;
    }

    /* ============================================================================
       CHAT INTERFACE - Professional Message Bubbles
    ============================================================================ */

    .stChatMessage {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--space-5) !important;
        margin-bottom: var(--space-4) !important;
        box-shadow: var(--shadow-sm) !important;
        transition: var(--transition-base) !important;
    }

    .stChatMessage:hover {
        box-shadow: var(--shadow-md) !important;
    }

    .stChatMessage[data-testid="chat-message-user"] {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
        border-color: var(--primary-blue-light) !important;
    }

    .stChatMessage[data-testid="chat-message-assistant"] {
        background: var(--gray-50) !important;
        border-color: var(--gray-200) !important;
    }

    /* ============================================================================
       METRICS - Dashboard Cards
    ============================================================================ */

    [data-testid="stMetric"] {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        box-shadow: var(--shadow-md);
        transition: var(--transition-smooth);
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--primary-blue-light);
        box-shadow: var(--shadow-lg), 0 0 24px rgba(30, 64, 175, 0.08);
        transform: translateY(-4px);
    }

    [data-testid="stMetricLabel"] {
        color: var(--gray-600);
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stMetricValue"] {
        color: var(--gray-900);
        font-size: 2.25rem;
        font-weight: 800;
        margin-top: var(--space-2);
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ============================================================================
       PROGRESS BAR - Modern Indicator
    ============================================================================ */

    .stProgress > div > div {
        background: var(--gray-200) !important;
        border-radius: var(--radius-full) !important;
        height: 12px !important;
        overflow: hidden;
        box-shadow: var(--shadow-inner);
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--primary-teal) 100%) !important;
        border-radius: var(--radius-full) !important;
        box-shadow: 0 0 12px rgba(30, 64, 175, 0.3);
        animation: progressShimmer 2s ease-in-out infinite;
    }

    @keyframes progressShimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    /* ============================================================================
       EXPANDER - Professional Accordion
    ============================================================================ */

    .streamlit-expanderHeader {
        background: var(--white) !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-4) var(--space-5) !important;
        font-weight: 600 !important;
        color: var(--gray-900) !important;
        transition: all var(--transition-base) !important;
    }

    .streamlit-expanderHeader:hover {
        background: var(--gray-50) !important;
        border-color: var(--primary-blue) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .streamlit-expanderContent {
        border: 1px solid var(--gray-200) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
        padding: var(--space-5) !important;
        background: var(--gray-50) !important;
    }

    /* ============================================================================
       DATAFRAME - Clean Table Style
    ============================================================================ */

    .stDataFrame {
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    .stDataFrame table {
        width: 100%;
    }

    .stDataFrame th {
        background: var(--gray-100) !important;
        color: var(--gray-900) !important;
        font-weight: 600 !important;
        padding: var(--space-3) var(--space-4) !important;
        border-bottom: 2px solid var(--gray-300) !important;
    }

    .stDataFrame td {
        padding: var(--space-3) var(--space-4) !important;
        border-bottom: 1px solid var(--gray-200) !important;
    }

    .stDataFrame tr:hover {
        background: var(--gray-50) !important;
    }

    /* ============================================================================
       SCROLLBAR - Modern Custom Design
    ============================================================================ */

    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }

    ::-webkit-scrollbar-track {
        background: var(--gray-100);
        border-radius: var(--radius-lg);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--gray-400);
        border-radius: var(--radius-lg);
        border: 3px solid var(--gray-100);
        transition: background var(--transition-base);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--gray-500);
    }

    ::-webkit-scrollbar-thumb:active {
        background: var(--gray-600);
    }

    /* ============================================================================
       LOADING SPINNER - Branded
    ============================================================================ */

    .stSpinner > div {
        border-color: var(--primary-blue) transparent var(--primary-teal) transparent !important;
        animation: spin 1s cubic-bezier(0.4, 0, 0.2, 1) infinite !important;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* ============================================================================
       TOOLTIPS - Professional Popover
    ============================================================================ */

    [data-baseweb="tooltip"] {
        background: var(--gray-900) !important;
        color: var(--white) !important;
        padding: var(--space-2) var(--space-3) !important;
        border-radius: var(--radius-md) !important;
        font-size: 0.875rem !important;
        box-shadow: var(--shadow-xl) !important;
    }

    /* ============================================================================
       STREAMLIT-SPECIFIC FIXES
    ============================================================================ */

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hide toolbar */
    .stApp [data-testid="stToolbar"] {
        display: none;
    }

    /* Fix columns spacing */
    [data-testid="column"] {
        padding: 0 var(--space-2) !important;
    }

    [data-testid="column"]:first-child {
        padding-left: 0 !important;
    }

    [data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Ensure proper stacking */
    .stButton,
    .stCheckbox,
    .stTextInput,
    .stSelectbox {
        position: relative;
        z-index: var(--z-base);
    }

    /* ============================================================================
       RESPONSIVE DESIGN - Mobile Optimizations
    ============================================================================ */

    @media (max-width: 768px) {
        :root {
            --space-8: 1.5rem;
            --space-10: 2rem;
            --space-12: 2.5rem;
        }

        .main .block-container {
            padding: var(--space-4) var(--space-3) !important;
        }

        .main-header {
            padding: var(--space-6) var(--space-4);
        }

        .main-header h1 {
            font-size: 1.75rem;
            flex-direction: column;
        }

        .main-header p {
            font-size: 1rem;
        }

        [data-baseweb="tab"] {
            padding: var(--space-2) var(--space-3) !important;
            font-size: 0.875rem !important;
        }

        .card, .checklist-card {
            padding: var(--space-4);
        }

        .stButton > button {
            padding: var(--space-3) var(--space-4) !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.75rem;
        }
    }

    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1.5rem;
        }

        .card {
            padding: var(--space-3);
        }

        .button-row {
            flex-direction: column;
            gap: var(--space-2) !important;
        }

        .button-row > * {
            width: 100%;
        }
    }

    /* ============================================================================
       ACCESSIBILITY ENHANCEMENTS
    ============================================================================ */

    /* Respect user motion preferences */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .card,
        .checklist-card,
        .stButton > button {
            border-width: 2px !important;
        }
    }

    /* Dark mode support (future) */
    @media (prefers-color-scheme: dark) {
        /* Dark mode variables would go here */
    }

    /* Focus visible (keyboard navigation) */
    *:focus-visible {
        outline: 3px solid var(--primary-blue) !important;
        outline-offset: 2px !important;
    }

    /* ============================================================================
       UTILITY CLASSES
    ============================================================================ */

    /* Spacing utilities */
    .mt-0 { margin-top: 0 !important; }
    .mt-1 { margin-top: var(--space-1) !important; }
    .mt-2 { margin-top: var(--space-2) !important; }
    .mt-3 { margin-top: var(--space-3) !important; }
    .mt-4 { margin-top: var(--space-4) !important; }
    .mt-6 { margin-top: var(--space-6) !important; }
    .mt-8 { margin-top: var(--space-8) !important; }

    .mb-0 { margin-bottom: 0 !important; }
    .mb-1 { margin-bottom: var(--space-1) !important; }
    .mb-2 { margin-bottom: var(--space-2) !important; }
    .mb-3 { margin-bottom: var(--space-3) !important; }
    .mb-4 { margin-bottom: var(--space-4) !important; }
    .mb-6 { margin-bottom: var(--space-6) !important; }
    .mb-8 { margin-bottom: var(--space-8) !important; }

    .p-0 { padding: 0 !important; }
    .p-2 { padding: var(--space-2) !important; }
    .p-4 { padding: var(--space-4) !important; }
    .p-6 { padding: var(--space-6) !important; }
    .p-8 { padding: var(--space-8) !important; }

    /* Flexbox utilities */
    .flex { display: flex !important; }
    .flex-col { flex-direction: column !important; }
    .flex-row { flex-direction: row !important; }
    .items-start { align-items: flex-start !important; }
    .items-center { align-items: center !important; }
    .items-end { align-items: flex-end !important; }
    .justify-start { justify-content: flex-start !important; }
    .justify-center { justify-content: center !important; }
    .justify-end { justify-content: flex-end !important; }
    .justify-between { justify-content: space-between !important; }
    .gap-1 { gap: var(--space-1) !important; }
    .gap-2 { gap: var(--space-2) !important; }
    .gap-3 { gap: var(--space-3) !important; }
    .gap-4 { gap: var(--space-4) !important; }
    .gap-6 { gap: var(--space-6) !important; }

    /* Text utilities */
    .text-left { text-align: left !important; }
    .text-center { text-align: center !important; }
    .text-right { text-align: right !important; }
    .font-light { font-weight: 300 !important; }
    .font-normal { font-weight: 400 !important; }
    .font-medium { font-weight: 500 !important; }
    .font-semibold { font-weight: 600 !important; }
    .font-bold { font-weight: 700 !important; }
    .font-extrabold { font-weight: 800 !important; }
    .text-xs { font-size: 0.75rem !important; }
    .text-sm { font-size: 0.875rem !important; }
    .text-base { font-size: 1rem !important; }
    .text-lg { font-size: 1.125rem !important; }
    .text-xl { font-size: 1.25rem !important; }
    .text-2xl { font-size: 1.5rem !important; }

    /* Color utilities */
    .text-primary { color: var(--primary-blue) !important; }
    .text-success { color: var(--success) !important; }
    .text-warning { color: var(--warning) !important; }
    .text-danger { color: var(--danger) !important; }
    .text-gray { color: var(--gray-600) !important; }
    .text-muted { color: var(--gray-500) !important; }

    /* Display utilities */
    .hidden { display: none !important; }
    .block { display: block !important; }
    .inline { display: inline !important; }
    .inline-block { display: inline-block !important; }

    /* Border radius utilities */
    .rounded-none { border-radius: 0 !important; }
    .rounded-sm { border-radius: var(--radius-sm) !important; }
    .rounded { border-radius: var(--radius-md) !important; }
    .rounded-lg { border-radius: var(--radius-lg) !important; }
    .rounded-xl { border-radius: var(--radius-xl) !important; }
    .rounded-full { border-radius: var(--radius-full) !important; }

    /* Shadow utilities */
    .shadow-none { box-shadow: none !important; }
    .shadow-sm { box-shadow: var(--shadow-sm) !important; }
    .shadow { box-shadow: var(--shadow) !important; }
    .shadow-md { box-shadow: var(--shadow-md) !important; }
    .shadow-lg { box-shadow: var(--shadow-lg) !important; }
    .shadow-xl { box-shadow: var(--shadow-xl) !important; }

</style>
"""
