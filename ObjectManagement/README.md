# Usage Guide for AirBnB Clone - Object Management

This guide provides detailed instructions on how to use the scripts within the AirBnB clone project for managing `BaseModel` and `User` objects, including creating new instances, saving them to a file, and reloading them. The scripts also demonstrate converting objects to a dictionary representation and initializing objects from dictionaries.

## Introduction

The provided Python scripts demonstrate the functionality of the `BaseModel` and `User` classes within the AirBnB clone project. These classes allow for creating and manipulating objects related to the AirBnB clone's functionality, including managing users and other entities within the system.

## Creating and Using BaseModel Instances

To create and interact with `BaseModel` instances, follow these steps:

1. Import the `BaseModel` class from the `models.base_model` module.
2. Instantiate a new `BaseModel` object.
3. Assign attributes to the object as needed (e.g., `name` and `my_number`).
4. Use the `.save()` method to update the object's `updated_at` timestamp.
5. Convert the object to a dictionary representation using the `.to_dict()` method.

Example usage:

```python
from models.base_model import BaseModel

my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model.to_dict())
```

## Creating and Using User Instances

To manage `User` objects, which inherit from `BaseModel`:

1. Import the `User` class from the `models.user` module.
2. Create a new `User` instance and set attributes such as `first_name`, `last_name`, `email`, and `password`.
3. Save the object to update its timestamp and optionally convert it to a dictionary for storage or transmission.

Example usage:

```python
from models.user import User

my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "airbnb@mail.com"
my_user.password = "root"
my_user.save()
print(my_user.to_dict())
```

## Persisting Objects to a File

Objects are automatically saved to a JSON file (`file.json`) by calling the `.save()` method, which uses the `FileStorage` system to serialize object data into JSON format for persistence.

## Reloading Objects from a File

Upon startup, the system automatically reloads existing objects from `file.json` into the current session, allowing for persistent storage across sessions.

```python
from models import storage

all_objs = storage.all()
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)
```

For more advanced usage and interaction with these objects, refer to the scripts provided for detailed examples of creating, saving, reloading, and managing objects within the AirBnB clone project.
