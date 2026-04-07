"""
Bad prompt test: Unhelpful responses.

Tests a prompt that provides generic, unhelpful feedback.
Expected: LOW scores in helpfulness, detail, and depth.
"""

from pathlib import Path

from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator

from ch03_prompt_evaluation.shared.clients import get_openai_client
from ch03_prompt_evaluation.shared.evaluators import prepare_with_input
from ch03_prompt_evaluation.shared.prompts import execute_text_prompt, load_yaml_prompt

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()


def run_bad_not_helpful(inputs: dict) -> dict:
    """Runs the bad_not_helpful prompt"""
    prompt = load_yaml_prompt("bad_not_helpful.yaml")
    # Note: Using lower temperature for this bad example
    return execute_text_prompt(
        prompt,
        inputs,
        oai_client,
        input_key="code",
        temperature=0.3,
    )


# Evaluators focused on detecting lack of usefulness
evaluators = [
    # Detects not_helpful (bad_not_helpful should have low score)
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "helpfulness", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Detects lack of details (bad_not_helpful should have low score)
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "detail", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Detects superficial analysis (bad_not_helpful should have low score)
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "depth", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Additional metrics for context
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "coherence", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "conciseness", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
]

print("=" * 80)
print("TEST: BAD_NOT_HELPFUL")
print("=" * 80)
print("\nExpected: LOW scores in helpfulness, detail and depth (< 0.4)")
print("Prompt: Lazy reviewer with generic responses")
print("=" * 80)
print()

# Run evaluation
results = evaluate(
    run_bad_not_helpful,
    data=DATASET_NAME,
    evaluators=evaluators,  # type: ignore
    experiment_prefix="BadNotHelpful_Test",
    max_concurrency=2,
)

print("=" * 80)
print(f"EXPERIMENT: {results.experiment_name}")
print("=" * 80)
