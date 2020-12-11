import os.path
import sys

CURRENT_DIR = os.getcwd()

# Local settings
# Set engine to django.db.backends. 'postgresql_psycopg2', 'mysql', 'sqlite3'
# Or path to database file if using sqlite3.
# Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.

LOCALE_PATHS = ("/home/denever/work/discipline_terra/conf/locale",)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(CURRENT_DIR, "discipline.db"),
        # The following settings are not used with sqlite3:
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",  # Set to empty string for default.
    }
}
DEBUG = False if "test" in sys.argv else True
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CURRENT_DIR, "discipline_terra/static"),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CURRENT_DIR, "discipline_terra")
)
