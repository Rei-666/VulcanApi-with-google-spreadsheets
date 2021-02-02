from write_as_api import create_post
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
import re

base = declarative_base()

class Homework(base):
    SPECIAL_CASES = ['Fizyka']

    __tablename__ = "Homeworks"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    subject = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"<Homework subject={self.subject}>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.subject in self.SPECIAL_CASES:
            self.format_description()

    def add_to_sheet(self, sheet):
        formatted_date = self.date.strftime("%d.%m")
        cell = sheet.find(formatted_date)
        row = sheet.row_values(cell.row)
        text = f"{self.subject}\n{self.description}"
        sheet.update_cell(cell.row, row.index('') + 1, text)

    def format_description(self):
        if self.subject == "Fizyka":
            regex = r'Praca domowa(:|;)(.*?)(?:(?:\r*\n){2}|$)'
            post = create_post(self.description, self.subject)
            occurences = re.findall(regex, self.description, flags=re.DOTALL | re.IGNORECASE)
            if occurences:
                self.description = '\n'.join([x[1:] for x in occurences[0][1:]])
            else:
                self.description = ""
            self.description =+ f'\n{post}'