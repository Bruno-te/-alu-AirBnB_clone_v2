import unittest
import MySQLdb
from os import getenv
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

class TestCreateStateDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySQLdb.connect(
            host=getenv("HBNB_MYSQL_HOST"),
            user=getenv("HBNB_MYSQL_USER"),
            passwd=getenv("HBNB_MYSQL_PWD"),
            db=getenv("HBNB_MYSQL_DB")
        )
        cls.cursor = cls.db.cursor()

    def test_create_state(self):
        # Get current number of states
        self.cursor.execute("SELECT COUNT(*) FROM city;")
        before = self.cursor.fetchone()[0]

        # Run the console command
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="kigali"')
            new_id = f.getvalue().strip()

        # Get new number of states
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        after = self.cursor.fetchone()[0]

        self.assertEqual(after, before + 1)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.db.close()
