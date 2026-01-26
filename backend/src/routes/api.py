from fastapi import APIRouter, Depends, HTTPException, status, Request
from auth.dependencies import get_current_user
from auth.middleware import jwt_middleware


router = APIRouter()


@router.get("/auth/verify")
async def verify_authentication(request: Request):
    """
    Verify that the incoming request has a valid authentication token.
    This endpoint can be used to check if a user is authenticated.
    """
    try:
        # This will raise an exception if token is invalid
        user_id = await jwt_middleware.verify_token_exists_only(request)

        return {
            "authenticated": True,
            "message": "Valid authentication token provided"
        }
    except HTTPException:
        raise


@router.get("/auth/profile")
async def get_user_profile(current_user: str = Depends(get_current_user)):
    """
    Get the profile information for the currently authenticated user.
    """
    return {
        "user_id": current_user,
        "message": "User profile retrieved successfully"
    }


@router.get("/auth/test-protected")
async def test_protected_route(current_user: str = Depends(get_current_user)):
    """
    A test endpoint that requires authentication.
    This can be used to verify that the authentication system is working properly.
    """
    return {
        "user_id": current_user,
        "message": "Successfully accessed protected route"
    }