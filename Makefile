define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
# TOTAL=5

help: ## all available targets
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

migrations: ## make migrations
	python manage.py makemigrations
	python manage.py migrate

test: ## run unit tests tp check code funcionality
	tox
	
test-quality: ## run test quality checks
	isort -rc . --diff
	pycodestyle --show-source .
	pydocstyle .

requirements: ## installs all dependencies
	pip install -r requirements.txt

run: ## run server
	python manage.py runserver

create-dummy-data: ## create dummy entries in models.
ifdef $(TOTAL)
	python manage.py create_dummy_clients --total $(TOTAL)
	python manage.py create_dummy_employees --total $(TOTAL)
	python manage.py create_dummy_orders --total $(TOTAL)
	python manage.py create_dummy_tasks --total $(TOTAL)
else
	python manage.py create_dummy_clients
	python manage.py create_dummy_employees
	python manage.py create_dummy_orders
	python manage.py create_dummy_tasks
endif

delete-dummy-data: ## deletes dummy data
	python manage.py delete_dummy_tasks
	python manage.py delete_dummy_orders
	python manage.py delete_dummy_clients
	python manage.py delete_dummy_employees