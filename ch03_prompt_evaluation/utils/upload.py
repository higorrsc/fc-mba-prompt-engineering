from pathlib import Path

from dotenv import load_dotenv

from ch03_prompt_evaluation.shared.clients import get_langsmith_client
from ch03_prompt_evaluation.shared.datasets import upload_langsmith_dataset

load_dotenv()

SCRIPT_DIR = Path(__file__).parent
DATASET_FILE = SCRIPT_DIR / "dataset.jsonl"
DATASET_NAME = "evaluation_basic_dataset"


def upload_dataset() -> None:
    """Upload dataset to LangSmith with metadata support."""

    client = get_langsmith_client()

    count = upload_langsmith_dataset(
        DATASET_FILE,
        DATASET_NAME,
        "Shared dataset for basic evaluators",
        client,
    )

    print(f"Dataset '{DATASET_NAME}' updated with {count} examples")


def main() -> None:
    upload_dataset()


if __name__ == "__main__":
    main()
