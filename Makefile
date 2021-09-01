install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

requirements:
	poetry export -f requirements.txt --output requriments.txt

run:
	poetry run python manage.py runserver

lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test


test-user:
	poetry run python manage.py test user


test-status:
	poetry run python manage.py test status


django-shell:
	poetry run python manage.py shell

start-locale:
	poetry run python manage.py makemessages -l ru ; \
	subl */locale/ru/LC_messages/django.po

locale:
	poetry run python manage.py compilemessages

heroku-shell:
	heroku run bash
