#!/bin/bash
# run.sh — boot the Flask app with Gunicorn
# Creates venv if missing, installs deps, runs 4 workers on port 8000.

set -e  # exit on first error

APP_DIR="$(dirname "$(readlink -f "$0")")"
cd "$APP_DIR"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating venv and installing dependencies..."
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo "Starting Gunicorn on port 8000 with 4 workers..."
exec gunicorn --workers 4 --bind 0.0.0.0:8000 app:app