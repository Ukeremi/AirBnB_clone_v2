#!/usr/bin/python3
"""
Unit tests for the console (command interpreter).
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """
    Test suite for the HBNBCommand class.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """
        Tests the create command with the FileStorage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            console.onecmd('create City name="Texas"')
            model_id = cout.getvalue().strip()
            clear_stream(cout)

            self.assertIn('City.{}'.format(model_id), storage.all().keys())

            console.onecmd('show City {}'.format(model_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())

            clear_stream(cout)

            console.onecmd('create User name="James" age=17 height=5.9')
            model_id = cout.getvalue().strip()

            self.assertIn('User.{}'.format(model_id), storage.all().keys())
            clear_stream(cout)

            console.onecmd('show User {}'.format(model_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """
        Tests the create command with the DBStorage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()

            # Creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                console.onecmd('create User')

            # Creating a User instance
            clear_stream(cout)
            cmd = 'create User email="john25@gmail.com" password="123"'
            console.onecmd(cmd)
            model_id = cout.getvalue().strip()

            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            query = 'SELECT * FROM users WHERE id="{}"'.format(model_id)
            cursor.execute(query)
            result = cursor.fetchone()

            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            cursor.close()
            db_connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """
        Tests the show command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            instance = User(email="john25@gmail.com", password="123")

            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            query = 'SELECT * FROM users WHERE id="{}"'.format(instance.id)
            cursor.execute(query)
            result = cursor.fetchone()

            self.assertTrue(result is None)
            console.onecmd('show User {}'.format(instance.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            instance.save()
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            query = 'SELECT * FROM users WHERE id="{}"'.format(instance.id)
            cursor.execute(query)
            clear_stream(cout)
            console.onecmd('show User {}'.format(instance.id))
            result = cursor.fetchone()

            self.assertTrue(result is not None)
            self.assertIn('john25@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('john25@gmail.com', cout.getvalue())
            self.assertIn('123', cout.getvalue())
            cursor.close()
            db_connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """
        Tests the count command with the DBStorage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            console = HBNBCommand()
            db_connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = db_connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])

            console.onecmd('create State name="Enugu"')
            clear_stream(cout)
            console.onecmd('count State')
            cnt = cout.getvalue().strip()

            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            console.onecmd('count State')
            cursor.close()
            db_connection.close()

if __name__ == '__main__':
    unittest.main()