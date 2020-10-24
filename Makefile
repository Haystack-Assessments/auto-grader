# ---------------------------------------------------------
# Makefile for building and testing project
#
# Commands:
# help                        Print help documentation
# ---------------------------------------------------------


###
# Help Command
###


help:
	# Print help documentation
	@echo "Makefile Commands:"
	@echo "  help                        Print help documentation"
	@echo "  test                        Run Unit Tests"
	@echo "  black                       Run Black"
	@echo "  flake8                      Run Flake8"
	@echo "  mypy                        Run Mypi"
	@echo "  pycodestyle                 Run Pycodestyle"
	@echo "  pylint                      Run Pylint"
	@echo "  build                       Build Package"
	@echo "  clean                       Clean Package"

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
