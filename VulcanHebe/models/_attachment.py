from sqlalchemy import Column, ForeignKey, Integer, String

from VulcanHebe.database_utils import base


class Attachment(base):
    __tablename__ = "Attachments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    homework = Column(Integer, ForeignKey("Homeworks.id"))

    def __repr__(self):
        return (
            f"<Attachment name={self.name} link={self.link} homework={self.homework}>"
        )
