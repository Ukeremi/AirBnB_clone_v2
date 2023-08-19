#!/usr/bin/python3
"""Unit tests for the Place class"""

from tests.test_models.test_base_model import TestBaseModel
from models.place import Place
import os


class TestPlace(TestBaseModel):
    """Test cases for the Place class"""

    def setUp(self):
        """Set up the test environment"""
        super().setUp()
        self.name = "Place"
        self.value = Place
        self.type_condition = (
            str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        )

    def test_city_id(self):
        """Test the data type of city_id attribute"""
        new = self.value()
        self.assertEqual(type(new.city_id), self.type_condition)

    def test_user_id(self):
        """Test the data type of user_id attribute"""
        new = self.value()
        self.assertEqual(type(new.user_id), self.type_condition)

    def test_name(self):
        """Test the data type of name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), self.type_condition)

    def test_description(self):
        """Test the data type of description attribute"""
        new = self.value()
        self.assertEqual(type(new.description), self.type_condition)

    def test_number_rooms(self):
        """Test the data type of number_rooms attribute"""
        new = self.value()
        self.assertEqual(type(new.number_rooms), self.type_condition)

    def test_number_bathrooms(self):
        """Test the data type of number_bathrooms attribute"""
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), self.type_condition)

    def test_max_guest(self):
        """Test the data type of max_guest attribute"""
        new = self.value()
        self.assertEqual(type(new.max_guest), self.type_condition)

    def test_price_by_night(self):
        """Test the data type of price_by_night attribute"""
        new = self.value()
        self.assertEqual(type(new.price_by_night), self.type_condition)

    def test_latitude(self):
        """Test the data type of latitude attribute"""
        new = self.value()
        self.assertEqual(type(new.latitude), self.type_condition)

    def test_longitude(self):
        """Test the data type of longitude attribute"""
        new = self.value()
        self.assertEqual(type(new.longitude), self.type_condition)

    def test_amenity_ids(self):
        """Test the data type of amenity_ids attribute"""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), self.type_condition)
