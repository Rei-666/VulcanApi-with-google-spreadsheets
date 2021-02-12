import datetime
import json


class Timetable:
    def __init__(self, timetable_dir=None):
        if timetable_dir is not None:
            with open(timetable_dir) as f:
                timetable = json.load(f)
            self.timetable = timetable

    @classmethod
    async def get_and_save_timetable_to_file(cls, client, filename):
        lessons = {}
        lessons_dictionary = await cls.get_lessons_dictionary(client)
        async for x in lessons_dictionary:
            date = int(x.date.strftime("%w"))
            if date not in lessons:
                lessons[date] = []
            if x.visible:
                lessons[date].append(x.subject.name)

        with open(filename, "w") as f:
            json.dump(lessons, f, indent=4, sort_keys=True)

    @staticmethod
    async def get_lessons_dictionary(client):
        date_now = datetime.datetime.now().date()
        date_week_ago = datetime.datetime.now().date() - datetime.timedelta(days=7)
        return await client.data.get_lessons(date_from=date_week_ago, date_to=date_now)
