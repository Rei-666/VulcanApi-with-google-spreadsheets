from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


class DatabaseConnectionCreator:
    def __new__(cls, database_directory):
        engine = create_engine(database_directory)
        Session = sessionmaker(bind=engine)
        base.metadata.create_all(engine)
        return Session()

