from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    """
    SQLModel table representing a Note.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(nullable=False, index=True, description="Short title for the note")
    content: str = Field(nullable=False, description="Full text content of the note")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
