"""
Binary criteria evaluation: Pass/Fail evaluation using LLM judges.

Demonstrates binary evaluators (0 or 1) for quick yes/no validation.
"""

from pathlib import Path

from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator

from ch03_prompt_evaluation.shared.clients import get_openai_client
from ch03_prompt_evaluation.shared.evaluators import (
    prepare_with_input,
    prepare_with_reference,
)
from ch03_prompt_evaluation.shared.prompts import execute_text_prompt, load_yaml_prompt

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()
prompt = load_yaml_prompt("criteria_eval.yaml")


def run_criteria_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""

    return execute_text_prompt(
        prompt,
        inputs,
        oai_client,
        input_key="code",
    )


# BINARY EVALUATORS: criteria (0 or 1)
#
# criteria: Returns 0 (fail) or 1 (pass)
# - Faster and more direct
# - Ideal for pass/fail yes/no validations
# - Examples: "Is JSON valid?", "Is response concise?", "Is it harmful?"
#
# Use criteria when:
# - You need simple pass/fail validation
# - Question is yes/no type
# - You want fast binary decisions
#
# NOTE: Next example (3-criteria-score-eval.py) shows score_string,
# which returns continuous values (0.0-1.0) for nuanced evaluations.

evaluators = [
    # Binary: Is concise? (0=no, 1=yes)
    LangChainStringEvaluator(
        "criteria",
        config={"criteria": "conciseness"},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Binary: Is helpful? (0=no, 1=yes)
    LangChainStringEvaluator(
        "criteria",
        config={"criteria": "helpfulness"},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Binary with reference: Is correct compared to expected? (0=no, 1=yes)
    LangChainStringEvaluator(
        "labeled_criteria",
        config={"criteria": "correctness"},
        prepare_data=prepare_with_reference,  # type: ignore
    ),
]

# Run evaluation
results = evaluate(  # type: ignore
    run_criteria_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,  # type: ignore
    experiment_prefix="CriteriaBinary",
    max_concurrency=2,
)

print("=" * 80)
print(f"EXPERIMENT: {results.experiment_name}")
print("=" * 80)
