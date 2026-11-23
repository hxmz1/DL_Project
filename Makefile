PYTHON ?= .\.venv\Scripts\python.exe

.PHONY: install test pipeline docs

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests --ignore LOG015,TRY004

pipeline:
	$(PYTHON) -m src.pipeline.run_pipeline

quick-pipeline:
	$(PYTHON) -m src.pipeline.run_pipeline --quick
