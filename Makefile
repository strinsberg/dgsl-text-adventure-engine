# Style
lint:
	pylint dgsl_engine dgsl.py

# Style on tests
lint-tests:
	pylint tests

# Run tests with verbose results
test:
	nosetests -v

# Run tests with coverage
coverage:
	nosetests --with-coverage --cover-erase --cover-package=dgsl_engine --cover-html
