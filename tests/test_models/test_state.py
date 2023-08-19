#!/usr/bin/python3
"""Unit tests for the State class"""

from tests.test_models.test_base_model import TestBaseModel
from models.state import State
import os


class TestState(TestBaseModel):
    """Test cases for the State class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State
        self.type_condition = (
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_name(self):
        """Test the data type of name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), self.type_condition)
