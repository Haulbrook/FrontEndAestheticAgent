"""
Disney Trip Planning Agent - Streamlit Web Application
A beautiful, user-friendly interface for planning your magical Disney vacation
"""
import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import pytz
import pickle
from pathlib import Path

from src.agents.trip_planner_agent import TripPlannerAgent
from src.models.trip_data import TripDetails, ChecklistItem, IdeaSuggestion
from src.utils.helpers import calculate_countdown, format_countdown, get_trip_phase
from src.utils.firebase_config import get_firebase_manager

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Disney Trip Planner",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Magical Disney Theme with Animations
st.markdown("""
<style>
    /* Import a whimsical font */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

    * {
        font-family: 'Nunito', sans-serif !important;
    }

    /* Sparkle animation */
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1) rotate(180deg); }
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    /* Button shimmy/bounce animation */
    @keyframes shimmy {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        25% { transform: translateX(-5px) rotate(-2deg); }
        75% { transform: translateX(5px) rotate(2deg); }
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* Fireworks animation */
    @keyframes firework {
        0% {
            transform: translate(0, 0) scale(0);
            opacity: 1;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translate(var(--tx), var(--ty)) scale(1);
            opacity: 0;
        }
    }

    /* Floating sparkles */
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    /* Magical pulse */
    @keyframes magicPulse {
        0%, 100% {
            box-shadow: 0 0 5px rgba(135, 206, 235, 0.5),
                        0 0 10px rgba(135, 206, 235, 0.3),
                        0 0 15px rgba(135, 206, 235, 0.2);
        }
        50% {
            box-shadow: 0 0 20px rgba(135, 206, 235, 0.8),
                        0 0 30px rgba(135, 206, 235, 0.6),
                        0 0 40px rgba(135, 206, 235, 0.4);
        }
    }

    /* Main background - light airy blue with floating sparkles */
    .main {
        background: linear-gradient(180deg, #f0f8ff 0%, #e6f3ff 50%, #ffffff 100%);
        position: relative;
    }

    .main::before, .main::after {
        content: '✨';
        position: fixed;
        font-size: 24px;
        animation: float 4s infinite ease-in-out;
        pointer-events: none;
        z-index: 1;
    }

    .main::before {
        top: 20%;
        left: 10%;
        animation-delay: 0s;
    }

    .main::after {
        top: 60%;
        right: 15%;
        animation-delay: 2s;
    }

    /* Sidebar - light blue gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
        position: relative;
    }

    [data-testid="stSidebar"]::before {
        content: '⭐';
        position: absolute;
        top: 10%;
        right: 10%;
        font-size: 20px;
        animation: sparkle 2s infinite;
    }

    /* Main header with sparkle effect and fireworks */
    .main-header {
        text-align: center;
        font-size: 3.5em;
        font-weight: 900;
        padding: 40px;
        background: linear-gradient(135deg, #87ceeb 0%, #b0e0e6 50%, #add8e6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        animation: magicPulse 3s infinite;
        letter-spacing: 2px;
    }

    /* Fireworks container */
    .main-header::before {
        content: '🎆';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2em;
        animation: firework 3s infinite;
        --tx: -100px;
        --ty: -100px;
    }

    .main-header::after {
        content: '🎇';
        position: absolute;
        top: -20px;
        right: 10%;
        font-size: 1.5em;
        animation: firework 3s infinite 1s;
        --tx: 100px;
        --ty: -80px;
    }

    /* Countdown box - CIRCLE SHAPE with shimmer and stars */
    .countdown-box {
        background: linear-gradient(135deg, #87ceeb 0%, #b0e0e6 50%, #add8e6 100%) !important;
        padding: 60px 40px !important;
        border-radius: 50% !important;  /* CIRCLE! */
        width: 400px !important;
        height: 400px !important;
        margin: 20px auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #ffffff !important;
        text-align: center !important;
        font-size: 1.8em !important;
        font-weight: 900 !important;
        box-shadow: 0 10px 40px rgba(135, 206, 235, 0.6),
                    inset 0 2px 0 rgba(255,255,255,0.6) !important;
        border: 5px solid rgba(255, 215, 0, 0.6) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: magicPulse 4s infinite !important;
    }

    .countdown-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.4) 50%,
            transparent 70%
        );
        animation: shimmer 3s infinite;
        border-radius: 50%;
    }

    .countdown-box::after {
        content: '🌟';
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 1.8em;
        animation: sparkle 2s infinite;
    }

    /* Checklist items - PLAYING CARD STYLE */
    .checklist-card {
        width: 100% !important;
        min-height: 180px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        border-radius: 20px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%) !important;
        border: 3px solid #b0d4f1 !important;
        box-shadow: 0 6px 16px rgba(135, 206, 235, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: visible !important;
    }

    .checklist-card:hover {
        transform: translateY(-8px) rotate(1deg) scale(1.02) !important;
        box-shadow: 0 12px 28px rgba(135, 206, 235, 0.5) !important;
        border-color: #ffd700 !important;
    }

    .checklist-card.completed {
        opacity: 0.75 !important;
        background: linear-gradient(135deg, #f5f5f5 0%, #e8f4f8 100%) !important;
        filter: grayscale(20%) !important;
    }

    .checklist-card.completed::before {
        content: '✓' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) rotate(-15deg) !important;
        font-size: 100px !important;
        color: rgba(39, 174, 96, 0.25) !important;
        font-weight: 900 !important;
        z-index: 1 !important;
        animation: checkPop 0.5s ease-out !important;
        pointer-events: none !important;
    }

    @keyframes checkPop {
        0% { transform: translate(-50%, -50%) rotate(-15deg) scale(0); }
        50% { transform: translate(-50%, -50%) rotate(-15deg) scale(1.3); }
        100% { transform: translate(-50%, -50%) rotate(-15deg) scale(1); }
    }

    .checklist-card-content {
        position: relative !important;
        z-index: 2 !important;
    }

    .checklist-card strong {
        color: #1e88e5 !important;
        font-size: 1.1em !important;
        font-weight: 700 !important;
        display: block !important;
        margin-bottom: 12px !important;
        line-height: 1.4 !important;
    }

    .checklist-card small {
        color: #546e7a !important;
        font-size: 0.85em !important;
        display: block !important;
        margin-top: 8px !important;
    }

    .card-checkbox-container {
        display: flex !important;
        align-items: flex-start !important;
        gap: 12px !important;
        margin-bottom: 8px !important;
    }

    /* Card Action Buttons - Small and Clean */
    .card-actions {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 12px !important;
        margin-top: 12px !important;
        padding: 0 4px !important;
    }

    /* Card action row - force proper layout */
    .card-action-row {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 10px !important;
        margin-top: 10px !important;
        padding: 0 !important;
    }

    .card-action-row > div:first-child {
        flex: 1 !important;
        max-width: calc(100% - 50px) !important;
    }

    .card-action-row > div:last-child {
        flex: 0 0 40px !important;
        width: 40px !important;
    }

    /* Small delete button for cards - MORE SPECIFIC SELECTOR */
    .card-delete-btn .stButton>button,
    .card-delete-btn button {
        background: linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%) !important;
        border: 2px solid #e57373 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        min-height: 40px !important;
        max-width: 40px !important;
        max-height: 40px !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 18px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 8px rgba(239, 83, 80, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        overflow: hidden !important;
    }

    .card-delete-btn .stButton>button::before,
    .card-delete-btn .stButton>button::after,
    .card-delete-btn button::before,
    .card-delete-btn button::after {
        content: none !important;
        display: none !important;
    }

    .card-delete-btn .stButton>button:hover,
    .card-delete-btn button:hover {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%) !important;
        transform: scale(1.1) rotate(10deg) !important;
        box-shadow: 0 4px 12px rgba(239, 83, 80, 0.5) !important;
        animation: none !important;
        border-width: 2px !important;
    }

    /* Checkbox label alignment */
    .stCheckbox label {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        font-size: 14px !important;
        color: #546e7a !important;
        font-weight: 600 !important;
    }

    /* Ensure no extra padding in card action columns */
    .card-action-row [data-testid="column"] {
        padding: 0 5px !important;
        gap: 0 !important;
    }

    .card-action-row [data-testid="column"]:first-child {
        padding-right: 8px !important;
    }

    .card-action-row [data-testid="column"]:last-child {
        padding-left: 0 !important;
    }

    /* Idea cards - CIRCLE SHAPE with sparkle and shimmy */
    .idea-card {
        padding: 40px 35px !important;
        margin: 20px auto !important;
        border-radius: 50% !important;  /* CIRCLE! */
        width: 350px !important;
        height: 350px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
        box-shadow: 0 8px 25px rgba(135, 206, 235, 0.4) !important;
        border: 5px solid rgba(255, 215, 0, 0.5) !important;
        color: #2c3e50 !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }

    .idea-card:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 12px 40px rgba(135, 206, 235, 0.6);
        animation: shimmy 0.6s ease-in-out;
        border-color: rgba(255, 215, 0, 0.8);
    }

    .idea-card::after {
        content: '✨';
        position: absolute;
        top: 30px;
        right: 30px;
        font-size: 2.5em;
        animation: sparkle 2s infinite;
    }

    .idea-card h3 {
        color: #1e88e5 !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .idea-card p {
        color: #37474f !important;
        text-align: center;
        font-size: 0.95em;
    }

    .idea-card small {
        color: #607d8b !important;
        text-align: center;
        display: block;
        margin-top: 10px;
    }

    /* Buttons - PERFECT CIRCLE/PILL SHAPE with shimmy animation */
    .stButton>button {
        background: linear-gradient(135deg, #87ceeb 0%, #5dade2 100%);
        color: white;
        border: 4px solid rgba(255, 215, 0, 0.5);
        border-radius: 50px !important;  /* PILL SHAPE! */
        padding: 16px 40px;
        min-width: 150px;
        font-weight: 800;
        font-size: 17px;
        box-shadow: 0 6px 20px rgba(135, 206, 235, 0.5);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: visible;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button::before {
        content: '✨';
        position: absolute;
        left: 15px;
        animation: sparkle 1.5s infinite;
        font-size: 1.2em;
    }

    .stButton>button::after {
        content: '✨';
        position: absolute;
        right: 15px;
        animation: sparkle 1.5s infinite 0.5s;
        font-size: 1.2em;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #5dade2 0%, #3498db 100%);
        animation: shimmy 0.5s ease-in-out, bounce 0.5s ease-in-out;
        box-shadow: 0 10px 35px rgba(135, 206, 235, 0.7);
        border-color: rgba(255, 215, 0, 0.9);
        transform: scale(1.1);
        border-width: 5px;
    }

    .stButton>button:active {
        transform: scale(0.9);
    }

    /* OVERRIDE: Card delete button - placed AFTER general button styles for precedence */
    .card-action-row .card-delete-btn .stButton>button,
    .card-delete-btn .stButton>button {
        background: linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%) !important;
        border: 2px solid #e57373 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        min-height: 40px !important;
        max-width: 40px !important;
        max-height: 40px !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 18px !important;
        line-height: 1 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        overflow: hidden !important;
    }

    .card-action-row .card-delete-btn .stButton>button::before,
    .card-action-row .card-delete-btn .stButton>button::after,
    .card-delete-btn .stButton>button::before,
    .card-delete-btn .stButton>button::after {
        content: none !important;
        display: none !important;
    }

    .card-action-row .card-delete-btn .stButton>button:hover,
    .card-delete-btn .stButton>button:hover {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%) !important;
        transform: scale(1.1) rotate(10deg) !important;
        animation: none !important;
        border-width: 2px !important;
    }

    /* Priority colors - adjusted for light theme */
    .priority-high {
        border-left-color: #e74c3c;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
    }
    .priority-medium {
        border-left-color: #f39c12;
        background: linear-gradient(135deg, #fffef5 0%, #fff8e1 100%);
    }
    .priority-low {
        border-left-color: #27ae60;
        background: linear-gradient(135deg, #f5fff5 0%, #e8f5e9 100%);
    }

    /* Input fields - PILL SHAPE with light blue focus */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        color: #2c3e50 !important;
        background-color: white !important;
        border: 3px solid #b0e0e6 !important;
        border-radius: 50px !important;  /* PILL SHAPE! */
        padding: 12px 24px !important;
        box-shadow: 0 3px 10px rgba(135, 206, 235, 0.2);
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #87ceeb !important;
        box-shadow: 0 0 15px rgba(135, 206, 235, 0.5);
        border-width: 4px !important;
    }

    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        color: #2c3e50 !important;
        background-color: white !important;
        border: 3px solid #b0e0e6 !important;
        border-radius: 50px !important;  /* PILL SHAPE! */
        padding: 8px 20px !important;
    }

    /* Text area - ROUNDED */
    .stTextArea > div > div > textarea {
        border-radius: 30px !important;
        border: 3px solid #b0e0e6 !important;
        padding: 15px 20px !important;
    }

    /* Labels - dark text for readability */
    label {
        color: #1e88e5 !important;
        font-weight: 600 !important;
    }

    /* Tabs styling - PILL SHAPED */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 50px !important;  /* PILL SHAPE! */
        padding: 8px;
        border: 3px solid rgba(255, 215, 0, 0.3);
    }

    .stTabs [data-baseweb="tab"] {
        color: #1e88e5 !important;
        font-weight: 700;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        margin: 0 5px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        transform: scale(1.05);
        background: rgba(135, 206, 235, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #87ceeb 0%, #5dade2 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 15px rgba(135, 206, 235, 0.5);
    }

    /* Progress bar - light blue */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #87ceeb 0%, #5dade2 100%);
    }

    /* Metrics - light styled */
    [data-testid="stMetricValue"] {
        color: #1e88e5 !important;
        font-weight: 700;
    }

    /* Chat messages - PILL SHAPED */
    .stChatMessage {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%) !important;
        border: 3px solid #b0e0e6;
        border-radius: 50px !important;  /* PILL SHAPE! */
        padding: 15px 25px !important;
        box-shadow: 0 3px 12px rgba(135, 206, 235, 0.3);
    }

    /* Triangle decorative elements */
    .main::after {
        content: '';
        position: fixed;
        bottom: 10%;
        left: 5%;
        width: 0;
        height: 0;
        border-left: 30px solid transparent;
        border-right: 30px solid transparent;
        border-bottom: 52px solid rgba(135, 206, 235, 0.3);
        animation: float 5s infinite ease-in-out;
        pointer-events: none;
        z-index: 1;
    }

    [data-testid="stSidebar"]::after {
        content: '';
        position: absolute;
        bottom: 15%;
        left: 10%;
        width: 0;
        height: 0;
        border-left: 25px solid transparent;
        border-right: 25px solid transparent;
        border-bottom: 43px solid rgba(255, 215, 0, 0.4);
        animation: sparkle 3s infinite;
    }

    /* Expandable sections - DIAMOND-ISH */
    .streamlit-expanderHeader {
        border-radius: 15px !important;
        border: 3px solid #b0e0e6 !important;
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%) !important;
        padding: 15px 20px !important;
    }

    /* Metric containers - CIRCLES */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 50% !important;
        padding: 20px !important;
        border: 4px solid rgba(135, 206, 235, 0.4);
        box-shadow: 0 5px 15px rgba(135, 206, 235, 0.3);
        min-width: 120px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Sparkle decorations throughout */
    h1::before, h2::before {
        content: '✨ ';
    }

    h1::after, h2::after {
        content: ' ✨';
    }

    /* Silver shimmer effect on hover for cards */
    .checklist-item::before,
    .idea-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(192, 192, 192, 0.2),
            transparent
        );
        transition: left 0.5s;
    }

    .checklist-item:hover::before,
    .idea-card:hover::before {
        left: 100%;
    }

    /* Trip code box - DIAMOND SHAPE */
    .trip-code-diamond {
        background: linear-gradient(135deg, #87ceeb 0%, #b0e0e6 100%);
        padding: 30px 60px;
        clip-path: polygon(15% 0%, 85% 0%, 100% 50%, 85% 100%, 15% 100%, 0% 50%);
        border: 5px solid rgba(255, 215, 0, 0.7);
        text-align: center;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 8px 25px rgba(135, 206, 235, 0.5);
        animation: magicPulse 3s infinite;
    }

    .trip-code-diamond h3 {
        color: white;
        margin: 0;
        font-size: 1.8em;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .trip-code-diamond p {
        color: white;
        margin: 10px 0 0 0;
        font-size: 1em;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }

    /* Alert boxes - CIRCULAR/PILL */
    .stAlert {
        border-radius: 50px !important;
        border-width: 3px !important;
        padding: 15px 30px !important;
    }

    /* Success/Info/Error boxes - PILL SHAPED */
    [data-testid="stNotification"] {
        border-radius: 50px !important;
        border-width: 3px !important;
    }

    /* Streamlit column overrides - remove square containers */
    [data-testid="column"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    [data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stHorizontalBlock"] {
        background: transparent !important;
        border: none !important;
    }

    /* Remove square borders from Streamlit containers */
    .element-container {
        border: none !important;
        background: transparent !important;
    }

    .stMarkdown {
        border: none !important;
        background: transparent !important;
    }

    /* Ensure our custom divs display properly */
    .stMarkdown > div {
        border: none !important;
        background: transparent !important;
    }

    /* MICKEY EARS CHECKBOXES - Soft and Magical */
    input[type="checkbox"] {
        appearance: none !important;
        -webkit-appearance: none !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        background: linear-gradient(135deg, #e8e8e8 0%, #d3d3d3 100%) !important;
        border-radius: 50% !important;
        position: relative !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
        border: 2px solid #c0c0c0 !important;
    }

    /* Mickey's left ear */
    input[type="checkbox"]::before {
        content: '' !important;
        position: absolute !important;
        width: 22px !important;
        height: 22px !important;
        background: linear-gradient(135deg, #e8e8e8 0%, #d3d3d3 100%) !important;
        border-radius: 50% !important;
        top: -10px !important;
        left: -4px !important;
        transition: all 0.3s ease !important;
        border: 2px solid #c0c0c0 !important;
    }

    /* Mickey's right ear */
    input[type="checkbox"]::after {
        content: '' !important;
        position: absolute !important;
        width: 22px !important;
        height: 22px !important;
        background: linear-gradient(135deg, #e8e8e8 0%, #d3d3d3 100%) !important;
        border-radius: 50% !important;
        top: -10px !important;
        right: -4px !important;
        transition: all 0.3s ease !important;
        border: 2px solid #c0c0c0 !important;
    }

    /* Checked state - golden Mickey! */
    input[type="checkbox"]:checked {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
        border-color: #ffc107 !important;
        animation: mickeyPop 0.4s ease-out !important;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5) !important;
    }

    input[type="checkbox"]:checked::before {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
        border-color: #ffc107 !important;
    }

    input[type="checkbox"]:checked::after {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important;
        border-color: #ffc107 !important;
    }

    @keyframes mickeyPop {
        0% { transform: scale(1); }
        50% { transform: scale(1.2) rotate(10deg); }
        100% { transform: scale(1); }
    }

    /* Filter Controls - Soft Princess Styling */
    .stCheckbox {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e9 100%) !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        border: 2px solid rgba(255, 192, 203, 0.4) !important;
        box-shadow: 0 2px 8px rgba(255, 182, 193, 0.2) !important;
    }

    .stCheckbox:hover {
        border-color: rgba(255, 192, 203, 0.6) !important;
        box-shadow: 0 3px 12px rgba(255, 182, 193, 0.3) !important;
    }

    .stMultiSelect > div {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%) !important;
        border-radius: 25px !important;
        padding: 8px !important;
        border: 2px solid rgba(135, 206, 235, 0.4) !important;
        box-shadow: 0 2px 8px rgba(135, 206, 235, 0.2) !important;
    }

    .stMultiSelect:hover > div {
        border-color: rgba(135, 206, 235, 0.6) !important;
        box-shadow: 0 3px 12px rgba(135, 206, 235, 0.3) !important;
    }

    /* Multi-select tags - soft pastel pills */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #ffb6c1 0%, #ffc0cb 100%) !important;
        border-radius: 20px !important;
        border: none !important;
        color: #fff !important;
        font-weight: 600 !important;
        padding: 4px 12px !important;
        margin: 2px !important;
    }

    /* Ghost placeholders */
    input::placeholder {
        color: rgba(135, 206, 235, 0.4) !important;
        opacity: 1 !important;
        font-style: italic !important;
    }

    textarea::placeholder {
        color: rgba(135, 206, 235, 0.4) !important;
        opacity: 1 !important;
        font-style: italic !important;
    }

    /* Disney Silhouettes - Subtle Floating decorations */
    body::before {
        content: '👑';
        position: fixed;
        top: 12%;
        right: 6%;
        font-size: 35px;
        opacity: 0.08;
        animation: float 6s infinite ease-in-out;
        pointer-events: none;
        z-index: 0;
        filter: grayscale(20%);
    }

    .main::before {
        content: '🌹';
        position: fixed;
        top: 35%;
        left: 3%;
        font-size: 38px;
        opacity: 0.07;
        animation: float 7s infinite ease-in-out 1s;
        pointer-events: none;
        z-index: 0;
        filter: grayscale(20%);
    }

    [data-testid="stSidebar"]::before {
        content: '🪝';
        position: absolute;
        top: 25%;
        right: 10%;
        font-size: 30px;
        opacity: 0.1;
        animation: sparkle 4s infinite;
        pointer-events: none;
        filter: grayscale(15%);
    }

    /* Additional floating silhouettes */
    .stApp::after {
        content: '🧚';
        position: fixed;
        bottom: 20%;
        right: 8%;
        font-size: 32px;
        opacity: 0.09;
        animation: float 5s infinite ease-in-out 2s;
        pointer-events: none;
        z-index: 0;
        filter: grayscale(20%);
    }

    /* Rapunzel's brush - floating decoration */
    .main::after {
        content: '🖌️';
        position: fixed;
        top: 65%;
        right: 4%;
        font-size: 33px;
        opacity: 0.08;
        animation: float 6.5s infinite ease-in-out 1.5s;
        pointer-events: none;
        z-index: 0;
        filter: grayscale(25%);
    }

    /* Login page beautification */
    .trip-code-entry {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 60px 40px;
        border-radius: 30px;
        border: 4px solid rgba(135, 206, 235, 0.5);
        box-shadow: 0 10px 40px rgba(135, 206, 235, 0.3);
        position: relative;
        overflow: hidden;
    }

    .trip-code-entry::before {
        content: '✨';
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 30px;
        animation: sparkle 2s infinite;
    }

    .trip-code-entry::after {
        content: '🏰';
        position: absolute;
        bottom: 20px;
        right: 20px;
        font-size: 50px;
        opacity: 0.1;
        animation: float 8s infinite ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence functions
DATA_DIR = Path.home() / ".disney_trip_planner"
DATA_FILE = DATA_DIR / "trip_data.pkl"

def save_trip_data():
    """Save trip data to Firebase and local disk"""
    data = {
        'trip_details': st.session_state.trip_details,
        'checklist': st.session_state.checklist,
        'ideas': st.session_state.ideas,
        'chat_history': st.session_state.chat_history,
        'rejected_items': st.session_state.get('rejected_items', set()),
        'pending_suggestions': st.session_state.get('pending_suggestions', [])
    }

    # Try Firebase first if trip code is set
    trip_code = st.session_state.get('trip_code')
    if trip_code:
        firebase = get_firebase_manager()
        if firebase.is_enabled():
            try:
                firebase.save_trip(trip_code, data)
            except Exception as e:
                st.warning(f"Could not save to cloud: {e}")

    # Always save locally as backup
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        st.warning(f"Could not save locally: {e}")

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
        st.session_state.ideas = saved_data.get('ideas', [])
        st.session_state.chat_history = saved_data.get('chat_history', [])
        # Ensure rejected_items is always a set (Firebase returns it as a list)
        rejected = saved_data.get('rejected_items', set())
        st.session_state.rejected_items = set(rejected) if isinstance(rejected, (list, set)) else set()
        st.session_state.pending_suggestions = saved_data.get('pending_suggestions', [])
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

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Your Personalized Checklist")
        with col2:
            if st.button("🔍 Find Forgotten Items"):
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

        # Filter options
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

                        action_col1, action_col2 = st.columns([5, 1], gap="small")
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

        # Add custom item
        st.markdown("---")
        st.subheader("➕ Add Custom Item")
        new_col1, new_col2, new_col3 = st.columns([3, 1, 1])
        with new_col1:
            new_item_text = st.text_input("Item description", key="new_item")
        with new_col2:
            new_item_category = st.text_input("Category", "custom", key="new_category")
        with new_col3:
            new_item_priority = st.selectbox("Priority", ["high", "medium", "low"], key="new_priority")

        if st.button("Add to Checklist") and new_item_text:
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
