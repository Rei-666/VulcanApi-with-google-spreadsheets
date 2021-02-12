from vulcan import Keystore

from VulcanHebe.vulcan_utils import FileManager


class KeystoreFileManager(FileManager):
    def __init__(self, directory):
        self.key = None

        if self._is_file_exists(directory):
            self._load(directory)
        else:
            self._generate_key()
            self._save(directory)

    def _generate_key(self, **kwargs):
        self.key = Keystore.create(**kwargs)

    def _save(self, directory):
        with open(directory, "w") as f:
            f.write(self.key.as_json)

    def _load(self, directory):
        with open(directory) as f:
            self.key = Keystore.load(f)


if __name__ == "__main__":
    keystore_handler = KeystoreFileManager("keystore.json")
    print(keystore_handler.key)
