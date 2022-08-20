lint:
	flake8 regta_period
	find . -iname "*.py" -not -path "./.venv/*" -not -path "./docs/*" | xargs pylint
test:
	pytest --cov=regta_period tests/ -v
html_docs:
	cd docs/ && $(MAKE) clean && $(MAKE) html
