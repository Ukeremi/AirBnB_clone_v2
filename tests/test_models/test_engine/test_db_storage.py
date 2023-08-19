#!/usr/bin/python3
"""Module for testing DB storage"""
import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'DB storage test not supported')
class TestDBStorage(unittest.TestCase):
    """Test cases for the DB storage engine"""

    def setUp(self):
        """Set up the test environment by establishing a database connection"""
        self.db = MySQLdb.connect(
            user=os.getenv('HBNB_MYSQL_USER'),
            host=os.getenv('HBNB_MYSQL_HOST'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            port=3306,
            db=os.getenv('HBNB_MYSQL_DB')
        )
        self.cur = self.db.cursor()

    def tearDown(self):
        """Tear down the test environment by closing the database connection"""
        self.cur.close()
        self.db.close()

    def test_create_and_save_user(self):
        """Test creating and saving a user to the database"""
        # Create a new user instance
        new_user = User(
            email='jack@bond.com',
            password='12345',
            first_name='jack',
            last_name='bond'
        )

        # Get the count of users before saving the new user
        old_count = self.execute_query('SELECT COUNT(*) FROM users')

        # Save the new user
        new_user.save()

        # Get the count of users after saving the new user
        new_count = self.execute_query('SELECT COUNT(*) FROM users')

        # Assert that the count increased by one, indicating successful save
        self.assertEqual(new_count, old_count + 1)

    def test_create_and_check_user(self):
        """
        Test creating a new user, saving it,
        and checking its details in the database
        """
        # Create a new user instance
        new_user = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )

        # Ensure the user is not in the storage
        self.assertNotIn(new_user, storage.all().values())

        # Save the new user
        new_user.save()

        # Ensure the user is now in the storage
        self.assertIn(new_user, storage.all().values())

        # Retrieve the user's details from the database
        query = 'SELECT * FROM users WHERE id="{}"'.format(new_user.id)
        result = self.execute_query(query)

        # Check if the user's details match the expected values
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)

    def test_delete_user(self):
        """Test deleting a user from the database"""
        # Create a new user instance
        new_user = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )

        # Save the new user
        new_user.save()

        # Ensure the user is in the storage
        self.assertTrue(new_user in storage.all().values())

        # Delete the user
        new_user.delete()

        # Ensure the user is removed from the storage
        self.assertNotIn(new_user, storage.all().values())

    def test_reload(self):
        """Test reloading the database session"""
        # Insert a new user directly into the database
        query = (
            'INSERT INTO users('
            'id, '
            'created_at, '
            'updated_at, '
            'email, '
            'password, '
            'first_name, '
            'last_name) '
            'VALUES(%s, %s, %s, %s, %s, %s, %s);'
        )
        params = [
            '4447-by-me',
            str(datetime.now()),
            str(datetime.now()),
            'ben_pike@yahoo.com',
            'pass',
            'Benjamin',
            'Pike',
        ]

        self.execute_query(query, params)

        # Ensure the user is not in the storage
        self.assertNotIn('User.4447-by-me', storage.all())

        # Reload the storage
        storage.reload()

        # Ensure the user is now in the storage
        self.assertIn('User.4447-by-me', storage.all())

    def test_save_user(self):
        """Test saving a user to the database"""
        # Create a new user instance
        new_user = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )

        # Retrieve the user's details from the database before saving
        query = 'SELECT * FROM users WHERE id="{}"'.format(new_user.id)
        result = self.execute_query(query)

        # Get the count of users before saving the new user
        old_count = self.execute_query('SELECT COUNT(*) FROM users;')

        # Ensure the user is not in the storage
        self.assertTrue(result is None)
        self.assertNotIn(new_user, storage.all().values())

        # Save the new user
        new_user.save()

        # Retrieve the user's details from the database after saving
        query = 'SELECT * FROM users WHERE id="{}"'.format(new_user.id)
        result = self.execute_query(query)

        # Get the count of users after saving the new user
        new_count = self.execute_query('SELECT COUNT(*) FROM users;')

        # Ensure the user is now in the storage and the count increased by one
        self.assertTrue(result is not None)
        self.assertEqual(old_count + 1, new_count)
        self.assertIn(new_user, storage.all().values())

    def execute_query(self, query, params=None):
        """Execute a MySQL query and return the result"""
        if params:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)
        return self.cur.fetchone()[0]
