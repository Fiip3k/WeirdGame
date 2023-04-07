#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
python manage.py collectstatic --no-input
pip install -r requirements.txt