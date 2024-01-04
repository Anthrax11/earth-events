"""Pre-execution task definition"""
from src.config import read_config
from src.database.client import DBClient


def check_db_exists(task_instance=None):
    config = read_config()

    db_client = DBClient.from_config(config)

    signal = "true" if db_client.db_exists else "false"

    if task_instance:
        task_instance.xcom_push(key="db_exists", value=signal)
    else:
        print(signal)


def main():
    check_db_exists()


if __name__ == "__main__":
    main()