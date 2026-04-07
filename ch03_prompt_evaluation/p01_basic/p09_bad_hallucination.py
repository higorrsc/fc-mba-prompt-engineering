"""
Bad prompt test: Hallucinated issues.

Tests a prompt that invents issues not present in the code.
Expected: LOW scores in faithfulness.
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


def run_bad_hallucination(inputs: dict) -> dict:
    """Runs the bad_hallucination prompt"""

    prompt = load_yaml_prompt("bad_hallucination.yaml")
    # Note: Using higher temperature for this bad example
    return execute_text_prompt(
        prompt,
        inputs,
        oai_client,
        input_key="code",
        temperature=1.2,
    )


# Evaluators focused on detecting hallucination
evaluators = [
    # Detects hallucination (bad_hallucination should have low score)
    LangChainStringEvaluator(
        "score_string",
        config={
            "criteria": {
                "faithfulness": "Is the response grounded ONLY in the provided code? "
                "Doesn't invent problems or context that doesn't exist in the code?"
            },
            "normalize_by": 10,
        },
        prepare_data=prepare_with_input,  # type: ignore
    ),
    # Additional metrics for context
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "helpfulness", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "coherence", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
    LangChainStringEvaluator(
        "score_string",
        config={"criteria": "detail", "normalize_by": 10},
        prepare_data=prepare_with_input,  # type: ignore
    ),
]

print("=" * 80)
print("TEST: BAD_HALLUCINATION")
print("=" * 80)
print("\nExpected: LOW score in faithfulness (< 0.4)")
print("Prompt: Expert who invents fictional problems")
print("=" * 80)
print()

# Run evaluation
results = evaluate(
    run_bad_hallucination,
    data=DATASET_NAME,
    evaluators=evaluators,  # type: ignore
    experiment_prefix="BadHallucination_Test",
    max_concurrency=2,
)

print("=" * 80)
print(f"EXPERIMENT: {results.experiment_name}")
print("=" * 80)
