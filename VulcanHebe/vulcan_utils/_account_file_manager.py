from vulcan import Account

from VulcanHebe.vulcan_utils import FileManager


class AccountFileManager(FileManager):
    def __init__(self, directory):
        self.account = None
        self.directory = directory
        if self._is_file_exists(directory):
            self._load(directory)

    async def register_and_save(self, keystore, token, symbol, pin):
        self.account = await Account.register(keystore, token, symbol, pin)
        self._save(self.directory)

    def _save(self, directory):
        with open(directory, "w") as f:
            f.write(self.account.as_json)

    def _load(self, directory):
        with open(directory) as f:
            self.account = Account.load(f)
