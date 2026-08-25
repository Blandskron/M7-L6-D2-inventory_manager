#!/bin/sh
set -eu

python manage.py migrate --noinput

# Crea el administrador una sola vez cuando no existe. Cambia las credenciales
# predeterminadas mediante un archivo .env antes de desplegar fuera del aula.
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); username = '$DJANGO_SUPERUSER_USERNAME'; email = '$DJANGO_SUPERUSER_EMAIL'; password = '$DJANGO_SUPERUSER_PASSWORD'; User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)"

exec "$@"
