from src.database.models import Base
from src.database.client import DBClient
from src.config import read_config


def init_db():
    config = read_config()

    db_client = DBClient.from_config(config)

    db_client.create_database()

    Base.metadata.create_all(db_client.engine)

def main():
    init_db()

if __name__ == "__main__":
    main()