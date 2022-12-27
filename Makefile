no: # Replace `Optional[T]` with `Union[T, None]`
	find regta_period -iname "*.py" | xargs python -m no_optional
	find tests -iname "*.py" | xargs python -m no_optional
isort: # Sort import statements
	isort .
lint: # Check code quality
	flake8 regta_period
	find . -iname "*.py" -not -path "./.venv/*" -not -path "./docs/*" | xargs pylint
test: # Run tests
	pytest --cov=regta_period tests/ -v
html_docs: # Build html docs
	cd docs/ && $(MAKE) clean && $(MAKE) html
