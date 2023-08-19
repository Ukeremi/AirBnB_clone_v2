#!/usr/bin/python3
"""Unit tests for the User class"""

from tests.test_models.test_base_model import TestBaseModel
from models.user import User
import os


class TestUser(TestBaseModel):
    """Test cases for the User class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User
        self.type_condition = (
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_first_name(self):
        """Test the data type of first_name attribute"""
        new = self.value()
        self.assertEqual(type(new.first_name), self.type_condition)

    def test_last_name(self):
        """Test the data type of last_name attribute"""
        new = self.value()
        self.assertEqual(type(new.last_name), self.type_condition)

    def test_email(self):
        """Test the data type of email attribute"""
        new = self.value()
        self.assertEqual(type(new.email), self.type_condition)

    def test_password(self):
        """Test the data type of password attribute"""
        new = self.value()
        self.assertEqual(type(new.password), self.type_condition)
