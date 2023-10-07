PYTHON = python3

# Makefile for running Python scripts

# Default target when user simply runs 'make'
default: help

# Define targets for running file1.py and file2.py
print_graphs_data:
	$(PYTHON) print_graphs_data.py

MM1:
	$(PYTHON) MM1.py

MM1K:
	$(PYTHON) MM1K.py

question1:
	$(PYTHON) question1.py

Stability_Check:
	$(PYTHON) Stability_Check.py

# Help target to display usage information
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  print_graphs_data   - Run print_graphs_data"
	@echo "  MM1  - Run MM1.py"
	@echo "  MM1K  - Run MM1K.py"
	@echo "  question1  - Run question1.py"
	@echo "  Stability_Check  - Run Stability_Check.py"
	@echo "  help    - Choose a target to run"

install:
	pip install -r requirements.txt
# Allow the user to specify a target as an argument to 'make'
.PHONY: install print_graphs_data MM1 MM1K question1 Stability_Check help
