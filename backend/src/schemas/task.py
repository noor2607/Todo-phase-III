from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    """Base schema for task operations"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    title: str  # Enforce title is required


class TaskUpdate(BaseModel):
    """Schema for updating task fields"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response with ID and timestamps"""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskToggleComplete(BaseModel):
    """Schema for toggling task completion"""
    completed: bool


class TaskListResponse(BaseModel):
    """Schema for listing multiple tasks"""
    success: bool = True
    data: List[TaskResponse]


class TaskSingleResponse(BaseModel):
    """Schema for single task response"""
    success: bool = True
    data: TaskResponse


class TaskDeleteResponse(BaseModel):
    """Schema for task deletion response"""
    success: bool = True
    data: dict


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool
    error: str