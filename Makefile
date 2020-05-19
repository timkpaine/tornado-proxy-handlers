run:  ## Run the proxy server on 8080
	python3.7 -m tornado_proxy_handlers.server http://www.google.com

tests: ## Clean and Make unit tests
	python3.7 -m pytest -v tornado_proxy_handlers/tests --cov=tornado_proxy_handlers --junitxml=python_junit.xml --cov-report=xml --cov-branch

test: lint ## run the tests for travis CI
	@ python3.7 -m pytest -v tornado_proxy_handlers/tests --cov=tornado_proxy_handlers --junitxml=python_junit.xml --cov-report=xml --cov-branch

lint: ## run linter
	python3.7 -m flake8 tornado_proxy_handlers 

annotate: ## MyPy type annotation check
	mypy -s tornado_proxy_handlers

annotate_l: ## MyPy type annotation check - count only
	mypy -s tornado_proxy_handlers | wc -l 

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean
	rm -rf ./docs/*.*.rst  # generated

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

install:  ## install to site-packages
	python3.7 -m pip install -U .

dist:  ## dist to pypi
	rm -rf dist build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine check dist/* && twine upload dist/*

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean test tests help annotate annotate_l docs dist
