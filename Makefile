lint:
	flake8
	find . -iname "*.py" -not -path "./.venv/*" -not -path "./docs/*" | xargs pylint
test:
	pytest --cov=regta_period tests/ -v
