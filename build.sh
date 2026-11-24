
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --no-input

# Reset administrator password only when configured
if [ -n "${RESET_ADMIN_USERNAME:-}" ] || [ -n "${RESET_ADMIN_PASSWORD:-}" ]; then
    if [ -z "${RESET_ADMIN_USERNAME:-}" ] || [ -z "${RESET_ADMIN_PASSWORD:-}" ]; then
        echo "ERROR: Both admin reset variables must be configured."
        exit 1
    fi

    python manage.py reset_admin_password
fi

# Reset patient password only when configured
if [ -n "${RESET_PATIENT_USERNAME:-}" ] || [ -n "${RESET_PATIENT_PASSWORD:-}" ]; then
    if [ -z "${RESET_PATIENT_USERNAME:-}" ] || [ -z "${RESET_PATIENT_PASSWORD:-}" ]; then
        echo "ERROR: Both patient reset variables must be configured."
        exit 1
    fi

    python manage.py reset_patient_password
fi

# Report production data configuration
if [ -n "${PRODUCTION_DATA_B64:-}" ]; then
    echo "PRODUCTION_DATA_B64 is configured."
else
    echo "WARNING: PRODUCTION_DATA_B64 is not configured."
fi
