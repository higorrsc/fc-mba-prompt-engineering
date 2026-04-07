"""
Correctness evaluation: Comparing predictions against reference outputs.

Demonstrates labeled evaluators that use reference outputs for comparison.
"""

from pathlib import Path

from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator

from ch03_prompt_evaluation.shared.clients import get_openai_client
from ch03_prompt_evaluation.shared.evaluators import prepare_with_reference
from ch03_prompt_evaluation.shared.prompts import execute_text_prompt, load_yaml_prompt

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()
prompt = load_yaml_prompt("correctness_eval.yaml")


def run_correctness_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, oai_client, input_key="code")


# Labeled evaluators with reference outputs
evaluators = [
    LangChainStringEvaluator(
        "labeled_score_string",
        config={"criteria": "correctness", "normalize_by": 10},
        prepare_data=prepare_with_reference,  # type: ignore
    ),
    LangChainStringEvaluator(
        "labeled_score_string",
        config={"criteria": "relevance", "normalize_by": 10},
        prepare_data=prepare_with_reference,  # type: ignore
    ),  # type: ignore
]

# Run evaluation
results = evaluate(  # type: ignore
    run_correctness_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,  # type: ignore
    experiment_prefix="CorrectnessEval",
    max_concurrency=2,
)

print("=" * 80)
print(f"EXPERIMENT: {results.experiment_name}")
print("=" * 80)
