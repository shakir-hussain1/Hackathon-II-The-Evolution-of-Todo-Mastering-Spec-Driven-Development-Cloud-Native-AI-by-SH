#!/usr/bin/env bash
# Render startup script for FastAPI backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations (create tables)
python -c "from src.db.database import create_db_and_tables; create_db_and_tables()"

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port $PORT
