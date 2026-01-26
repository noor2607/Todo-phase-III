from sqlmodel import Session, select
from typing import Optional
from database.models.user import User, UserCreate, UserUpdate, UserRead
from utils.hashing import hash_password, verify_password
from fastapi import HTTPException, status
from datetime import datetime
from utils.logging import get_logger
from auth.jwt_handler import create_access_token
from config.settings import settings

logger = get_logger(__name__)


class UserService:
    """Service class for handling user-related business logic"""

    @staticmethod
    def get_user_by_id(*, session: Session, user_id: str) -> Optional[UserRead]:
        """
        Get a user by their ID

        Args:
            session: Database session
            user_id: ID of the user to retrieve

        Returns:
            User as UserRead object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if user:
            logger.info(f"User retrieved: ID {user.id}")
            return UserRead.model_validate(user)

        logger.warning(f"User not found: ID {user_id}")
        return None

    @staticmethod
    def get_user_by_email(*, session: Session, email: str) -> Optional[UserRead]:
        """
        Get a user by their email

        Args:
            session: Database session
            email: Email of the user to retrieve

        Returns:
            User as UserRead object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if user:
            logger.info(f"User retrieved: ID {user.id} for email {email}")
            return UserRead.model_validate(user)

        logger.warning(f"User not found: email {email}")
        return None

    @staticmethod
    def get_user_by_username(*, session: Session, username: str) -> Optional[UserRead]:
        """
        Get a user by their username

        Args:
            session: Database session
            username: Username of the user to retrieve

        Returns:
            User as UserRead object if found, None otherwise
        """
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if user:
            logger.info(f"User retrieved: ID {user.id} for username {username}")
            return UserRead.model_validate(user)

        logger.warning(f"User not found: username {username}")
        return None

    @staticmethod
    def create_user(*, session: Session, user_create: UserCreate) -> UserRead:
        """
        Create a new user

        Args:
            session: Database session
            user_create: User creation data

        Returns:
            Created user as UserRead object
        """
        # Check if user with email already exists
        existing_user_by_email = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists"
            )

        # Check if user with username already exists
        existing_user_by_username = session.exec(select(User).where(User.username == user_create.username)).first()
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this username already exists"
            )

        # Hash the password
        hashed_password = hash_password(user_create.password)

        # Create the user object
        user = User(
            email=user_create.email,
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password,
            is_active=True
        )

        # Add to session and commit
        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(f"User created successfully: ID {user.id}")

        # Return the created user
        return UserRead.model_validate(user)

    @staticmethod
    def update_user(*, session: Session, user_id: str, user_update: UserUpdate) -> Optional[UserRead]:
        """
        Update a user

        Args:
            session: Database session
            user_id: ID of the user to update
            user_update: User update data

        Returns:
            Updated user as UserRead object if successful, None if user not found
        """
        # Get the existing user
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if not user:
            logger.warning(f"User not found for update: ID {user_id}")
            return None

        # Check if email is being updated and if it conflicts with another user
        if user_update.email is not None and user_update.email != user.email:
            existing_user = session.exec(select(User).where(User.email == user_update.email)).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists"
                )

        # Check if username is being updated and if it conflicts with another user
        if user_update.username is not None and user_update.username != user.username:
            existing_user = session.exec(select(User).where(User.username == user_update.username)).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this username already exists"
                )

        # Update the user fields
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        # Update the timestamp
        user.updated_at = datetime.utcnow()

        # Commit changes
        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(f"User updated successfully: ID {user.id}")

        # Return the updated user
        return UserRead.model_validate(user)

    @staticmethod
    def authenticate_user(*, session: Session, email: str, password: str) -> Optional[UserRead]:
        """
        Authenticate a user with email and password

        Args:
            session: Database session
            email: Email of the user
            password: Plain text password to verify

        Returns:
            User as UserRead object if authentication successful, None otherwise
        """
        # Get user by email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed for email: {email}")
            return None

        # Update last login time
        user.last_login_at = datetime.utcnow()
        session.add(user)
        session.commit()

        logger.info(f"User authenticated successfully: ID {user.id}")
        return UserRead.model_validate(user)

    @staticmethod
    def create_auth_token(user: UserRead) -> str:
        """
        Create an authentication token for a user

        Args:
            user: User object to create token for

        Returns:
            JWT token string
        """
        token_data = {
            "sub": user.id,
            "email": user.email,
            "username": user.username
        }
        token = create_access_token(token_data)
        logger.info(f"Authentication token created for user: {user.id}")
        return token