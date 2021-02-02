from vulcan import Vulcan
import datetime
import json
import os
import re
from write_as_api import create_post
from google_spreadsheet import SheetClient
from Homework import Homework

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(ROOT_DIR, 'cert.json')
CRED_DIR = os.path.join(ROOT_DIR, 'creds.json')
TIMETABLE_DIR = os.path.join(ROOT_DIR, 'timetable.json')


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

with open(CERT_DIR) as f:
    certificate = json.load(f)

client = Vulcan(certificate)

date_from = datetime.datetime.now().date() - datetime.timedelta(days=7)

timetable = Timetable(TIMETABLE_DIR).timetable


def get_homework_list():
    all_homeworks = [x for x in client.get_homework(date_from=date_from, date_to=datetime.datetime.now().date())]
    homework_list = []
    for homework in all_homeworks:
        for i in range(1, 8):
            next_day = homework.date + datetime.timedelta(days=i)
            next_day_number = next_day.strftime("%w")

            if next_day_number in ('0', '6'):
                continue

            if homework.subject.name in timetable[next_day_number]:
                new_homework = Homework(id=homework.id, date=next_day, subject=homework.subject.name, description=homework.description)
                homework_list.append(new_homework)
    return homework_list


if __name__ == "__main__":
    pass