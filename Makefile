# Run tests with verbose results
.PHONY: tests
tests:
	nosetests -v

# Run tests with coverage
.PHONY: coverage
coverage:
	nosetests --with-coverage --cover-erase --cover-package=dgsl_engine --cover-html
	
# Style
.PHONY: lint
lint:
	pylint dgsl_engine dgsl.py

# Style on tests
.PHONY: lint-tests
lint-tests:
	pylint tests

# Make all sphinx documentation
.PHONY: docs
docs:
	cd docs/code; \
	make html
