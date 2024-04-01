ci-mypy:
	mypy manage.py server $(find tests -name '*.py')

flake8:
	flake8 .
celery:
	celery -A server worker -l info --concurrency=4
