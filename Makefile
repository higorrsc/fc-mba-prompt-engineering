.PHONY: help install upload reset

.DEFAULT_GOAL := help

# Show this help message
help:
	@echo "Usage: make [target] [VARIABLES...]"
	@echo ""
	@echo "Targets:"
	@echo "  help       Show this help message"
	@echo "  install    Install project dependencies"
	@echo "  upload     Upload a dataset to LangSmith (requires DIR and NAME)"
	@echo "  reset      Delete a dataset from LangSmith (requires NAME)"
	@echo ""
	@echo "Examples:"
	@echo "  make upload DIR=ch03_prompt_evaluation/p01_basic NAME=evaluation_basic_dataset"
	@echo "  make reset NAME=evaluation_basic_dataset"

# Install project dependencies
install:
	uv sync

# Upload a dataset to LangSmith
# Example: make upload DIR=ch03_prompt_evaluation/p01_basic NAME=evaluation_basic_dataset
upload:
	@if [ -z "$(DIR)" ] || [ -z "$(NAME)" ]; then \
		echo "Error: DIR and NAME variables are required.\nUsage: make upload DIR=path/to/directory NAME=dataset_name"; \
		exit 1; \
	fi
	uv run -m ch03_prompt_evaluation.utils.upload --dataset-dir $(DIR) --dataset-name $(NAME)

# Delete a dataset from LangSmith
# Example: make reset NAME=evaluation_basic_dataset
reset:
	@if [ -z "$(NAME)" ]; then \
		echo "Error: NAME variable is required.\nUsage: make reset NAME=dataset_name"; \
		exit 1; \
	fi
	uv run -m ch03_prompt_evaluation.utils.reset --dataset-name $(NAME)
