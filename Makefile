install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

req:
	poetry export -f requirements.txt --output requriments.txt

load-demo-data:
	poetry run python manage.py loaddata */fixtures/*.yaml

run:
	poetry run python manage.py runserver

lint:
	poetry run flake8

test:
	poetry run python manage.py test

coverage:
	poetry run coverage run --source='.' manage.py test

test-user:
	poetry run python manage.py test user

test-status:
	poetry run python manage.py test status

test-label:
	poetry run python manage.py test label

test-task:
	poetry run python manage.py test task

django-shell:
	poetry run python manage.py shell

start-locale:
	poetry run python manage.py makemessages -l ru

locale:
	poetry run python manage.py compilemessages

heroku-shell:
	heroku run bash
