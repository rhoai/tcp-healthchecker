PYPI_SERVER ?= gemfury

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build-upload:
	python setup.py register -r ${PYPI_SERVER} sdist upload -r ${PYPI_SERVER}

build:
	python setup.py sdist