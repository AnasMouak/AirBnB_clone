#!/usr/bin/python3
"""Unittests for file_storage.py."""

import os
import json
import models
import unittest
import subprocess
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestCodeStyle(unittest.TestCase):
    """Unittests for checking the PEP8 compliance of file_storage.py."""

    def test_pycodestyle_conformance(self):
        """Test that file_storage.py conforms to PEP8."""
        # Adjust the path to your file_storage.py
        file_storage_path = os.path.join('models', 'engine', 'file_storage.py')
        pycodestyle_check = subprocess.run(
            ['pycodestyle', file_storage_path],
            capture_output=True, text=True
        )
        if pycodestyle_check.returncode != 0:
            errors = pycodestyle_check.stdout.strip().split('\n')
            red = '\033[91m'
            yellow = '\033[93m'
            cyan = '\033[96m'
            reset = '\033[0m'
            formatted_errors = '\n'.join([
                f"{red}Error: {yellow}{error}{reset}" for error in errors
            ])
            error_message = (
                f"{cyan}Pycodestyle violations:{reset}\n{formatted_errors}"
            )
            self.fail(msg=error_message)


class TestFileStorage_instantiation(unittest.TestCase):
    """Tests instances and storage initialization."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Tests FileStorage methods."""
    @classmethod
    def setUp(self):
        """Remove file.json if it exists to start fresh."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Clean up file.json after tests."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """'all' should return a dict."""
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """'all' doesn't take args."""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        """'new' should add objects."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args(self):
        """'new' with unexpected args should fail."""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        """'save' should write to file."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(self):
        """'save' doesn't take args."""
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        """'reload' should load objects from file."""
        a_storage = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        with open("file.json", "w") as f:
            f.write("{}")
        with open("file.json", "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(a_storage.reload(), None)

    def test_reload_with_arg(self):
        """'reload' doesn't take args."""
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
