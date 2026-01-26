from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from database.engine import get_session
from services.user_service import UserService
from database.models.user import UserRegister, UserLogin, UserRead, UserUpdate
from auth.dependencies import get_current_user
from schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserProfileResponse,
    AuthErrorResponse
)
from utils.logging import get_logger
from datetime import datetime

router = APIRouter()
logger = get_logger(__name__)


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_register: UserRegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user
    """
    try:
        # Prepare the user creation data
        user_to_create = UserRegister(
            email=user_register.email,
            username=user_register.username,
            password=user_register.password,
            first_name=getattr(user_register, 'first_name', None),
            last_name=getattr(user_register, 'last_name', None),
            is_active=True
        )

        # Create the user
        created_user = UserService.create_user(
            session=session,
            user_create=user_to_create
        )

        # Create authentication token
        auth_token = UserService.create_auth_token(created_user)

        logger.info(f"User registered successfully: ID {created_user.id}")

        return UserRegisterResponse(
            success=True,
            data={
                "user": created_user,
                "token": auth_token
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user {user_register.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while registering user"
        )


@router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_login: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return token
    """
    try:
        # Authenticate the user
        authenticated_user = UserService.authenticate_user(
            session=session,
            email=user_login.email,
            password=user_login.password
        )

        if not authenticated_user:
            logger.warning(f"Failed login attempt for email: {user_login.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create authentication token
        auth_token = UserService.create_auth_token(authenticated_user)

        logger.info(f"User logged in successfully: ID {authenticated_user.id}")

        return UserLoginResponse(
            success=True,
            data={
                "user": authenticated_user,
                "token": auth_token
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user {user_login.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while logging in"
        )


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get the profile information for the currently authenticated user
    """
    try:
        # Get user by ID
        user = UserService.get_user_by_id(
            session=session,
            user_id=current_user_id
        )

        if not user:
            logger.error(f"Authenticated user not found in database: ID {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User account could not be found"
            )

        logger.info(f"User profile retrieved: ID {user.id}")

        return UserProfileResponse(
            success=True,
            data=user
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving profile"
        )


@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    user_update: UserRegisterRequest,  # Using the request schema for updates
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update the profile information for the currently authenticated user
    """
    try:
        # Prepare the user update data
        user_to_update = UserUpdate(
            email=getattr(user_update, 'email', None),
            username=getattr(user_update, 'username', None),
            first_name=getattr(user_update, 'first_name', None),
            last_name=getattr(user_update, 'last_name', None)
        )

        # Update the user
        updated_user = UserService.update_user(
            session=session,
            user_id=current_user_id,
            user_update=user_to_update
        )

        if not updated_user:
            logger.error(f"Authenticated user not found in database: ID {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User account could not be found"
            )

        logger.info(f"User profile updated: ID {updated_user.id}")

        return UserProfileResponse(
            success=True,
            data=updated_user
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating profile"
        )