import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lostlink.settings")
django.setup()

# Run migrations at startup
db_url = os.environ.get("DATABASE_URL")
if db_url:
    print("Running database migrations on startup...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("Migrations completed successfully.")
        
        # Ensure superuser exists
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin@123')
            print("Superuser created.")
        else:
            print("Updating superuser password...")
            u = User.objects.get(username='admin')
            u.set_password('admin@123')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            print("Superuser password updated.")
    except Exception as e:
        print(f"Startup database configuration error: {e}")

application = get_wsgi_application()
app = application
