# Set default goal
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run-app       - Run the recipe recommendation app"
	@echo "  update-data   - Run the make_dataframe script (specify NB_PAGES=xxx)"

.PHONY: run-app
run-app:
	python App/app.py

.PHONY: update-data
update-data:
	python App/make_dataframe.py NB_PAGES=$(NB_PAGES)