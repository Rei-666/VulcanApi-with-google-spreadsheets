from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Homework import Homework
from Homework import base
from Exceptions import *
from VulcanApi import get_homework_list
from config import cfg
from google_spreadsheet import SheetClient
import datetime


if __name__ == "__main__":

    engine = create_engine(cfg['DATABASE'])

    Session = sessionmaker(bind=engine)
    session = Session()

    base.metadata.create_all(engine)

    sheet_client = SheetClient(cfg['GOOGLE_SHEET_CREDENTIALS_DIR'])

    newest_homework = session.query(Homework).order_by(Homework.date.desc()).first()

    newest_homework_date_minus_one_day = newest_homework.date - datetime.timedelta(days=1)

    homework_list = get_homework_list(date_from=newest_homework_date_minus_one_day)

    for homework in homework_list:
        is_homework_in_db = session.query(Homework).filter(Homework.id == homework.id).first()
        if not is_homework_in_db:
            try:
                homework.add_to_sheet(sheet_client.sheet)
            except NotEnoughSpace:
                print(f"Homework: {homework} wasn't added, because there weren't any empty cells.")
            else:
                session.add(homework)
    session.commit()
