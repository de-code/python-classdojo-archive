VENV = venv

ifeq ($(OS),Windows_NT)
	VENV_BIN = $(VENV)/Scripts
else
	VENV_BIN = $(VENV)/bin
endif

PIP = $(VENV_BIN)/pip
PYTHON = $(VENV_BIN)/python

SYSTEM_PYTHON = python3


ARGS =
PYTEST_WATCH_MODULES =


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi


venv-create:
	$(SYSTEM_PYTHON) -m venv $(VENV)


venv-activate:
	chmod +x venv/bin/activate
	bash -c "venv/bin/activate"


dev-install:
	$(PIP) install --disable-pip-version-check \
		-r requirements.build.txt \
		-r requirements.dev.txt \
		-r requirements.txt


dev-venv: venv-create dev-install


dev-flake8:
	$(PYTHON) -m flake8 dojo_archive tests

dev-pylint:
	$(PYTHON) -m pylint dojo_archive tests

dev-mypy:
	$(PYTHON) -m mypy dojo_archive tests


dev-lint: dev-flake8 dev-pylint dev-mypy

dev-unittest:
	$(PYTHON) -m pytest -p no:cacheprovider $(ARGS) tests

dev-watch:
	$(PYTHON) -m pytest_watcher --now . $(ARGS) $(PYTEST_WATCH_MODULES)

dev-test: dev-lint dev-unittest


run:
	$(PYTHON) -m dojo_archive.cli
