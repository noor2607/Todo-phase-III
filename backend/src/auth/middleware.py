from fastapi import Request, HTTPException, status
from typing import Optional, Dict, Any
from auth.jwt_handler import verify_token


class JWTVerificationMiddleware:
    """
    Middleware class to verify JWT tokens for protected routes
    """

    def __init__(self):
        pass

    async def verify_token_in_request(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token in the request Authorization header

        Args:
            request: FastAPI request object

        Returns:
            Decoded token payload if valid, None if invalid/missing
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated, Authorization header missing or invalid format"
            )

        token = auth_header[len("Bearer "):]

        try:
            payload = verify_token(token)
            return payload
        except HTTPException:
            # Re-raise HTTP exceptions (like expired token, invalid token)
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

    async def verify_token_exists_only(self, request: Request) -> bool:
        """
        Verify that a token exists and is valid without returning the payload

        Args:
            request: FastAPI request object

        Returns:
            True if token is valid, raises HTTPException if invalid/missing
        """
        await self.verify_token_in_request(request)
        return True


# Create a singleton instance of the middleware
jwt_middleware = JWTVerificationMiddleware()