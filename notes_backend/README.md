# Notes Backend (FastAPI)

A simple FastAPI service providing CRUD operations for personal notes with SQLite persistence.

## Features

- FastAPI with Pydantic validation
- SQLite persistence via SQLModel
- CRUD endpoints:
  - POST /notes
  - GET /notes
  - GET /notes/{id}
  - PUT /notes/{id}
  - DELETE /notes/{id}
  - GET /health
- CORS enabled (allow all)
- Pagination (limit, offset) and search (`q`) on GET /notes
- OpenAPI docs at `/docs` and JSON at `/openapi.json`

## Configuration

Environment variables (optional):

- `DATABASE_URL`: SQLAlchemy-style DB URL. Defaults to `sqlite:///notes.db`.
- `NOTES_DB_PATH`: When `DATABASE_URL` is not set, the SQLite file path. Defaults to `notes.db`.

See `.env.example` for reference.

## Project Structure

```
notes_backend/
  src/api/
    __init__.py
    main.py
    db.py
    models.py
    schemas.py
    routers/
      notes.py
```

## Running

The environment is configured to run automatically in the preview system. If running locally:

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload --port 3001
```

Then open: http://localhost:3001/docs

## API Usage Examples (curl)

- Health:

```bash
curl -s http://localhost:3001/health
```

- Create note:

```bash
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First Note","content":"Hello world"}'
```

- List notes (with pagination and search):

```bash
curl -s "http://localhost:3001/notes?limit=10&offset=0&q=first"
```

- Get note by ID:

```bash
curl -s http://localhost:3001/notes/1
```

- Update note:

```bash
curl -s -X PUT http://localhost:3001/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'
```

- Delete note:

```bash
curl -s -X DELETE http://localhost:3001/notes/1 -o /dev/null -w "%{http_code}\n"
```

## Notes

- Tables are auto-created on startup.
- SQLite is used by default; data persists to `notes.db` in the container/service working directory.
