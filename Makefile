# Run tests with verbose results
.PHONY: tests
tests:
	nosetests

# Run tests with coverage
.PHONY: coverage
coverage:
	nosetests --with-coverage --cover-erase --cover-package=dgsl_engine --cover-html
	
# Style
.PHONY: lint
lint:
	pylint dgsl_engine

# Style on tests
.PHONY: lint-tests
lint-tests:
	pylint tests

# Make all sphinx documentation
.PHONY: docs
docs:
	cd docs/code; \
	make clean; \
	make html

# Run all
.PHONY: all
all: coverage docs lint


# Add and fix docstrings
.PHONY: pyment
pyment:
	pyment -o google -w dgsl_engine
