#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py migrate --noinput

python manage.py collectstatic --no-input

if [ -n "${PRODUCTION_DATA_B64:-}" ]; then
    echo "$PRODUCTION_DATA_B64" | base64 --decode > production_data.json

    python manage.py loaddata production_data.json

    rm production_data.json
fi