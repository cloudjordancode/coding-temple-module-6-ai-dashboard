# project/starter/app/schemas/task.py
# Module 5 Project — Task schemas
#
# TODO: Define TaskCreate, TaskPatch, TaskResponse

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models.task import TaskPriority

class TaskCreate(BaseModel):
    """Input for creating a task."""
    # TODO: title, description (optional), completed (default False)
    title: str = Field(
        min_length=1,
        max_length=200
    )
    description: Optional[str] = Field(
        default=None, max_length=2000
    )
    completed: bool = False

    priority: TaskPriority = TaskPriority.medium

class TaskPatch(BaseModel):
    """Input for partial task update."""
    # all Optional fields
    title: Optional[str] = Field(
        min_length=1,
        max_length=200,
        default=None
    )
    description: Optional[str] = Field(
        default=None, max_length=2000
    )
    completed: Optional[bool] = None

    priority: Optional[TaskPriority] = None

class TaskResponse(TaskCreate):
    """Returned to clients."""
    #  id, owner_id + model_config
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
