#!/usr/bin/python3
"""Unit tests for the Review class"""

from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os


class TestReview(test_basemodel):
    """Test cases for the Review class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review
        self.type_condition = (
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_place_id(self):
        """Test the data type of place_id attribute"""
        new = self.value()
        self.assertEqual(type(new.place_id), self.type_condition)

    def test_user_id(self):
        """Test the data type of user_id attribute"""
        new = self.value()
        self.assertEqual(type(new.user_id), self.type_condition)

    def test_text(self):
        """Test the data type of text attribute"""
        new = self.value()
        self.assertEqual(type(new.text), self.type_condition)
