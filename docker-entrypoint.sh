#!/bin/bash

echo "Flush the manage.py command it any"

while ! python manage.py flush --no-input 2>&1; do
    echo "Flusing django manage command"
    sleep 3
done

echo "Migrate the Database at startup of project"

# Wait for few minute and run db make migration
while ! python manage.py makemigrations user 2>&1; do
    echo "Make Migration for specific app user"
    sleep 3
done

# Wait for few minute and run db migraiton
while ! python manage.py migrate user 2>&1; do
    echo "Migration is in progress for user"
    sleep 3
done

echo "Django docker is fully configured successfully."

exec "$@"