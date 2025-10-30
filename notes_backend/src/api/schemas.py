from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the note")
    content: str = Field(..., min_length=1, description="Content of the note")


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated title")
    content: Optional[str] = Field(None, min_length=1, description="Updated content")


class NoteRead(NoteBase):
    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class NotesListResponse(BaseModel):
    total: int = Field(..., description="Total number of notes matching the query")
    items: list[NoteRead] = Field(..., description="List of notes for the current page")
