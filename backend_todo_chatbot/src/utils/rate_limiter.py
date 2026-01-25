import time
from collections import defaultdict
from functools import wraps
from fastapi import HTTPException


# Simple in-memory rate limiter (for demo purposes)
# In production, you'd use Redis or another distributed store
request_counts = defaultdict(list)


def rate_limit(max_calls: int, time_window: int):
    """
    Rate limiting decorator.

    Args:
        max_calls: Maximum number of calls allowed
        time_window: Time window in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get client identifier (in a real app, this might be IP or user ID)
            # For this implementation, we'll use a simple approach
            current_time = time.time()

            # Clean up old requests outside the time window
            client_key = f"{func.__name__}_global"  # Simplified for demo
            request_counts[client_key] = [
                req_time for req_time in request_counts[client_key]
                if current_time - req_time < time_window
            ]

            # Check if limit exceeded
            if len(request_counts[client_key]) >= max_calls:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: {max_calls} calls per {time_window} seconds"
                )

            # Add current request
            request_counts[client_key].append(current_time)

            # Call the original function
            return func(*args, **kwargs)

        return wrapper
    return decorator