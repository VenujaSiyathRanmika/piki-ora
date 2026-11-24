
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --no-input

if [ -n "${RESET_ADMIN_USERNAME:-}" ] || [ -n "${RESET_ADMIN_PASSWORD:-}" ]; then
    if [ -z "${RESET_ADMIN_USERNAME:-}" ] || [ -z "${RESET_ADMIN_PASSWORD:-}" ]; then
        echo "ERROR: Both reset variables must be configured."
        exit 1
    fi

    python manage.py reset_admin_password
fi

if [ -n "${PRODUCTION_DATA_B64:-}" ]; then
    echo "PRODUCTION_DATA_B64 is configured."
else
    echo "WARNING: PRODUCTION_DATA_B64 is not configured."
fi
