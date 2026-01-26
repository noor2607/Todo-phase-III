from fastapi import HTTPException, status
from typing import Dict, Any
from src.auth.jwt_handler import verify_token


def handle_invalid_token(error_detail: str = "Invalid or expired token") -> HTTPException:
    """
    Create a standardized HTTPException for invalid token scenarios

    Args:
        error_detail: Detail message for the exception

    Returns:
        HTTPException with 401 status code
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error_detail
    )


def handle_missing_token() -> HTTPException:
    """
    Create a standardized HTTPException for missing token scenarios

    Returns:
        HTTPException with 401 status code
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication token is required but missing"
    )


def validate_and_extract_user_id(authorization_header: str) -> str:
    """
    Validate the authorization header and extract user ID from the JWT token

    Args:
        authorization_header: The Authorization header value (e.g., "Bearer token...")

    Returns:
        User ID string from the token payload

    Raises:
        HTTPException: If token is invalid, missing, or expired
    """
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise handle_missing_token()

    token = authorization_header[len("Bearer "):]

    try:
        payload = verify_token(token)

        # Extract user_id from the payload
        user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")

        if not user_id:
            raise handle_invalid_token("Token does not contain valid user identification")

        return str(user_id)

    except HTTPException:
        # Re-raise HTTP exceptions (like expired token, invalid token)
        raise
    except Exception as e:
        raise handle_invalid_token(f"Token validation failed: {str(e)}")


def verify_token_authorization(authorization_header: str) -> Dict[str, Any]:
    """
    Verify the token in the authorization header and return the payload

    Args:
        authorization_header: The Authorization header value (e.g., "Bearer token...")

    Returns:
        Token payload dictionary

    Raises:
        HTTPException: If token is invalid, missing, or expired
    """
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise handle_missing_token()

    token = authorization_header[len("Bearer "):]

    try:
        payload = verify_token(token)
        return payload
    except HTTPException:
        # Re-raise HTTP exceptions (like expired token, invalid token)
        raise
    except Exception as e:
        raise handle_invalid_token(f"Token verification failed: {str(e)}")