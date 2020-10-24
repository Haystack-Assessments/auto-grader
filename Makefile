# ---------------------------------------------------------
# Makefile for building and testing project
#
# Commands:
# help                        Print help documentation
# black                       Run Black
# build                       Build Package
# clean                       Clean Package
# flake8                      Run Flake8
# help                        Print help documentation
# install                     Install Package
# mypy                        Run Mypi
# profile                     Running Assessment with Profile Enabled
# pycodestyle                 Run Pycodestyle
# pylint                      Run Pylint
# run                         Running Assessment
# test                        Run Unit Tests
# venv                        Create Virtual Environment
# ---------------------------------------------------------


###
# Help Command
###


help:
	# Print help documentation
	@echo "Makefile Commands:"
	@echo "  black                       Run Black"
	@echo "  build                       Build Package"
	@echo "  clean                       Clean Package"
	@echo "  flake8                      Run Flake8"
	@echo "  help                        Print help documentation"
	@echo "  install                     Install Package"
	@echo "  mypy                        Run Mypi"
	@echo "  pycodestyle                 Run Pycodestyle"
	@echo "  pylint                      Run Pylint"
	@echo "  run                         Running Assessment"
	@echo "  test                        Run Unit Tests and Code Coverage"
	@echo "  venv                        Create Virtual Environment"


###
# Env Commands
###


venv:
	# Create Venv
	python3 -m virtualenv venv


###
# Test Commands
###


test:
	# Run Unit Tests
	python3 setup.py -q test --addopts="-c .pytest.ini"


###
# Style/Typing Commands
###


black:
	# Run Black
	black --config=.blackrc .

flake8:
	# Run Flake8
	flake8 --config=.flake8

mypy:
	# Run Mypi
	mypy --config-file=.mypy.ini grader

pycodestyle:
	# Run Pycodestyle
	pycodestyle --config=.pycodestyle grader

pylint:
	# Run Pylint
	pylint --rcfile=.pylintrc grader


###
# Buid Commands
###


build:
	# Build Package
	python3 setup.py build


###
# Install Commands
###


install:
	# Install Package
	pip3 install --editable .



###
# Clean Commands
###


clean:
	# Clean Package
	rm -rf \
	    *.egg-info\
		.egg\
		.eggs \
		.pytest_cache/ \
		.mypy_cache/ \
		reports/ \
		.coverage \
		build/
	find . -name '__pycache__' -type d | xargs rm -fr
	find . -name '.DS_Store' -type d | xargs rm -fr
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
