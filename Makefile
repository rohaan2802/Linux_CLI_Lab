PYTHON ?= python3

.PHONY: doctor demo test showcase verify summary audit
doctor:
	$(PYTHON) -m cli_lab doctor

demo:
	$(PYTHON) -m cli_lab demo

test:
	$(PYTHON) -m unittest discover -s tests -v

showcase:
	$(PYTHON) tools/build_showcase.py

verify:
	$(PYTHON) tools/verify_showcase.py

summary:
	$(PYTHON) -m cli_lab summary

audit:
	$(PYTHON) -m cli_lab verify
