from sqlalchemy import Column, ForeignKey, Integer

from VulcanHebe.database_utils import base


class Cell(base):
    __tablename__ = "Cells"
    id = Column(Integer, primary_key=True)
    column = Column(Integer)
    row = Column(Integer)
    homework = Column(Integer, ForeignKey("Homeworks.id"))

    def __repr__(self):
        return f"<Cell column={self.column} row={self.row} homework={self.homework}>"
