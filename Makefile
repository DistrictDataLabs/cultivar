# Shell to use with Make
SHELL := /bin/sh

# Set important Paths
PROJECT := trinket
LOCALPATH := $(CURDIR)/
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

# Production Settings
SETTINGS := production
DJANGO_SETTINGS_MODULE = $(PROJECT).settings.$(SETTINGS)
DJANGO_POSTFIX := --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)

# Development Settings
LOCAL_SETTINGS := development
DJANGO_LOCAL_SETTINGS_MODULE = $(PROJECT).settings.$(LOCAL_SETTINGS)
DJANGO_LOCAL_POSTFIX := --settings=$(DJANGO_LOCAL_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)

# Testing Settings
TEST_SETTINGS := testing
DJANGO_TEST_SETTINGS_MODULE = $(PROJECT).settings.$(TEST_SETTINGS)
DJANGO_TEST_POSTFIX := --settings=$(DJANGO_TEST_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)

# Apps to test
APPS := trinket

# Export targets not associated with files
.PHONY: test showenv coverage bootstrap pip virtualenv clean virtual_env_set

# Show Virtual Environment
showenv:
	@echo 'Environment:'
	@echo '------------------------'
	@$(PYTHON_BIN)/python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'PROJECT:' $(PROJECT)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_LOCAL_SETTINGS_MODULE:' $(DJANGO_LOCAL_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)
	@echo 'VIRTUAL_ENV:' $(VIRTUAL_ENV)

# Show help for Django
djangohelp:
	$(LOCALPATH)/manage.py help $(DJANGO_LOCAL_POSTFIX)

# Run the development server
runserver:
	$(LOCALPATH)/manage.py runserver $(DJANGO_LOCAL_POSTFIX)

# Clean build files
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT)/*.egg-info

# Targets for Django testing
test:
	$(PYTHON_BIN)/coverage run --source=$(CURDIR) $(CURDIR)/manage.py test $(CURDIR) $(DJANGO_POSTFIX)
	- $(PYTHON_BIN)/coverage report --omit="venv/*"
