from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
import uuid
import enum

import uuid
import enum
from datetime import datetime

Base = declarative_base()

class TaskStatus(enum.Enum):
    queued = 'queued'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    image_path = Column(String, nullable=False)
    metadata = Column(JSON)
    status = Column(Enum(TaskStatus), default=TaskStatus.queued)
    result_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

