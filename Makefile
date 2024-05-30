

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