# Makefile for Django App

# Variables
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

# Create a new virtual environment
create_venv:
	python3.10 -m venv $(VENV_NAME)

# Activate the virtual environment
# Note: 'source' command does not work in Makefile, you have to run it manually
activate_venv:
	@echo "To activate the virtual environment, run 'source $(VENV_NAME)/bin/activate'"

# Install dependencies
install_requirements:
	$(PYTHON) -m pip install -r requirements.txt

# Run the Django development server
run:
	$(PYTHON) manage.py runserver

# Full setup: create venv, install requirements, and run server
setup: create_venv activate_venv install_requirements

.PHONY: create_venv activate_venv install_requirements run_server setup
