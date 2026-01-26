from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt import PyJWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from config.settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload as dictionary

    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=[settings.jwt_algorithm])

        # Extract user_id from the payload (following Better Auth format)
        user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID found in token"
            )

        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )


def extract_user_id_from_token_payload(payload: Dict[str, Any]) -> str:
    """
    Extract user_id from the decoded JWT payload

    Args:
        payload: Decoded JWT payload dictionary

    Returns:
        User ID as string
    """
    # Check multiple possible keys for user ID based on Better Auth format
    user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user ID found in token"
        )

    return str(user_id)


def is_token_expired(payload: Dict[str, Any]) -> bool:
    """
    Check if the token is expired based on the 'exp' claim

    Args:
        payload: Decoded JWT payload dictionary

    Returns:
        True if token is expired, False otherwise
    """
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None:
        return True

    current_time = datetime.utcnow().timestamp()
    return current_time > exp_timestamp