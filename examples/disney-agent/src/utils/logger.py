"""
Logging utility for Disney Trip Planner
Structured logging with context and proper error handling
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Any
import streamlit as st

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_DIR = Path.home() / '.disney_trip_planner' / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Create log file with timestamp
log_file = LOG_DIR / f'app_{datetime.now().strftime("%Y%m%d")}.log'

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('DisneyTripPlanner')


# ============================================================================
# LOGGING HELPERS
# ============================================================================
def log_info(message: str, context: Optional[dict] = None):
    """Log informational message with optional context"""
    if context:
        message = f"{message} | Context: {context}"
    logger.info(message)


def log_warning(message: str, context: Optional[dict] = None):
    """Log warning message with optional context"""
    if context:
        message = f"{message} | Context: {context}"
    logger.warning(message)


def log_error(message: str, error: Optional[Exception] = None, context: Optional[dict] = None):
    """Log error message with exception details and context"""
    if error:
        message = f"{message} | Error: {str(error)}"
    if context:
        message = f"{message} | Context: {context}"
    logger.error(message, exc_info=error is not None)


def log_debug(message: str, context: Optional[dict] = None):
    """Log debug message with optional context"""
    if context:
        message = f"{message} | Context: {context}"
    logger.debug(message)


# ============================================================================
# USER-FACING ERROR MESSAGES
# ============================================================================
def show_error(message: str, error: Optional[Exception] = None, display_to_user: bool = True):
    """
    Log error and optionally display to user

    Args:
        message: User-friendly error message
        error: Original exception (logged but not shown to user)
        display_to_user: Whether to show message in UI
    """
    # Log the full error
    log_error(message, error)

    # Show user-friendly message
    if display_to_user:
        st.error(f"❌ {message}")


def show_warning(message: str, display_to_user: bool = True):
    """Log warning and optionally display to user"""
    log_warning(message)

    if display_to_user:
        st.warning(f"⚠️ {message}")


def show_info(message: str, display_to_user: bool = True):
    """Log info and optionally display to user"""
    log_info(message)

    if display_to_user:
        st.info(f"ℹ️ {message}")


def show_success(message: str, display_to_user: bool = True):
    """Log success and optionally display to user"""
    log_info(f"SUCCESS: {message}")

    if display_to_user:
        st.success(f"✅ {message}")


# ============================================================================
# CONTEXT MANAGERS FOR OPERATIONS
# ============================================================================
class OperationContext:
    """Context manager for tracking operations with logging"""

    def __init__(self, operation_name: str, context: Optional[dict] = None):
        self.operation_name = operation_name
        self.context = context or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        log_info(f"Starting: {self.operation_name}", self.context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()

        if exc_type is None:
            log_info(f"Completed: {self.operation_name} ({duration:.2f}s)", self.context)
        else:
            log_error(
                f"Failed: {self.operation_name} ({duration:.2f}s)",
                error=exc_val,
                context=self.context
            )

        # Don't suppress exceptions
        return False


# ============================================================================
# SAFE EXECUTION WRAPPER
# ============================================================================
def safe_execute(
    operation: callable,
    error_message: str,
    default_return: Any = None,
    show_user_error: bool = False,
    context: Optional[dict] = None
) -> Any:
    """
    Safely execute an operation with proper error handling

    Args:
        operation: Function to execute
        error_message: User-friendly error message if operation fails
        default_return: Value to return on error
        show_user_error: Whether to show error in UI
        context: Additional context for logging

    Returns:
        Operation result or default_return on error
    """
    try:
        return operation()
    except Exception as e:
        if show_user_error:
            show_error(error_message, e, display_to_user=True)
        else:
            log_error(error_message, e, context)
        return default_return


# ============================================================================
# API CALL WRAPPER
# ============================================================================
def log_api_call(
    api_name: str,
    endpoint: str,
    params: Optional[dict] = None,
    response_summary: Optional[str] = None
):
    """Log API calls for debugging and cost tracking"""
    context = {
        'api': api_name,
        'endpoint': endpoint,
        'params': params or {}
    }

    if response_summary:
        context['response'] = response_summary

    log_info(f"API Call: {api_name}", context)
