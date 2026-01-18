from typing import Optional
from datetime import datetime


def validate_title_length(title: str) -> bool:
    """
    Validate that title is between 1 and 200 characters

    Args:
        title: Task title to validate

    Returns:
        True if title length is valid, False otherwise
    """
    if not title:
        return False

    return 1 <= len(title) <= 200


def validate_due_date_format(due_date_str: Optional[str]) -> bool:
    """
    Validate that due date string is in ISO format (YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD)

    Args:
        due_date_str: Due date string to validate

    Returns:
        True if date format is valid, False otherwise
    """
    if due_date_str is None:
        return True  # Allow None/empty due dates

    try:
        # Try parsing as ISO format datetime
        datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        try:
            # Try parsing as date only
            datetime.strptime(due_date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by stripping whitespace and limiting length

    Args:
        text: Input text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Strip leading/trailing whitespace
    sanitized = text.strip()

    # Limit length to prevent extremely long inputs
    return sanitized[:1000]  # Reasonable limit for titles and descriptions