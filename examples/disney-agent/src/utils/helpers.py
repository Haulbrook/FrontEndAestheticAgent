"""
Utility functions for the Disney Trip Planning Agent
"""
from datetime import datetime, timedelta
from typing import Tuple
import pytz


def calculate_countdown(target_date: datetime) -> Tuple[int, int, int, int]:
    """
    Calculate countdown to trip date

    Returns:
        Tuple of (days, hours, minutes, seconds) until trip
    """
    now = datetime.now(pytz.UTC)
    if target_date.tzinfo is None:
        target_date = pytz.UTC.localize(target_date)

    delta = target_date - now

    if delta.total_seconds() < 0:
        return (0, 0, 0, 0)

    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return (days, hours, minutes, seconds)


def format_countdown(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format countdown as a readable string"""
    if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
        return "🎉 It's trip time! 🎉"

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 and days == 0:  # Only show seconds if less than a day
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)


def get_trip_phase(trip_date: datetime) -> str:
    """
    Determine which phase of trip planning we're in

    Returns:
        Phase name: "early", "mid", "final", or "imminent"
    """
    now = datetime.now(pytz.UTC)
    if trip_date.tzinfo is None:
        trip_date = pytz.UTC.localize(trip_date)

    days_until = (trip_date - now).days

    if days_until > 90:
        return "early"
    elif days_until > 30:
        return "mid"
    elif days_until > 7:
        return "final"
    else:
        return "imminent"


def generate_checklist_id() -> str:
    """Generate a unique ID for checklist items"""
    from uuid import uuid4
    return str(uuid4())
