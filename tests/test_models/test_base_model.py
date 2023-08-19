#!/usr/bin/python3
"""Unit tests for BaseModel class"""

from models.base_model import BaseModel, Base
from datetime import datetime
import unittest
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'BaseModel tests not supported for DB storage')
class TestBaseModel(unittest.TestCase):
    """Test class for the BaseModel model"""

    def setUp(self):
        """Set up test environment"""
        self.name = 'BaseModel'
        self.value = BaseModel()

    def tearDown(self):
        """Tear down test environment"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Test the initialization of the model class."""
        # Check if the instance is of the expected class
        self.assertIsInstance(self.value, BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value, Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """Test default initialization of BaseModel."""
        i = self.value
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test BaseModel with kwargs."""
        i = self.value
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test BaseModel with int kwargs."""
        i = self.value
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Test the save method."""
        i = self.value
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test the str method."""
        i = self.value
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_to_dict(self):
        """Test the to_dict method."""
        i = self.value
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

        self.assertIsInstance(self.value.to_dict(), dict)

        self.assertIn('id', self.value.to_dict())
        self.assertIn('created_at', self.value.to_dict())
        self.assertIn('updated_at', self.value.to_dict())

        # Testing additional attributes and data types
        model = self.value
        model.firstname = 'Celestine'
        model.lastname = 'Akpanoko'

        new_instance = BaseModel(firstname='Celestine')
        self.assertIn('firstname', new_instance.to_dict())
        self.assertIn('lastname', new_instance.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())

        # Testing data types of datetime attributes
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)

        # Testing to_dict output
        datetime_now = datetime.today()
        model = self.value
        model.id = '012345'
        model.created_at = model.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': model.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(model.to_dict(), to_dict)

        # Additional testing for different scenarios
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34', age=13).to_dict(),
                {
                    '__class__': model.__class__.__name__,
                    'id': 'u-b34',
                    'age': 13
                }
            )
            self.assertDictEqual(
                self.value(id='u-b34', age=None).to_dict(),
                {
                    '__class__': model.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )

        # More testing for consistency and coverage
        model_d = self.value
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(model_d.to_dict(), model_d.__dict__)
        self.assertNotEqual(
            model_d.to_dict()['__class__'],
            model_d.__class__
        )

        # Additional testing for invalid arguments
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """Test kwargs with None."""
        n = {None: None}
        with self.assertRaises(TypeError):
            n = self.value(**n)

    def test_kwargs_one(self):
        """Test kwargs with one arg."""
        n = {'id': '1'}
        new = BaseModel(**n)
        self.assertEqual(new.id, '1')

    def test_id(self):
        """Test id attribute of the model."""
        new = self.value
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test created_at attribute."""
        new = self.value
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Test updated_at attribute."""
        new = self.value
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
