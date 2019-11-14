.PHONY: check test

check:
	python -m doctest -f *.py

test:
	python -m doctest -v *.py
