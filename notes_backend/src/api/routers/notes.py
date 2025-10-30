from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select, Session

from ..db import get_session
from ..models import Note
from ..schemas import NoteCreate, NoteRead, NoteUpdate, NotesListResponse

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note with a title and content.",
    responses={
        201: {"description": "Note created successfully"},
        422: {"description": "Validation Error"},
    },
)
# PUBLIC_INTERFACE
def create_note(payload: NoteCreate, session: Session = Depends(get_session)) -> NoteRead:
    """Create a new note and return the created entity."""
    note = Note(title=payload.title, content=payload.content)
    session.add(note)
    session.commit()
    session.refresh(note)
    return NoteRead.model_construct(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.get(
    "",
    response_model=NotesListResponse,
    summary="List notes",
    description="List notes with optional search by query 'q' across title and content. Supports pagination with 'limit' and 'offset'.",
)
# PUBLIC_INTERFACE
def list_notes(
    q: Optional[str] = Query(None, description="Search query for title or content"),
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    session: Session = Depends(get_session),
) -> NotesListResponse:
    """List notes with optional search and pagination."""
    statement = select(Note)
    count_statement = select(Note)

    if q:
        # Case-insensitive contains; SQLite uses LIKE which is case-insensitive by default for ASCII.
        like = f"%{q}%"
        statement = statement.where((Note.title.like(like)) | (Note.content.like(like)))
        count_statement = count_statement.where((Note.title.like(like)) | (Note.content.like(like)))

    total = session.exec(count_statement).all()
    total_count = len(total)

    statement = statement.order_by(Note.created_at.desc()).offset(offset).limit(limit)
    results = session.exec(statement).all()

    items = [
        NoteRead.model_construct(
            id=n.id,
            title=n.title,
            content=n.content,
            created_at=n.created_at,
            updated_at=n.updated_at,
        )
        for n in results
    ]

    return NotesListResponse(total=total_count, items=items)


@router.get(
    "/{note_id}",
    response_model=NoteRead,
    summary="Get a note by ID",
    description="Retrieve a single note by its unique identifier.",
    responses={
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def get_note(note_id: int, session: Session = Depends(get_session)) -> NoteRead:
    """Retrieve a note by ID."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteRead.model_construct(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.put(
    "/{note_id}",
    response_model=NoteRead,
    summary="Update a note",
    description="Update a note's title and/or content.",
    responses={
        404: {"description": "Note not found"},
        422: {"description": "Validation Error"},
    },
)
# PUBLIC_INTERFACE
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)) -> NoteRead:
    """Update a note by ID. At least one of title or content must be provided."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updated = False
    if payload.title is not None:
        note.title = payload.title
        updated = True
    if payload.content is not None:
        note.content = payload.content
        updated = True

    if not updated:
        # No-op update; treat as bad request
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No fields to update")

    from datetime import datetime
    note.updated_at = datetime.utcnow()

    session.add(note)
    session.commit()
    session.refresh(note)

    return NoteRead.model_construct(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its unique identifier.",
    responses={
        204: {"description": "Note deleted successfully"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def delete_note(note_id: int, session: Session = Depends(get_session)) -> None:
    """Delete a note by ID."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    session.delete(note)
    session.commit()
    return None
