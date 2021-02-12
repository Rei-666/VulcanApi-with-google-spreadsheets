import asyncio

from vulcan import VulcanHebe

from config import cfg
from VulcanHebe.database_utils import DatabaseConnectionCreator, merge_all
from VulcanHebe.google_sheet import SheetClient
from VulcanHebe.homework_utils import HomeworkGetter, HomeworkParser
from VulcanHebe.models import Cell, Homework
from VulcanHebe.vulcan_utils import AccountFileManager, KeystoreFileManager


async def main():
    keystore_manager = KeystoreFileManager("keystore.json")
    account_manager = AccountFileManager("account.json")

    if not account_manager.account:
        await account_manager.register_and_save(
            keystore_manager.key, "Token", "Symbol", "PIN"
        )

    client = VulcanHebe(keystore_manager.key, account_manager.account)
    await client.select_student()

    homework_getter = HomeworkGetter(client)
    homeworks = await homework_getter.get_homework_list()

    homework_parser = HomeworkParser(cfg["TIMETABLE_DIR"])
    parsed_homeworks = homework_parser.parse_homework_list(homeworks)

    session = DatabaseConnectionCreator(cfg["DATABASE"])
    merge_all(session, Homework, parsed_homeworks)
    session.commit()

    sheet_client = SheetClient(cfg["GOOGLE_SHEET_CREDENTIALS_DIR"], cfg["SHEET_NAME"])

    add_homeworks_to_sheet_and_update_cells_in_database(
        parsed_homeworks, sheet_client, session
    )

    await client.close()


def add_homeworks_to_sheet_and_update_cells_in_database(
    homeworks, sheet_client, session
):
    for homework in homeworks:
        is_in_sheet = session.query(Cell).filter(Cell.homework == homework.id).first()
        if not is_in_sheet:
            try:
                cell = sheet_client.add_homework_to_sheet_and_get_cell(homework)
            except KeyError:
                pass
            else:
                session.add(cell)
    session.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
