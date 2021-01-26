from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///db.db', echo=True)

base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()


class Homework(base):
    __tablename__ = "Homeworks"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    subject = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"<Homework subject={self.subject}>"


base.metadata.create_all(engine)
today = datetime.datetime.now().date()

homework = Homework(date=today, subject="Niemiecki", description="Sprawdzian")

homeworks = session.query(Homework).filter(Homework.date==today).first()

if not homeworks:
    print("Pusto")
else:
    print(homeworks)