from app.core.config import config
from sqlmodel import create_engine, SQLModel, Session


class Database:
    def __init__(self, url: str):
        self.engine = create_engine(url)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session


db = Database(config.DATABASE_URL)
