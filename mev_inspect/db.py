from dotenv import load_dotenv
import os
from typing import Any, Iterable, List, Optional
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.arbitrages import ArbitrageModel
from contextlib import contextmanager

load_dotenv()

def get_database_uri() -> Optional[str]:
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db_name = "blocks"

    if all(field is not None for field in [username, password, host]):
        # "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
        return f"postgresql+psycopg2://{username}:{password}@{host}/{db_name}"

    return None

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


database_uri = get_database_uri()
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    recreate_database()
    # add_data()

    arb = ArbitrageModel(
        id='1',
        block_number=12345,
        transaction_hash='0x2734762',
        account_address='0x123456789',
        profit_token_address='0x5678910',
        start_amount=10,
        end_amount=20,
        profit_amount=10,
        protocols=['uniswap', 'curve']
    )

    with session_scope() as s:
        s.add(arb)