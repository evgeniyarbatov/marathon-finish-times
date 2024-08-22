CONFIG_FILE = config.json
OUTPUT_DIR = data

VENV_PATH = ~/.venv/marathon-finish-times

all: scrape

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

scrape: install
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/scrape.py "$(CONFIG_FILE)" $(OUTPUT_DIR)

merge:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/merge.py $(OUTPUT_DIR)

clean:
	@source $(VENV_PATH)/bin/activate && \
	python3 scripts/clean.py $(OUTPUT_DIR)

upload:
	@source $(VENV_PATH)/bin/activate && \
	export KAGGLE_KEY=f254df82ac823f1663bf3a7d9049ddb1 KAGGLE_USERNAME=evgenyarbatov; \
	python3 scripts/upload.py $(OUTPUT_DIR)

.PHONY: venv install scrape merge clean upload