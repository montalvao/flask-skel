clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	pip install -e .[dev] --upgrade --no-cache


install:
	pip install -e .['dev']


run:
	FLASK_DEBUG=true flask --app skel.app run


static-check:
	mypy \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--disallow-untyped-calls \
	--disallow-incomplete-defs \
	skel tests


test: static-check
	FLASK_DEBUG=false pytest --verbose tests
	isort --check .
	black --check .
	docstr-coverage --skip-file-doc --fail-under 80 skel


format-src:
	isort .
	black .


list:
	@grep '^[^\.#[:space:]].*:' Makefile

.PHONY: list
