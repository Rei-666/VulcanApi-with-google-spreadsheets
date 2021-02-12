import re

from config import cfg
from GenerateLinks import Rentry
from GenerateLinks.Pastebin import PastebinClient
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from VulcanHebe.database_utils import base

pastebinClient = PastebinClient(cfg["PASTEBIN_API_TOKEN"])


class Homework(base):
    __tablename__ = "Homeworks"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    scheduled_date = Column(Date)
    teacher = Column(String)
    subject = Column(String)
    description = Column(String)
    attachments = relationship("Attachment", cascade="all, delete")

    def __repr__(self):
        return f"<Homework subject={self.subject} date={self.date} scheduled_date={self.scheduled_date}>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_formatted_description(self):
        return self.description

    def get_formatted_date(self):
        return self.scheduled_date.strftime("%d.%m")


class PhysicHomework(Homework):
    def __init__(self, *args, **kwargs):
        self.formatted_description = None
        super().__init__(*args, **kwargs)

    def get_formatted_description(self):
        regex = r"Praca domowa(:|;)(.*?)(?:(?:\r*\n){2}|$)"
        occurrences = self._get_occurrences_in_description_using_regex(regex)
        if occurrences:
            self._set_formatted_description_from_regex_occurrences(occurrences)
        else:
            self._set_default_formatted_description()

        url = self._create_rentry_post_and_get_url()
        self._add_url_to_formatted_description(url)

        return self.formatted_description

    def _get_occurrences_in_description_using_regex(self, regex):
        occurrences = re.findall(
            regex, self.description, flags=re.DOTALL | re.IGNORECASE
        )
        return occurrences

    def _get_post_title(self):
        return f"{self.subject} - {self.date}"

    def _create_pastebin_post_and_get_url(self):
        title = self._get_post_title()
        url = pastebinClient.create_post_and_get_url(self.description, title)
        return url

    def _create_rentry_post_and_get_url(self):
        text = self._get_markdown_description()
        url = Rentry.new(text)["url"]
        return url

    def _get_markdown_description(self):
        title = self._get_post_title()
        return f"# {title}\n{self.description}"

    def _add_url_to_formatted_description(self, url):
        self.formatted_description = self.formatted_description + f"\n{url}"

    def _set_formatted_description_from_regex_occurrences(self, occurrences):
        self.formatted_description = "\n".join([x[1:] for x in occurrences[0][1:]])

    def _set_default_formatted_description(self):
        self.formatted_description = "Link: "
