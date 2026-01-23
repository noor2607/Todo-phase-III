from sqlmodel import Session, select
from typing import List, Optional
from ..models import Task, TaskCreate, TaskUpdate


class TaskService:
    def create_task(self, db_session: Session, task_data: TaskCreate) -> Task:
        """Create a new task for a user."""
        task = Task.from_orm(task_data)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    def get_tasks_by_user(self, db_session: Session, user_id: int, status: Optional[str] = None) -> List[Task]:
        """Retrieve tasks for a specific user with optional status filter."""
        query = select(Task).where(Task.user_id == user_id)

        if status == "active":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        # If status is "all" or None, return all tasks

        return db_session.exec(query).all()

    def get_task_by_id(self, db_session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Get a specific task by ID for a user."""
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return db_session.exec(query).first()

    def update_task(self, db_session: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task for a user."""
        task = self.get_task_by_id(db_session, task_id, user_id)
        if not task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = task.__class__.updated_at.default_factory()
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    def delete_task(self, db_session: Session, task_id: int, user_id: int) -> bool:
        """Delete a task for a user."""
        task = self.get_task_by_id(db_session, task_id, user_id)
        if not task:
            return False

        db_session.delete(task)
        db_session.commit()
        return True

    def complete_task(self, db_session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Mark a task as completed for a user."""
        task = self.get_task_by_id(db_session, task_id, user_id)
        if not task:
            return None

        task.completed = True
        task.updated_at = task.__class__.updated_at.default_factory()
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task