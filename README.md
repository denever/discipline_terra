    docker-compose up -d db

    DJANGO_SECRET_KEY=dev_secret_key DJANGO_POSTGRES_DBNAME=discipline DJANGO_POSTGRES_DBUSER=discipline DJANGO_POSTGRES_DBPASSWD=devpasswd DJANGO_POSTGRES_DBHOST=localhost poetry run python manage.py makemigrations
