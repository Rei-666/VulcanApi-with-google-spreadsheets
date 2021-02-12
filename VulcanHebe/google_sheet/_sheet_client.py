import gspread
from oauth2client.service_account import ServiceAccountCredentials

from VulcanHebe.models import Cell

from .Exceptions import NotEnoughSpace


class SheetClient:
    def __init__(self, directory, sheet_name):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(directory, scope)

        client = gspread.authorize(creds)

        self.sheet = client.open(sheet_name).get_worksheet(1)

    def add_homework_to_sheet_and_get_cell(self, homework):
        formatted_description = homework.get_formatted_description()
        formatted_date = homework.get_formatted_date()

        cell = self.sheet.find(formatted_date)
        row = self.sheet.row_values(cell.row)
        text = f"{homework.subject}\n{formatted_description}"

        try:
            first_empty_col = row.index("") + 1
        except ValueError:
            raise NotEnoughSpace(f"Not enough space to insert cell on {cell.row} row")
        self.sheet.update_cell(cell.row, first_empty_col, text)

        return Cell(column=first_empty_col, row=cell.row, homework=homework.id)
