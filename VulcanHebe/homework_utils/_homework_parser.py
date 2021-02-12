import datetime

from VulcanHebe.homework_utils import AttachmentParser, HomeworkCreator
from VulcanHebe.Timetable import Timetable


class HomeworkParser:
    def __init__(self, timetable_dir):
        self.timetable = Timetable(timetable_dir=timetable_dir).timetable
        self._attachment_parser = AttachmentParser()

    def parse_homework_list(self, homework_list):
        homeworks = []
        for homework in homework_list:
            homeworks.append(self.parse_homework(homework))
        return homeworks

    def parse_homework(self, homework):

        return HomeworkCreator(
            id=homework.id,
            date=homework.deadline.date,
            scheduled_date=self.get_scheduled_date_from_homework(homework),
            subject=homework.subject.name,
            teacher=homework.creator.display_name,
            description=homework.content,
            attachments=self._attachment_parser.parse_attachment_list(
                homework.attachments, homework.id
            ),
        )

    def get_scheduled_date_from_homework(self, homework):
        for days in range(1, 8):
            scheduled_date = homework.deadline.date + datetime.timedelta(days=days)
            scheduled_date_day_number = scheduled_date.strftime("%w")

            if scheduled_date_day_number in ("0", "6"):
                continue

            if homework.subject.name in self.timetable[scheduled_date_day_number]:
                return scheduled_date
        raise
