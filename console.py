#!/usr/bin/python3
"""
This is the entry point of the command interpreter.
Authors: YASSINE - ANAS
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import re
import ast


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HolbertonBnB application.

    Manages entities via console with predefined commands.

    Attributes:
        prompt (str): Command prompt symbol.
        classes (dict): Mapping of class names to classes.
    """
    prompt = '(hbnb) '
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Exits the console. Usage: quit"""
        return True

    def do_EOF(self, arg):
        """Exits console with EOF (Ctrl+D)."""
        print("")
        return True

    def emptyline(self):
        """Does nothing on empty input."""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel. Usage: create <class name>
        Example: create User
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if '.' in args[0]:
            print("*** Unknown syntax: {} ***".format(arg))
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        instance = self.classes[args[0]]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """
        Shows an instance based on the class name and id.
        Usage: show <class name> <id>
        Example: show User 1234-1234-1234
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id>
        Example: destroy User 1234-1234-1234
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """
        Shows all instances of a class or all classes if not specified.
        Usage: all or all <class name>
        Example: all User
        """
        args = arg.split()
        instances = storage.all()
        if not args:
            print([str(v) for v in instances.values()])
        elif args[0] in self.classes:
            filtered_instances = [
                str(v) for v in instances.values()
                if type(v).__name__ == args[0]
            ]
            print(filtered_instances)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance by adding or
        updating an attribute or multiple attributes via a dictionary.
        ----------------
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        update <class name> <id> <dictionary of attributes>
        ----------------
        Example: update User 1234-1234-1234 email "contact@yassine.fun"
        update User 1234-1234-1234 '{"email": "c@yassine.fun", "name": "Yass"}'
        """
        args = arg.split(" ", 2)
        if not args or args[0] == "":
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2 or args[1] == "":
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return

        if (len(args) == 3 and args[2].startswith("{") and
                args[2].endswith("}")):
            try:
                attr_dict = ast.literal_eval(args[2])
                if not isinstance(attr_dict, dict):
                    raise ValueError("** value is not a dictionary **")
                for attr_name, attr_value in attr_dict.items():
                    self.apply_update(key, attr_name, attr_value)
            except (ValueError, SyntaxError) as e:
                print(e)
        elif len(args) == 3:
            attr_args = args[2].split(" ", 1)
            if len(attr_args) < 2:
                print("** attribute name or value missing **")
                return
            attr_name, attr_value_str = attr_args[0], attr_args[1]
            try:
                attr_value = ast.literal_eval(attr_value_str)
            except (ValueError, SyntaxError):
                attr_value = attr_value_str.strip("\"")
            self.apply_update(key, attr_name, attr_value)
        else:
            print("** Unknown error **")

    def apply_update(self, key, attr_name, attr_value):
        """Helper method to apply update to an instance."""
        obj = storage.all()[key]
        if isinstance(attr_value, str) and not attr_value.isdigit():
            attr_value = attr_value.strip("\"")
        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_count(self, arg):
        """
        Counts instances of a specific class.
        Usage: count <class name>
        Example: count User
        """
        args = arg.split()
        if len(args) != 1:
            print("** class name missing or too many args **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        count = 0
        for obj_id in storage.all():
            if obj_id.startswith(class_name + "."):
                count += 1
        print(count)

    def default(self, line):
        """Handles unrecognized commands, including update from dictionary."""
        single_update_pattern = re.compile(
            r'^(\w+)\.update\("([^"]+)", "([^"]+)", (?:\"([^"]*)\"|(\d+))\)$'
        )
        dict_update_pattern = re.compile(
            r'^(\w+)\.update\("([^"]+)", ({.*})\)$'
        )

        match_single = single_update_pattern.match(line)
        match_dict = dict_update_pattern.match(line)

        if match_single:
            groups = match_single.groups()
            cls_name, obj_id, attribute_name, attribute_value = groups[:4]
            non_string_value = groups[4]
            if non_string_value is not None:
                attribute_value = non_string_value
            if cls_name in self.classes:
                update_cmd = (
                    f'{cls_name} {obj_id} {attribute_name} "{attribute_value}"'
                )
                self.do_update(update_cmd)
        elif match_dict:
            cls_name, obj_id, dict_arg = match_dict.groups()
            update_cmd = f'{cls_name} {obj_id} {dict_arg}'
            self.do_update(update_cmd)
        else:
            if ".create()" in line:
                print(f"*** Unknown syntax: {line} ***")
                return

            try:
                cls_name, command, arguments = self.parse_line(line)
                if cls_name not in self.classes:
                    print("** class doesn't exist **")
                    return

                arguments_clean = arguments.replace('\"', '')
                args_list = arguments_clean.split(',')

                if command in ["show", "destroy"]:
                    command_func = getattr(self, f'do_{command}', None)
                    if command_func:
                        command_func(f"{cls_name} {' '.join(args_list)}")
                elif command == "count":
                    self.do_count(cls_name)
                elif command in ["all", "create", "update"]:
                    self.onecmd(f"{command} {cls_name} {' '.join(args_list)}")
                else:
                    print(f"*** Unknown syntax: {line} ***")
            except ValueError:
                print("** class doesn't exist **")

    def parse_line(self, line):
        """Parses input to retrieve class name, command, and arguments."""
        pattern = re.compile(r"^(\w+)\.(\w+)\((.*)\)$")
        match = pattern.match(line)
        if match:
            cls_name, command, arguments = match.groups()
            return cls_name, command, arguments
        else:
            raise ValueError("Invalid command syntax")

    def handle_update(self, cls_name, arguments):
        """Handles update action for dictionary updates."""
        if "{" in arguments and "}" in arguments:
            id_arg, dict_arg = arguments.split(",", 1)
            dict_arg = ast.literal_eval(dict_arg.strip())
            for key, value in dict_arg.items():
                self.do_update(
                    "{} {} {} \"{}\"".format(
                        cls_name, id_arg.strip("\""), key, value
                    )
                )
        else:
            args = arguments.split(",", 2)
            if len(args) == 3:
                id_arg, key_arg, value_arg = args
                self.do_update(
                    "{} {} {} {}".format(
                        cls_name, id_arg.strip("\""),
                        key_arg.strip(), value_arg.strip()
                    )
                )
            else:
                print("** Invalid arguments **")

    def count_instances(self, class_name):
        """Counts the number of instances for a given class name."""
        count = sum(
            1 for obj in storage.all().values()
            if obj.__class__.__name__ == class_name
        )
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
