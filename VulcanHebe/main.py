from VulcanHebe.KeystoreFileManager import KeystoreFileManager
from VulcanHebe.AccountFileManager import AccountFileManager
from vulcan import VulcanHebe
import asyncio


async def main():
    keystore_manager = KeystoreFileManager("keystore.json")
    account_manager = AccountFileManager("account.json")

    if not account_manager.account:
        await account_manager.register_and_save(keystore_manager.key, "Token", "Symbol", "PIN")

    client = VulcanHebe(keystore_manager.key, account_manager.account)

    await client.select_student()

    await client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
