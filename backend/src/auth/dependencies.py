from fastapi import Depends, HTTPException, status, Request
from typing import Dict, Any
from auth.jwt_handler import verify_token, extract_user_id_from_token_payload


def get_current_user(request: Request) -> str:
    """
    Dependency to get the current user ID from the JWT token in the request

    Args:
        request: FastAPI request object containing the Authorization header

    Returns:
        User ID as string extracted from the JWT token

    Raises:
        HTTPException: If no valid token is provided or if token is invalid
    """
    # Get the authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated, Authorization header missing or invalid format"
        )

    # Extract the token (remove "Bearer " prefix)
    token = auth_header[len("Bearer "):]

    # Verify the token and get the payload
    payload = verify_token(token)

    # Extract user_id from the payload
    user_id = extract_user_id_from_token_payload(payload)

    return user_id


def get_current_user_optional(request: Request) -> str:
    """
    Optional dependency to get the current user ID, allowing unauthenticated requests

    Args:
        request: FastAPI request object containing the Authorization header

    Returns:
        User ID as string if token is valid, None otherwise
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated, Authorization header missing or invalid format"
        )

    token = auth_header[len("Bearer "):]
    payload = verify_token(token)
    user_id = extract_user_id_from_token_payload(payload)

    return user_id


def require_user_identity(payload: Dict[str, Any], expected_user_id: str) -> bool:
    """
    Verify that the user identity in the token matches the expected user ID

    Args:
        payload: Decoded JWT payload
        expected_user_id: The user ID that should match the token's user ID

    Returns:
        True if user identity matches, raises HTTPException otherwise
    """
    token_user_id = extract_user_id_from_token_payload(payload)

    if token_user_id != expected_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User identity does not match expected user"
        )

    return True