from VulcanHebe.models import Homework, PhysicHomework


class HomeworkCreator:
    SPECIAL_SUBJECTS = {
        "Default": {"HomeworkClass": Homework},
        "Fizyka": {"HomeworkClass": PhysicHomework},
    }

    def __new__(cls, *args, **kwargs):
        subject = kwargs["subject"]
        if subject in cls.SPECIAL_SUBJECTS:
            homework_class = cls.SPECIAL_SUBJECTS[subject]["HomeworkClass"]
        else:
            homework_class = cls.SPECIAL_SUBJECTS["Default"]["HomeworkClass"]
        return homework_class(**kwargs)
