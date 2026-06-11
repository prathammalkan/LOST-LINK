import os
import django
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lostlink.settings")
    django.setup()

    # If DATABASE_URL is not set, we default to SQLite
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL environment variable is not set. Skipping migrations and superuser setup.")
        return

    print("DATABASE_URL found. Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("Migrations completed successfully.")
    except Exception as e:
        print(f"Error running migrations: {e}")
        return

    # Create superuser if not exists
    from django.contrib.auth.models import User
    try:
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin@123')
            print("Superuser created successfully.")
        else:
            print("Superuser 'admin' already exists. Updating password to admin@123...")
            u = User.objects.get(username='admin')
            u.set_password('admin@123')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            print("Superuser password updated.")
    except Exception as e:
        print(f"Error creating/updating superuser: {e}")

if __name__ == "__main__":
    main()
