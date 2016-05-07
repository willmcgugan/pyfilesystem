PYTHON=python
TSCRIPT=fs/tests/runner.py

all: test

clean:
	rm -f `find . -type f -name \*.py[co]`
	rm -f `find . -type f -name \*.so`
	rm -f `find . -type f -name \*.~`
	rm -f `find . -type f -name \*.orig`
	rm -f `find . -type f -name \*.bak`
	rm -f `find . -type f -name \*.rej`
	rm -rf `find . -type d -name __pycache__`
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

install:
	$(PYTHON) setup.py build
	$(PYTHON) setup.py develop

test: install
	$(PYTHON) $(TSCRIPT)
