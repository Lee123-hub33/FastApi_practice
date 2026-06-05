# FastAPI & PostgreSQL Practice API

A modular, production-ready backend project built to master database connections, structured routing, and clean environment configurations.

## Tech Stack
* **Framework:** FastAPI
* **Database ORM:** SQLAlchemy
* **Database driver:** PostgreSQL (`psycopg2-binary`)
* **Package Manager:** `uv` (Blazing fast virtual environments)
* **Environment Management:** `python-dotenv`

## Key Learning Milestones Covered
1. **Separation of Concerns:** Isolated routes into `routers/`, data schemas into `schemas.py`, and core DB modeling into `models.py`.
2. **Secure Credentials:** Completely isolated database links outside of source control using localized `.env` variables.
3. **Dependency Injection:** Handled persistent connection pooling dynamically using FastAPI's `Depends()` lifecycle management.

## Getting Started Locally

1. Install dependencies using `uv`:
   ```bash
   uv add fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv