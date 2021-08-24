install:
	poetry install

requirements:
	poetry export -f requirements.txt --output requriments.txt

run:
	poetry run python manage.py runserver

lint:
	poetry run flake8 task_manager
