from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

DATASET_NAME = "evaluation_basic_dataset"


def reset_dataset() -> None:
    """Delete dataset if it exists."""

    client = Client()

    try:
        dataset = client.read_dataset(dataset_name=DATASET_NAME)
        client.delete_dataset(dataset_id=dataset.id)
        print(f"Dataset deleted: {DATASET_NAME}")
    except Exception:
        print(f"Dataset not found or already deleted: {DATASET_NAME}")


def main() -> None:
    reset_dataset()


if __name__ == "__main__":
    main()

#
