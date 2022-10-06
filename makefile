.PHONY: test

test:
	mypy --strict --implicit-reexport .
	lizard -w .
	python -m unittest
