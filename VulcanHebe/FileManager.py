import os


class FileManager:
    @staticmethod
    def _is_file_exists(directory):
        if os.path.isfile(directory):
            return True
        return False
