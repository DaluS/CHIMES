lint:
	flake8 ./chimes/plots --show-source --statistics
	flake8 ./tests/unit --ignore=E501 --show-source --statistics
	flake8 . --count --select=E9,F63,F7 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


test:
	pytest --mocha tests/unit/ -v --cov=chimes

integration:
	pytest --mocha tests/integration/ -v --cov=chimes


docs:
	sphinx-apidoc -o docs ./chimes
	cd docs; \
	make -f ./Makefile html; \
	cd ..
	make opendocs

opendocs:
	firefox docs/_build/html/index.html


coverage:
	pytest --mocha tests/unit/ -v --cov=chimes --cov-report html
	pytest --mocha tests/integration -v --cov=chimes --cov-report html --cov-append
	make opencov

opencov:
	firefox htmlcov/index.html


.PHONY: docs opendocs