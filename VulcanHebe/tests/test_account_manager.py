import unittest

from vulcan import VulcanHebe

from VulcanHebe.vulcan_utils import AccountFileManager, KeystoreFileManager


class AccountManagerTest(unittest.IsolatedAsyncioTestCase):
    async def test_registering(self):
        keystore_manager = KeystoreFileManager("keystore.json")

        account_manager = AccountFileManager("account.json")
        await account_manager.register_and_save(
            keystore_manager.key, "FK100000", "powiatwulkanowy", "999999"
        )

        client = VulcanHebe(keystore_manager.key, account_manager.account)
        await client.close()
