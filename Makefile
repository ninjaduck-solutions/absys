BUILDDIR ?= _build
ENV ?= dev
PORT ?= 8000
SPHINXOPTS =

.PHONY: help clean clean-build clean-docs clean-pyc clean-test coverage coverage-html \
    create-db develop docs isort migrate serve-docs runserver shell startapp test \
    test-all glances fixtures reset-db test-fixtures modelgraph test-fresh wheelhouse

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean                    to remove all build, test, coverage and Python artifacts (does not remove backups)"
	@echo "  clean-backups            to remove backup files created by editors and Git"
	@echo "  clean-build              to remove build artifacts"
	@echo "  clean-docs               to remove documentation artifacts"
	@echo "  clean-pyc                to remove Python file artifacts"
	@echo "  clean-test               to remove test and coverage artifacts"
	@echo "  coverage                 to generate a coverage report with the default Python"
	@echo "  coverage-html            to generate and open a HTML coverage report with the default Python"
	@echo "  create-db                to create a new PostgreSQL database"
	@echo "  create-db-user           to create a new PostgreSQL user"
	@echo "  createsuperuser          to create a superuser for the current project"
	@echo "  drop-db                  to drop the PostgreSQL database"
	@echo "  drop-db-user             to drop the PostgreSQL user"
	@echo "  develop                  to install (or update) all packages required for development"
	@echo "  dist                     to package a release"
	@echo "  docs                     to build the project documentation as HTML"
	@echo "  fixtures                 to load fixtures for development"
	@echo "  isort                    to run isort on the whole project"
	@echo "  makemigrations           to build migrations after altering the models"
	@echo "  migrate                  to synchronize Django's database state with the current set of models and migrations"
	@echo "  modelgraph               to generate a visualisation of your models and their relations"
	@echo "  reset-db                 to reset the PostgreSQL database"
	@echo "  runserver                to start Django's development Web server"
	@echo "  serve-docs               to serve the project documentation in the default browser"
	@echo "  wheelhouse               to populate the wheelhouse with all production wheels"
	@echo "  shell                    to start a Python interactive interpreter"
	@echo "  startapp                 to create a new Django app"
	@echo "  glances                  to start the Glances monitoring tool in web server mode"
	@echo "  test                     to run unit tests quickly with the default Python"
	@echo "  test-fresh               to run unit tests with a fresh database and the default Python"
	@echo "  test-fixtures            to show all pytest fixtures"
	@echo "  test-all                 to run unit tests on every Python version with tox"


clean: clean-build clean-docs clean-test clean-pyc

clean-backups:
	find . -name '*~' -delete
	find . -name '*.orig' -delete
	find . -name '*.swp' -delete

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-docs:
	$(MAKE) -C docs clean BUILDDIR=$(BUILDDIR)

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -delete

clean-test:
	rm -fr .cache/
	rm -fr .tox/
	coverage erase
	rm -fr htmlcov/

coverage:
	envdir envs/$(ENV) coverage run -m pytest tests/
	coverage report

coverage-html: coverage
	coverage html
	python -c "import os, webbrowser; webbrowser.open('file://{}/htmlcov/index.html'.format(os.getcwd()))"

create-db:
	sudo -u postgres createdb -l en_US.UTF-8 -E UTF8 -O absys -T template0 -e absys

create-db-user:
	sudo -u postgres psql -d postgres -c "CREATE USER \"absys\" WITH PASSWORD 'absys' CREATEDB;"

createsuperuser:
	envdir envs/$(ENV) python3 manage.py createsuperuser --email ada@example.com

drop-db:
	sudo -u postgres dropdb -i -e absys

drop-db-user:
	sudo -u postgres dropuser -i -e absys

develop:
	pip install -U pip setuptools wheel
	pip install -U -c requirements/constraints.pip -r requirements/dev.pip
	pip install -U -c requirements/constraints.pip -e .

dist: clean
	python3 setup.py bdist_wheel
	@echo
	ls -1 dist/

make wheelhouse:
	rm -fr wheelhouse/
	mkdir wheelhouse/
	pip wheel --constraint requirements/constraints.pip --wheel-dir wheelhouse/ dist/absys-*.whl
	@echo
	ls -1 wheelhouse/

docs:
	$(MAKE) -C docs html BUILDDIR=$(BUILDDIR) SPHINXOPTS='$(SPHINXOPTS)'

isort:
	isort --recursive setup.py absys/ tests/

makemigrations:
	envdir envs/$(ENV) python3 manage.py makemigrations

migrate:
	envdir envs/$(ENV) python3 manage.py migrate

modelgraph:
	git diff --quiet docs
	git diff --cached --quiet
	envdir envs/$(ENV) python3  manage.py graph_models -a -E -o docs/_static/modelgraph_easy.png
	envdir envs/$(ENV) python33  manage.py graph_models -a -g -o docs/_static/modelgraph_complete.png
	git add docs
	git commit -m "docs: Modelgraphen aktualisiert"

runserver:
	envdir envs/$(ENV) python3 manage.py runserver 0.0.0.0:$(PORT)

serve-docs:
	cd docs/$(BUILDDIR)/html; python3 -m http.server $(PORT)

shell:
	envdir envs/$(ENV) python3 manage.py shell

startapp:
	@read -p "Enter the name of the new Django app: " app_name; \
	app_name_title=`python3 -c "import sys; sys.stdout.write(sys.argv[1].title())" $$app_name`; \
	mkdir -p absys/apps/$$app_name; \
	envdir envs/$(ENV) python3 manage.py startapp $$app_name absys/apps/$$app_name --template absys/config/app_template; \
	echo "Don't forget to add 'absys.apps."$$app_name".apps."$$app_name_title"Config' to INSTALLED_APPS in 'absys/config/settings/common.py'!"

glances:
	glances -w

test:
	@echo "Use the PYTEST_ADDOPTS environment variable to add extra command line options"
	@echo "Use \"PYTEST_ADDOPTS='--cache-clear'\" to clean up the test cache"
	@echo "Use \"PYTEST_ADDOPTS='--create-db'\" to force recreation of the test database"
	@echo
	envdir envs/$(ENV) python3 -m pytest -m "not slowtest" --reuse-db --last-failed tests/

test-fresh:
	envdir envs/$(ENV) python3 -m pytest -m "not slowtest" --create-db --cache-clear tests/

test-fixtures:
	envdir envs/$(ENV) python3 -m pytest --fixtures tests/

test-all:
	tox

fixtures:
	envdir envs/$(ENV) python3 manage.py loaddata sites.json
	envdir envs/$(ENV) python3 manage.py loadtestdata schueler.Gruppe:2
	envdir envs/$(ENV) python3 manage.py loadtestdata schueler.Sozialamt:2
	envdir envs/$(ENV) python3 manage.py loadtestdata schueler.Schueler:10
	envdir envs/$(ENV) python3 manage.py loadtestdata einrichtungen.Einrichtung:4
	envdir envs/$(ENV) python3 manage.py loadtestdata einrichtungen.SchuelerInEinrichtung:80
	envdir envs/$(ENV) python3 manage.py loadtestdata einrichtungen.EinrichtungHatPflegesatz:8
	envdir envs/$(ENV) python3 manage.py loadtestdata einrichtungen.Ferien:4
	envdir envs/$(ENV) python3 manage.py loadtestdata einrichtungen.Schliesstag:10
	envdir envs/$(ENV) python3 manage.py createsuperuser --email ada@example.com

reset-db: drop-db create-db migrate
