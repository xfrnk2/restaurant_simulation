VERSION = $(shell gobump show -r)
CURRENT_REVISION = $(shell git rev-parse --short HEAD) 
BUILD_LDFLAGS = "-X github.com/xfrnk2/restaurant_simulation.revision=$(CURRENT_REVISION)"
ifdef update
  u=-u
endif
OsConf= ./LinuxWindowsScript.sh
VENV=${test_path}

.PHONY: help bootstrap clean lint test coverage install


help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "install - install the package to the active Python's site-packages"

bootstrap:
	python -m venv env
	pip install --upgrade setuptools ;\
	pip install --upgrade "pip>=19" ;\
	pip install -r requirements.txt ;\
	

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .coverage
	rm -fr htmlcov/

lint:
	$(OsConf)
	$(VENV)
	flake8 src tests

test:	
	$(OsConf)
	$(VENV)
	python setup.py test $(TEST_ARGS)

coverage: test
	$(OsConf)
	$(VENV)
	coverage run --source src setup.py test ;\
	coverage report -m ;\
	coverage html ;\
	open htmlcov/index.html ;\


install: clean
	$(OsConf)
	$(VENV)
	python setup.py install

cover:
	$(OsConf)
	$(VENV)
	coverage run --source=src setup.py test ;\
	coverage xml -i ;\
	coveralls_token=${coveralls_token} coveralls --service=travis-ci ;\
	#coveralls_token=${coveralls_token} coveralls --service=travis-ci ;\
	
	