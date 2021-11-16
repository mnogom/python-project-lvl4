install:
	poetry install ; \
	cp .env_example .env

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

check-migrations:
	poetry run python manage.py migrate --fake

req:
	poetry lock ; \
	poetry export -f requirements.txt --output requirements.txt

run:
	poetry run python manage.py runserver

lint:
	poetry run flake8

test:
	poetry run coverage run --source '.' manage.py test

coverage:
	poetry run coverage xml

django-shell:
	poetry run python manage.py shell

start-locale:
	poetry run python manage.py makemessages -l ru

locale:
	poetry run python manage.py compilemessages

heroku-shell:
	heroku run bash -a hidden-bayou-30395
