#-------------- Variables
PYTHON=$(shell which python3)
#--------------

all: dev-install 

clean:
	@rm -rf `find . -type d -name __pycache__ \
		-o -type f -name \*.bak \
		-o -type f -name \*.orig \
		-o -type f -name \*.pyc \
		-o -type f -name \*.pyd \
		-o -type f -name \*.pyo \
		-o -type f -name \*.rej \
		-o -type f -name \*.so`
	
	@rm -rf \
		*.core \
		*.egg-info \
		.coverage \
		.tox \
		pyftpd-tmp-\* \
		build/ \
		dist/ \
		docs/_build/ \
		.pytest_cache/ \
		tmp/

#-------------- Dev mode
dev:
	$(PYTHON) -m pip install -q --upgrade twine build

dev-install:
	$(PYTHON) -m pip install -e . --user

dev-uninstall:
	cd ..; $(PYTHON) -m pip uninstall -y -v mptcplib || true
	$(PYTHON) scripts/internal/purge_installation.py

dev-build:
	$(PYTHON) -m build

test:
	pip3 install -q pytest
	pytest ./mptcplib/test/ -v -s

test-coverage:
	pip3 install -q pytest-cov pytest-xdist
	pytest --cov=mptcplib ./mptcplib/test/ -v

#-------------- Distribution
pre-release: clean dev
	$(PYTHON) -m build
	$(PYTHON) -m twine check --strict dist/*
 
release: pre-release
	$(PYTHON) -m twine upload dist/*