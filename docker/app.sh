#!/bin/bash
cd app
alembic upgrade head

cd ..
gunicorn app.main:app  --bind=0.0.0.0:8000