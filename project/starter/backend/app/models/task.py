# project/starter/app/models/task.py
# Module 5 Project — Task model
#
# Define the Task ORM model
# Fields: id, title, description (optional), completed (bool, default False), owner_id (FK)
# Relationship: task belongs to a user
import enum
from sqlalchemy import Enum as SQLEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional
from app.database import Base

from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    # Add columns
    # Add owner_id ForeignKey to users.id
    # Add relationship to User (owner = relationship("User", back_populates="tasks"))

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner_id: Mapped[int] = mapped_column(
            ForeignKey("users.id"),
            nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )

    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        default=TaskPriority.medium,
        nullable=False
    )
