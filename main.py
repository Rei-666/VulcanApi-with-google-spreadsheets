from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Homework import Homework
from Homework import base
from main import get_homework_list
from main import CRED_DIR
from google_spreadsheet import SheetClient


if __name__ == "__main__":

    engine = create_engine('sqlite:///db.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    base.metadata.create_all(engine)

    sheet_client = SheetClient(CRED_DIR)

    homework_list = get_homework_list()

    for homework in homework_list:
        is_homework_in_db = session.query(Homework).filter(Homework.id == homework.id).first()
        if not is_homework_in_db:
            homework.add_to_sheet(sheet_client.sheet)
            session.add(homework)
    session.commit()
