from vulcan import Vulcan
import datetime
import json
import os
import re
from write_as_api import create_post
from google_spreadsheet import SheetClient


class Timetable:
    def __init__(self, timetable_dir=None):
        if timetable_dir is not None:
            with open(timetable_dir) as f:
                timetable = json.load(f)
            self.timetable = timetable

    @staticmethod
    def get_timetable(client, filename):
        lessons = {}
        lessons_dictionary = client.get_lessons(date_from=date_from, date_to=datetime.datetime.now().date())
        for x in lessons_dictionary:
            date = int(x.date.strftime("%w"))
            if date not in lessons:
                lessons[date] = []
            if x.visible:
                lessons[date].append(x.subject.name)
        with open(TIMETABLE_DIR, 'w') as f:
            json.dump(lessons, f, indent=4, sort_keys=True)


class Homework:
    SPECIAL_CASES = ['Fizyka']

    def __init__(self, homework, scheduled_date):
        self.scheduled_date = scheduled_date
        self.subject = homework.subject.name
        self.description = homework.description

        if self.subject in self.SPECIAL_CASES:
            self.format_description()

    def add_to_sheet(self, sheet):
        formatted_date = self.scheduled_date.strftime("%d.%m")
        cell = sheet.find(formatted_date)
        row = sheet.row_values(cell.row)
        text = f"{self.subject}\n{self.description}"
        sheet.update_cell(cell.row, row.index('')+1, text)

    def format_description(self):
        if self.subject == "Fizyka":
            regex = r'Praca domowa(:|;)(.*?)(?:(?:\r*\n){2}|$)'
            post = create_post(self.description, self.subject)
            occurences = re.findall(regex, self.description, flags=re.DOTALL|re.IGNORECASE)
            self.description = '\n'.join([x[1:] for x in occurences[0][1:]])
            self.description += f'\n{post})'


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(ROOT_DIR, 'cert.json')
CRED_DIR = os.path.join(ROOT_DIR, 'creds.json')
TIMETABLE_DIR = os.path.join(ROOT_DIR, 'timetable.json')

with open(CERT_DIR) as f:
    certificate = json.load(f)


client = Vulcan(certificate)

date_from = datetime.datetime.now().date() - datetime.timedelta(days=2)

timetable = Timetable(TIMETABLE_DIR).timetable


def main():

    sheet = SheetClient(CRED_DIR)

    all_homeworks = [x for x in client.get_homework(date_from=date_from, date_to=datetime.datetime.now().date())]
    for homework in all_homeworks:
        description = homework.description.split('\n')
        print(f"{homework.date} {homework.date.strftime('%w')} {homework.subject.name} {description[0:2]}")

        for i in range(1, 8):
            next_day = homework.date + datetime.timedelta(days=i)
            next_day_number = next_day.strftime("%w")

            if next_day_number in ('0', '6'):
                continue

            if homework.subject.name in timetable[next_day_number]:
                new_homework = Homework(homework, next_day)
                new_homework.add_to_sheet(sheet.sheet)
                formatted_date = next_day.strftime("%d.%m")
                print(f"jest zadane na {formatted_date}")
                break


main()