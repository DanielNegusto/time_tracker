set shell := ["cmd.exe", "/c"]

up:
    pip install -r req.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py csu
    python manage.py runserver

lint:
    flake8 hours
    flake8 users
    black --check .