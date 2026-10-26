# project/starter/app/models/user.py
# Module 5 Project — User model
#
# Define the User ORM model
# Fields: id, username (unique), email (unique), hashed_password
# Relationship: one user has many tasks

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base
from sqlalchemy import Boolean, DateTime, func
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    # Add columns
    # Add relationship to Task (tasks = relationship("Task", back_populates="owner"))

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )