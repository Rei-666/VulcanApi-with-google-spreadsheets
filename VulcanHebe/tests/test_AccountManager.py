import unittest
from AccountManager import AccountManager
from KeystoreManager import KeystoreManager
from vulcan import VulcanHebe


class AccountManagerTest(unittest.IsolatedAsyncioTestCase):

    async def test_registering(self):
        keystore_manager = KeystoreManager("keystore.json")

        account_manager = AccountManager("account.json")
        account_manager.register(keystore_manager.key, "FK100000", "powiatwulkanowy", "999999")

        client = VulcanHebe(keystore_manager.key, account_manager.account)
        await client.close()

