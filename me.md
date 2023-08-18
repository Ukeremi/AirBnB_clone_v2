# HBNB - The Console

This repository contains the initial stage of a student project to build a clone of the AirBnB website. This stage implements a backend interface, or console, to manage program data. Console commands allow the user to create, update, and destroy objects, as well as manage file storage. Using a system of JSON serialization/deserialization, storage is persistent between sessions.

---

## Table of Contents

- [Contributors](#contributors)
- [Project Tasks](#project-tasks)
- [Repository Contents](#repository-contents)
- [General Use](#general-use)
- [Examples](#examples)

---

## Contributors

These individuals contributed to the hbnb project in this repository:

- Ezra Nobrega <ezra.nobrega@outlook.com>
- Justin Majetich <justinmajetich@gmail.com>
- Dr Dyrane Alexander <Ogranya.Alex@gmail.com>
- Ukeremi <ukpono9@gmail.com>

---

## Project Tasks

1. **Authors/README File:** [AUTHORS](https://github.com/justinmajetich/AirBnB_clone/blob/dev/AUTHORS) - Project authors
2. **Pep8:** N/A - All code is pep8 compliant
3. **Unit Testing:** [/tests](https://github.com/justinmajetich/AirBnB_clone/tree/dev/tests) - All class-defining modules are unittested
4. **Make BaseModel:** [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) - Defines a parent class to be inherited by all model classes
5. **Update BaseModel w/ kwargs:** [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) - Add functionality to recreate an instance of a class from a dictionary representation
6. **Create FileStorage class:** [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) [/models/__init__.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/__init__.py) [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) - Defines a class to manage persistent file storage system
7. **Console 0.0.1:** [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) - Add basic functionality to the console program, allowing it to quit, handle empty lines and ^D
8. **Console 0.1:** [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) - Update the console with methods allowing the user to create, destroy, show, and update stored data
9. **Create User class:** [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py) - Dynamically implement a user class
10. **More Classes:** [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py) [/models/place.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/place.py) [/models/city.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/city.py) [/models/amenity.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/amenity.py) [/models/state.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/state.py) [/models/review.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/review.py) - Dynamically implement more classes
11. **Console 1.0:** [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) - Update the console and file storage system to work dynamically with all classes, update file storage

---

## Repository Contents

For detailed information about the repository contents and files, please refer to the project tasks and links provided above.

---

## General Use

1. First clone this repository.

2. Once the repository is cloned, locate the "console.py" file and run it as follows:
   ```
   /AirBnB_clone$ ./console.py
   ```

3. When this command is run, the following prompt should appear:
   ```
   (hbnb)
   ```

4. This prompt designates you are in the "HBnB" console. There are a variety of commands available within the console program.

### Commands

- `create` - Creates an instance based on the given class
- `destroy` - Destroys an object based on class and UUID
- `show` - Shows an object based on class and UUID
- `all` - Shows all objects the program has access to, or all objects of a given class
- `update` - Updates existing attributes of an object based on class name and UUID
- `quit` - Exits the program (EOF will as well)

### Alternative Syntax

Users are able to issue a number of console commands using an alternative syntax:

- Usage: `<class_name>.<command>([<id>[name_arg value_arg]|[kwargs]])`

Advanced syntax is implemented for the following commands:

- `all` - Shows all objects the program has access to, or all objects of a given class
- `count` - Returns the number of object instances by class
- `show` - Shows an object based on class and UUID
- `destroy` - Destroys an object based on class and UUID
- `update` - Updates existing attributes of an object based on class name and UUID

---

## Examples