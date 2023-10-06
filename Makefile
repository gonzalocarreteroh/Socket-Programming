# Makefile for running Python scripts

# Default target when user simply runs 'make'
default: help

# Define targets for running file1.py and file2.py
graph1:
	python graph1.py

graph2:
	python graph2.py

graph3:
	python graph3.py

graph4:
	python graph4.py

MM1:
	python MM1.py

MM1K:
	python MM1K.py

question1:
	python question1.py

Stability_Check:
	python Stability_Check.py


# Help target to display usage information
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  graph1   - Run graph1.py"
	@echo "  graph2   - Run graph2.py"
	@echo "  graph3  - Run graph3.py"
	@echo "  graph4  - Run graph4.py"
	@echo "  MM1  - Run MM1.py"
	@echo "  MM1K  - Run MM1K.py"
	@echo "  question1  - Run question1.py"
	@echo "  Stability_Check  - Run Stability_Check.py"
	@echo "  help    - Choose a target to run"

# Allow the user to specify a target as an argument to 'make'
.PHONY: graph1 graph2 graph3 graph4 MM1 MM1K question1 Stability_Check help
