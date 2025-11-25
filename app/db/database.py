from app.core.config import get_settings
from sqlmodel import create_engine, SQLModel, Session

config = get_settings()


class Database:
    def __init__(self, url: str):
        self.engine = create_engine(url)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session


db = Database(config.database_url)
