from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from database.engine import get_session
from auth.dependencies import get_current_user
from services.task_service import TaskService
from database.models.task import TaskCreate, TaskUpdate
from schemas.task import (
    TaskCreate as TaskCreateSchema,
    TaskUpdate as TaskUpdateSchema,
    TaskResponse,
    TaskListResponse,
    TaskSingleResponse,
    TaskToggleComplete,
    TaskDeleteResponse,
    ErrorResponse
)
from utils.logging import get_logger
from datetime import datetime

router = APIRouter()

logger = get_logger(__name__)


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter tasks by completion status"),
    sort_by: Optional[str] = Query(None, alias="sort", description="Sort tasks by field"),
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional filtering and sorting
    """
    try:
        # Validate query parameters
        if status_filter and status_filter not in ["all", "completed", "pending"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status parameter. Use 'all', 'completed', or 'pending'"
            )

        if sort_by and sort_by not in ["created_at", "due_date", "title"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sort parameter. Use 'created_at', 'due_date', or 'title'"
            )

        # Get tasks for the current user
        tasks = TaskService.get_tasks_for_user(
            session=session,
            user_id=current_user,
            status_filter=status_filter,
            sort_by=sort_by
        )

        # Convert to response format
        task_responses = []
        for task in tasks:
            task_response = TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                due_date=task.due_date,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_responses.append(task_response)

        logger.info(f"Retrieved {len(tasks)} tasks for user {current_user}")

        return TaskListResponse(success=True, data=task_responses)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving tasks"
        )


@router.post("/tasks", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreateSchema,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    try:
        # Prepare the task creation data
        task_to_create = TaskCreate(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            due_date=task_create.due_date,
            user_id=current_user  # Set user_id from authenticated user
        )

        # Create the task
        created_task = TaskService.create_task(
            session=session,
            task_create=task_to_create,
            user_id=current_user
        )

        # Convert to response format
        task_response = TaskResponse(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            completed=created_task.completed,
            due_date=created_task.due_date,
            user_id=created_task.user_id,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )

        logger.info(f"Created task {created_task.id} for user {current_user}")

        return TaskSingleResponse(success=True, data=task_response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while creating task"
        )


@router.get("/tasks/{task_id}", response_model=TaskSingleResponse)
def get_task(
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user
    """
    try:
        # Get the task
        task = TaskService.get_task_by_id(
            session=session,
            task_id=task_id,
            user_id=current_user
        )

        if not task:
            logger.warning(f"Task {task_id} not found or not owned by user {current_user}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Convert to response format
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

        logger.info(f"Retrieved task {task_id} for user {current_user}")

        return TaskSingleResponse(success=True, data=task_response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving task"
        )


@router.put("/tasks/{task_id}", response_model=TaskSingleResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdateSchema,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user
    """
    try:
        # Prepare the task update data
        task_to_update = TaskUpdate(
            title=task_update.title,
            description=task_update.description,
            completed=task_update.completed,
            due_date=task_update.due_date
        )

        # Update the task
        updated_task = TaskService.update_task(
            session=session,
            task_id=task_id,
            task_update=task_to_update,
            user_id=current_user
        )

        if not updated_task:
            logger.warning(f"Task {task_id} not found or not owned by user {current_user}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Convert to response format
        task_response = TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

        logger.info(f"Updated task {task_id} for user {current_user}")

        return TaskSingleResponse(success=True, data=task_response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating task"
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskSingleResponse)
def toggle_task_completion(
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    try:
        # Toggle the task completion status
        updated_task = TaskService.toggle_task_completion(
            session=session,
            task_id=task_id,
            user_id=current_user
        )

        if not updated_task:
            logger.warning(f"Task {task_id} not found or not owned by user {current_user}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Convert to response format
        task_response = TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
            due_date=updated_task.due_date,
            user_id=updated_task.user_id,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at
        )

        logger.info(f"Toggled completion status for task {task_id} (now {updated_task.completed}) for user {current_user}")

        return TaskSingleResponse(success=True, data=task_response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling task completion {task_id} for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while toggling task completion"
        )


@router.delete("/tasks/{task_id}", response_model=TaskDeleteResponse)
def delete_task(
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    try:
        # Delete the task
        success = TaskService.delete_task(
            session=session,
            task_id=task_id,
            user_id=current_user
        )

        if not success:
            logger.warning(f"Task {task_id} not found or not owned by user {current_user}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Deleted task {task_id} for user {current_user}")

        return TaskDeleteResponse(
            success=True,
            data={"message": "Task deleted successfully"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {current_user}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while deleting task"
        )