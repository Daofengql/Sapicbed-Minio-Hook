.PHONY: clean

help:
	@echo "  clean           remove unwanted stuff"
	@echo "  dev             make a development package"
	@echo "  publish-test    package and upload a release to test.pypi.org"
	@echo "  publish-release package and upload a release to pypi.org"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.DS_Store' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.coverage' -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info +

build:
	pip install -U setuptools twine wheel
	python setup.py sdist bdist_wheel

dev:
	pip install .
	$(MAKE) clean

publish-test:
	$(MAKE) build
	twine upload -r testpypi dist/*
	$(MAKE) clean

publish-release:
	$(MAKE) build
	twine upload dist/*
	$(MAKE) clean
