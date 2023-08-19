#!/usr/bin/python3
"""Test cases for the City class"""

from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os

class TestCity(test_basemodel):
    """Test cases for the City class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City
        self.type_condition = (
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_state_id(self):
        """Test the data type of state_id attribute"""
        new = self.value()
        self.assertEqual(type(new.state_id), self.type_condition)

    def test_name(self):
        """Test the data type of name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), self.type_condition)
