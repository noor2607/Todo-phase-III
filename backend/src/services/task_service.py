from sqlmodel import Session, select
from typing import List, Optional
from database.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from utils.validators import validate_title_length
from fastapi import HTTPException, status
from datetime import datetime
from utils.logging import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service class for handling task-related business logic"""

    @staticmethod
    def create_task(*, session: Session, task_create: TaskCreate, user_id: str) -> TaskRead:
        """
        Create a new task for the specified user

        Args:
            session: Database session
            task_create: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created task as TaskRead object
        """
        # Validate title length
        if not validate_title_length(task_create.title):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title must be between 1 and 200 characters"
            )

        # Create the task object
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            due_date=task_create.due_date,
            user_id=user_id
        )

        # Add to session and commit
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task created successfully: ID {task.id} for user {user_id}")

        # Return the created task
        return TaskRead.model_validate(task)

    @staticmethod
    def get_task_by_id(*, session: Session, task_id: int, user_id: str) -> Optional[TaskRead]:
        """
        Get a task by its ID for the specified user

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task as TaskRead object if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if task:
            logger.info(f"Task retrieved: ID {task.id} for user {user_id}")
            return TaskRead.model_validate(task)

        logger.warning(f"Task not found or not owned by user: ID {task_id} for user {user_id}")
        return None

    @staticmethod
    def get_tasks_for_user(*, session: Session, user_id: str, status_filter: Optional[str] = None, sort_by: Optional[str] = None) -> List[TaskRead]:
        """
        Get all tasks for the specified user with optional filtering and sorting

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            status_filter: Optional filter for task status ('all', 'completed', 'pending')
            sort_by: Optional sort field ('created_at', 'due_date', 'title')

        Returns:
            List of tasks as TaskRead objects
        """
        # Build the query
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status_filter and status_filter != 'all':
            if status_filter == 'completed':
                statement = statement.where(Task.completed == True)
            elif status_filter == 'pending':
                statement = statement.where(Task.completed == False)

        # Apply sorting
        if sort_by == 'due_date':
            statement = statement.order_by(Task.due_date)
        elif sort_by == 'title':
            statement = statement.order_by(Task.title)
        else:  # Default to created_at
            statement = statement.order_by(Task.created_at.desc())

        tasks = session.exec(statement).all()

        logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")

        # Convert to TaskRead objects
        task_reads = []
        for task in tasks:
            task_read = TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead(**task.dict())
            task_reads.append(task_read)

        return task_reads

    @staticmethod
    def update_task(*, session: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[TaskRead]:
        """
        Update a task for the specified user

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Task update data
            user_id: ID of the user updating the task

        Returns:
            Updated task as TaskRead object if successful, None if task not found or not owned
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found or not owned by user for update: ID {task_id} for user {user_id}")
            return None

        # Validate title if it's being updated
        if task_update.title is not None and not validate_title_length(task_update.title):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title must be between 1 and 200 characters"
            )

        # Update the task fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task updated successfully: ID {task.id} for user {user_id}")

        # Return the updated task
        return TaskRead.model_validate(task)

    @staticmethod
    def toggle_task_completion(*, session: Session, task_id: int, user_id: str) -> Optional[TaskRead]:
        """
        Toggle the completion status of a task for the specified user

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user toggling the task

        Returns:
            Updated task as TaskRead object if successful, None if task not found or not owned
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found or not owned by user for toggle: ID {task_id} for user {user_id}")
            return None

        # Toggle the completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task completion toggled: ID {task.id}, completed={task.completed} for user {user_id}")

        # Return the updated task
        return TaskRead.model_validate(task)

    @staticmethod
    def delete_task(*, session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a task for the specified user

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user deleting the task

        Returns:
            True if task was deleted, False if task not found or not owned
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found or not owned by user for deletion: ID {task_id} for user {user_id}")
            return False

        # Delete the task
        session.delete(task)
        session.commit()

        logger.info(f"Task deleted successfully: ID {task_id} for user {user_id}")

        return True