URL = https://worldathletics.org/records/all-time-toplists/road-running/marathon/all/women/senior?regionType=world&page=1&bestResultsOnly=true&firstDay=1900-01-01&lastDay=2024-08-12&maxResultsByCountry=all&eventId=10229534&ageCategory=senior

VENV_PATH = ~/.venv/marathon-finish-times
OUTPUT_DIR = data

all: scrape

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

scrape: install
	source $(VENV_PATH)/bin/activate && \
	python3 scripts/scrape.py "$(URL)" $(OUTPUT_DIR)

.PHONY: venv install scrape