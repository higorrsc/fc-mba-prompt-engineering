import argparse

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()


def reset_dataset(dataset_name: str) -> None:
    """Delete dataset if it exists."""

    client = Client()

    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        client.delete_dataset(dataset_id=dataset.id)
        print(f"Dataset deleted: {dataset_name}")
    except Exception:
        print(f"Dataset not found or already deleted: {dataset_name}")


def main() -> None:
    """Add arguments to reset a LangSmith dataset."""

    parser = argparse.ArgumentParser(description="Reset a LangSmith dataset.")
    parser.add_argument(
        "--dataset-name",
        type=str,
        required=True,
        help="The name of the dataset to reset.",
    )
    args = parser.parse_args()

    reset_dataset(args.dataset_name)


if __name__ == "__main__":
    main()

#
