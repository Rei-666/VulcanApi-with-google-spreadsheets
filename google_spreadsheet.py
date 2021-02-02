import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetClient:
    def __init__(self, directory):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name(directory, scope)

        client = gspread.authorize(creds)

        self.sheet = client.open("Zdalne nauczanie 2aG").get_worksheet(1)
