import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class SheetClient:
    def __init__(self, dir):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name(dir, scope)

        client = gspread.authorize(creds)

        self.sheet = client.open("Zdalne nauczanie 2aG").get_worksheet(1)

    def main(self):
        data = self.sheet.batch_get(["A1:ZZ"], date_time_render_option="FORMATTED_STRING")  # Get a list of all records

        cell = self.sheet.find("27.01")
        print(cell.row, cell.col)


if __name__ == "__main__":
    client = SheetClient()
    client.main()
