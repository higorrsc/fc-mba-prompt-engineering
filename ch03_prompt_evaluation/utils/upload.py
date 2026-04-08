import argparse
from pathlib import Path

from dotenv import load_dotenv

from ch03_prompt_evaluation.shared.clients import get_langsmith_client
from ch03_prompt_evaluation.shared.datasets import upload_langsmith_dataset

load_dotenv()


def upload_dataset(dataset_dir: str, dataset_name: str) -> None:
    """Upload dataset to LangSmith with metadata support."""

    client = get_langsmith_client()

    dataset_file = Path(dataset_dir) / "dataset.jsonl"

    if not dataset_file.exists():
        print(f"Error: Dataset file not found at {dataset_file}")
        return

    count = upload_langsmith_dataset(
        dataset_file,
        dataset_name,
        f"Shared dataset for {dataset_name}",
        client,
    )

    print(f"Dataset '{dataset_name}' updated with {count} examples")


def main() -> None:
    """Add arguments to upload a dataset to LangSmith."""

    parser = argparse.ArgumentParser(description="Upload a dataset to LangSmith.")
    parser.add_argument(
        "--dataset-dir",
        type=str,
        required=True,
        help="The directory containing the dataset.jsonl file.",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        required=True,
        help="The name of the dataset to upload.",
    )
    args = parser.parse_args()

    upload_dataset(args.dataset_dir, args.dataset_name)


if __name__ == "__main__":
    main()
