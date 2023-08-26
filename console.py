#!/usr/bin/python3
"""Console Module"""
import re
import uuid
import os
from datetime import datetime
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    # Determines the prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''  # Initialize line elements

        # Scan for general formatting - i.e., '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line left to right
            pline = line[:]  # Parsed line

            # Isolate <class name>
            _cls = pline[:pline.find('.')]

            # Isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # If parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline converted to tuple

                # Isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # Possible bug here: empty quotes register as
                # empty _id when replaced

                # If arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # Check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, args):
        """Create an object of any class"""
        skipped_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        pattern = r'(?P<class_name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'

        # Match the class name from the args
        class_match = re.match(pattern, args)
        data = {}

        if class_match is not None:
            class_name = class_match.group('class_name')
            param_str = args[len(class_name):].strip()
            params = param_str.split(' ')
            param_pattern = (
                r'{}=({}|{}|{})'.format(
                    pattern,
                    r'(?P<str_val>"([^"]|\")*")',
                    r'(?P<float_val>[-+]?\d+\.\d+)',
                    r'(?P<int_val>[-+]?\d+)'
                )
            )

            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('class_name')
                    str_val = param_match.group('str_val')
                    float_val = param_match.group('float_val')
                    int_val = param_match.group('int_val')

                    if float_val is not None:
                        data[key_name] = float(float_val)
                    if int_val is not None:
                        data[key_name] = int(int_val)
                    if str_val is not None:
                        data[key_name] = str_val[1:-1].replace('_', ' ')

        else:
            class_name = args

        # Check for missing class name or non-existent class
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create and save the instance based on the storage type
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            # Set default values if using database storage
            data.setdefault('id', str(uuid.uuid4()))
            data.setdefault('created_at', str(datetime.now()))
            data.setdefault('updated_at', str(datetime.now()))

            # Create and save the instance
            new_instance = HBNBCommand.classes[class_name](**data)
            new_instance.save()
            print(new_instance.id)
        else:
            # Create and save the instance with attributes
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in data.items():
                if key not in skipped_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates an instance of a class")
        print("[Usage]: create <className> "
              "[attribute_name=attribute_value ...]\n")

    def do_show(self, args):
        """Method to show an individual object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # Guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            obj = storage.get(key)
            print(obj)
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            obj = storage.get(key)
            obj.delete()
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # Remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for obj in storage.all(args).values():
                print_list.append(str(obj))
        else:
            for class_name in HBNBCommand.classes:
                for obj in storage.all(class_name).values():
                    print_list.append(str(obj))

        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all objects of a class")
        print("[Usage]: all [className]\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all(args).items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Help information for the count command"""
        print("Counts the number of class instances")
        print("[Usage]: count <className>\n")

    def do_update(self, args):
        """Updates a certain object with new info"""
        c_name = c_id = att_name = att_val = kwargs = ''

        # Isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # Class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # Class name invalid
            print("** class doesn't exist **")
            return

        # Isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # Id not present
            print("** instance id missing **")
            return

        # Generate key from class and id
        key = c_name + "." + c_id

        # Determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # First determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # Reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # Isolate args
            args = args[2]
            if args and args[0] == '\"':  # Check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # If att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # Check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # If att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # Retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # Iterate through attr names and values
        for i, att_name in enumerate(args):
            # Block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # Following item is value
                if not att_name:  # Check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # Check for att_value
                    print("** value missing **")
                    return
                # Type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # Update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # Save updates to file
        storage.save()   # Save changes to storage

    def help_update(self):
        """Help information for the update method"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
