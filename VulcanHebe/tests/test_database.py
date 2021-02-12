import os
import unittest

import sqlalchemy.orm

from VulcanHebe.database_utils import DatabaseConnectionCreator


class ConnectionTest(unittest.TestCase):
    def test_connection(self):
        session = DatabaseConnectionCreator("sqlite:///test_db.db")
        self.assertIsInstance(session, sqlalchemy.orm.session.Session)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
