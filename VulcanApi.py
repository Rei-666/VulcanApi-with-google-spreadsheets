from vulcan import Vulcan
from config import cfg
import datetime
import json
from Homework import HomeworkCreator


class Timetable:
    def __init__(self, timetable_dir=None):
        if timetable_dir is not None:
            with open(timetable_dir) as f:
                timetable = json.load(f)
            self.timetable = timetable

    @staticmethod
    def get_timetable(client, filename):
        date_now = datetime.datetime.now().date()
        date_week_ago = datetime.datetime.now().date() - datetime.timedelta(days=7)
        lessons = {}
        lessons_dictionary = client.get_lessons(date_from=date_week_ago, date_to=date_now)
        for x in lessons_dictionary:
            date = int(x.date.strftime("%w"))
            if date not in lessons:
                lessons[date] = []
            if x.visible:
                lessons[date].append(x.subject.name)
        with open(filename, 'w') as f:
            json.dump(lessons, f, indent=4, sort_keys=True)


with open(cfg['VULCAN_API_CERT_DIR']) as f:
    certificate = json.load(f)

vulcan_client = Vulcan(certificate)

timetable = Timetable(cfg['TIMETABLE_DIR']).timetable


def get_homework_list(date_from=None):
    date_now = datetime.datetime.now().date()
    if not date_from:
        date_from = date_now - datetime.timedelta(days=7)

    all_homeworks = [homework for homework in vulcan_client.get_homework(date_from=date_from, date_to=date_now)]

    homework_list = []
    for homework in all_homeworks:
        for i in range(1, 8):
            next_day = homework.date + datetime.timedelta(days=i)
            next_day_number = next_day.strftime("%w")

            if next_day_number in ('0', '6'):
                continue

            if homework.subject.name in timetable[next_day_number]:
                new_homework = HomeworkCreator(id=homework.id,
                                               date=homework.date,
                                               scheduled_date=next_day,
                                               subject=homework.subject.name,
                                               description=homework.description)
                homework_list.append(new_homework)
    return homework_list
