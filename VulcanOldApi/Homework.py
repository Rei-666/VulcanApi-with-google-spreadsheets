from Pastebin import PastebinClient
from Exceptions import *
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from config import cfg
import Rentry
import datetime
import re

base = declarative_base()

pastebinClient = PastebinClient(cfg['PASTEBIN_API_TOKEN'])


class Homework(base):

    __tablename__ = "Homeworks"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    scheduled_date = Column(Date)
    subject = Column(String)
    description = Column(String)

    def __repr__(self):
        return f"<Homework subject={self.subject} date={self.date} scheduled_date={self.scheduled_date}>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_to_sheet(self, sheet):
        formatted_description = self._get_formatted_description()
        formatted_date = self._get_formatted_date()
        cell = sheet.find(formatted_date)
        row = sheet.row_values(cell.row)
        text = f"{self.subject}\n{formatted_description}"
        try:
            first_empty_col = row.index('') + 1
        except ValueError:
            raise NotEnoughSpace(f"Not enough space to insert cell on {cell.row} row")
        sheet.update_cell(cell.row, first_empty_col, text)

    def _get_formatted_description(self):
        return self.description

    def _get_formatted_date(self):
        return self.scheduled_date.strftime("%d.%m")


class PhysicHomework(Homework):
    def __init__(self, *args, **kwargs):
        self.formatted_description = None
        super().__init__(*args, **kwargs)

    def _get_formatted_description(self):
        regex = r'Praca domowa(:|;)(.*?)(?:(?:\r*\n){2}|$)'
        occurrences = self._get_occurrences_in_description_using_regex(regex)
        if occurrences:
            self._set_formatted_description_from_regex_occurrences(occurrences)
        else:
            self._set_default_formatted_description()

        url = self._create_rentry_post_and_get_url()
        self._add_url_to_formatted_description(url)

        return self.formatted_description

    def _get_occurrences_in_description_using_regex(self, regex):
        occurrences = re.findall(regex, self.description, flags=re.DOTALL | re.IGNORECASE)
        return occurrences

    def _get_post_title(self):
        return f"{self.subject} - {self.date}"

    def _create_pastebin_post_and_get_url(self):
        title = self._get_post_title()
        url = pastebinClient.create_post_and_get_url(self.description, title)
        return url

    def _create_rentry_post_and_get_url(self):
        text = self._get_markdown_description()
        url = Rentry.new(text)['url']
        return url

    def _get_markdown_description(self):
        title = self._get_post_title()
        return f"# {title}\n{self.description}"

    def _add_url_to_formatted_description(self, url):
        self.formatted_description = self.formatted_description + f"\n{url}"

    def _set_formatted_description_from_regex_occurrences(self, occurrences):
        self.formatted_description = '\n'.join([x[1:] for x in occurrences[0][1:]])

    def _set_default_formatted_description(self):
        self.formatted_description = "Link: "


class HomeworkCreator:
    SPECIAL_SUBJECTS = {'Default': {'HomeworkClass': Homework},
                        'Fizyka': {'HomeworkClass': PhysicHomework}}

    def __new__(cls, *args, **kwargs):
        subject = kwargs['subject']
        if subject in cls.SPECIAL_SUBJECTS:
            homework_class = cls.SPECIAL_SUBJECTS[subject]['HomeworkClass']
        else:
            homework_class = cls.SPECIAL_SUBJECTS['Default']['HomeworkClass']
        return homework_class(**kwargs)
