from typing import Dict, Any, List, Optional
from ..services import TaskService
from ..models import TaskCreate, TaskUpdate
from sqlmodel import Session
from ..database import get_db_session
import functools


# Mock decorator for function_tool if mcp_sdk is not available
def function_tool(func):
    """Mock function_tool decorator for development purposes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@function_tool
def add_task(user_id: int, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new task for the user.

    Args:
        user_id: The ID of the user who owns the task
        title: The title of the task
        description: Detailed description of the task (optional)

    Returns:
        Dictionary with task_id, title, description, and completed status
    """
    # Validate inputs
    if not title or len(title.strip()) == 0:
        raise ValueError("Title is required and cannot be empty")

    if len(title) > 255:
        raise ValueError("Title must be 255 characters or less")

    if description and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")

    # Get database session
    db_session: Session = next(get_db_session())

    try:
        # Validate that user_id exists (in a real system, you'd validate against a users table)
        # For now, we'll just ensure it's a positive integer
        if user_id <= 0:
            raise ValueError("user_id must be a positive integer")

        # Create task data
        task_create = TaskCreate(
            title=title.strip(),
            description=description.strip() if description else None
        )

        # Create the task using the service
        task_service = TaskService()
        task = task_service.create_task(db_session, task_create)

        # Verify the task belongs to the user
        if task.user_id != user_id:
            raise ValueError("Unauthorized: Task does not belong to user")

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    finally:
        db_session.close()


@function_tool
def list_tasks(user_id: int, status: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieves tasks for the specified user with optional status filter.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status: Filter tasks by status ("all", "active", "completed"); defaults to "all"

    Returns:
        Dictionary with tasks list containing task_id, title, and completed status
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    valid_statuses = ["all", "active", "completed", None]
    if status not in valid_statuses:
        raise ValueError(f"status must be one of: {', '.join([s for s in valid_statuses if s is not None])}")

    # Get database session
    db_session: Session = next(get_db_session())

    try:
        # Get tasks using the service
        task_service = TaskService()
        tasks = task_service.get_tasks_by_user(db_session, user_id, status)

        # Format the response
        task_list = []
        for task in tasks:
            task_list.append({
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed
            })

        return {"tasks": task_list}
    finally:
        db_session.close()


@function_tool
def complete_task(user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Marks a user's task as completed.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as completed

    Returns:
        Dictionary with task_id, completed status, and title
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    # Get database session
    db_session: Session = next(get_db_session())

    try:
        # Attempt to complete the task
        task_service = TaskService()
        task = task_service.complete_task(db_session, task_id, user_id)

        if not task:
            raise ValueError(f"No task found with id {task_id} for user {user_id}")

        return {
            "task_id": task.id,
            "completed": task.completed,
            "title": task.title
        }
    finally:
        db_session.close()


@function_tool
def delete_task(user_id: int, task_id: int) -> Dict[str, Any]:
    """
    Deletes a user's task.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete

    Returns:
        Dictionary with task_id and deleted status
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    # Get database session
    db_session: Session = next(get_db_session())

    try:
        # Attempt to delete the task
        task_service = TaskService()
        success = task_service.delete_task(db_session, task_id, user_id)

        if not success:
            raise ValueError(f"No task found with id {task_id} for user {user_id}")

        return {
            "task_id": task_id,
            "deleted": True
        }
    finally:
        db_session.close()


@function_tool
def update_task(user_id: int, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Updates a user's task details.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dictionary with task_id, title, description, and updated status
    """
    # Validate inputs
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if task_id <= 0:
        raise ValueError("task_id must be a positive integer")

    if title and (len(title) == 0 or len(title) > 255):
        raise ValueError("Title must be between 1 and 255 characters if provided")

    if description and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less if provided")

    # Get database session
    db_session: Session = next(get_db_session())

    try:
        # Prepare update data
        task_update = TaskUpdate(
            title=title.strip() if title else None,
            description=description.strip() if description else None
        )

        # Attempt to update the task
        task_service = TaskService()
        task = task_service.update_task(db_session, task_id, user_id, task_update)

        if not task:
            raise ValueError(f"No task found with id {task_id} for user {user_id}")

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "updated": True
        }
    finally:
        db_session.close()