from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

    # 'default' generates the timestamp locally in Python immediately during the insert transaction
    created_at = Column(DateTime(timezone=True), default=func.now(), server_default=func.now())
    priority = Column(String, server_default="medium", nullable=False)