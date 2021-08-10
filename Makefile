install:
	poetry install

requirements:
	poetry export -f requirements.txt --output requriments.txt

run:
	poetry run python manage.py runserver
