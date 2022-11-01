#!/usr/bin/python3
"""A program that contains the entry point of the command interpreter"""

import cmd
import re
import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review
from shlex import split

# A global list that specifies the menu of the command interpreter
CLASSES=[
    "BaseModel",
    "User",
    "City",
    "Place",
    "State",
    "Amenity",
    "Review"
    ]

def parse(arg):
    """ A function that parses the command

        PARAMETERS
            arg: string containing commands
    """

    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


def is_missing(args):
    """ A function that checks if the class name is missing or doesn't
        exist
    
		PARAMETERS
            args: string containing commands
    """

    arg_list = parse(args)

    if len(arg_list) == 0:
        print("** class name missing **")
    elif arg_list[0] not in CLASSES:
        print("** class doesn't exist **")
    else:
        return arg_list


class HBNBCommand(cmd.Cmd):
    """A class that defines the command interpreter"""
    
    prompt = "(hbnb)"
    storage = models.storage

    def emptyline(self):
        """ A function that defines a command to be executed
            when an empty line + <ENTER> key is pressed
        """
        pass

    def default(self, arg):
        """ A function that defines the default behaviour for
            the cmd module when an input is invalid
        
            PARAMETERS
                self: the constructor variable
                arg: string containing commands
        """
        
        action_m0ap = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }

        match = re.search(r"\.", arg)
        if match:
            arg1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg1[1])
            if match:
                command = [arg1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in action_map:
                    call = "{} {}".format(arg1[0], command[1])
                    return action_map[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_EOF(self, argv):
        """ A function that executes the EOF menu command to 
            exit the program
                    
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """

        print("")
        return True

    def do_quit(self, argv):
        """ A function that executes the Quit menu command to exit
            the program
                    
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """
        
        return True

    def do_create(self, argv):
        """ A function that executes the Create menu command to create
            a new instance of the BaseModel class, save it (to a 
            JSON file) and print the id
                    
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """

        args = is_missing(argv)
        if args:
            print(eval(args[0])().id)
            self.storage.save()

    def do_show(self, argv):
        """ A function that executes the Show menu command and prints the
            string representation of an instance based on the class name
            and id
                            
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """

        args = is_missing(argv)
        if args:
            if len(args) != 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in self.storage.all():
                    print("** no instance found **")
                else:
                    print(self.storage.all()[key])

    def do_all(self, argv):
        """ A function that executes the All menu command and prints all 
            string representation of all instances based on or not on the 
            class name
                            
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """
        
        arg_list = split(argv)
        objects = self.storage.all().values()
        if not arg_list:
            print([str(obj) for obj in objects])
        else:
            if arg_list[0] not in CLASSES:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objects
                       if arg_list[0] in str(obj)])

    def do_destroy(self, argv):
        """ A function that execuites the Destroy menu command and deletes
            a class instance based on the name and given id and saves the 
            changes to the JSON file
                            
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """
        
        arg_list = is_missing(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")

    def do_update(self, argv):
        """ A function that executes the Update menu command and updates 
            an instance based on the class name and id by adding or updating 
            attribute and saves the changes the JSON file
                            
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """
        
        arg_list = is_missing(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                instance_id = "{}.{}".format(arg_list[0], arg_list[1])
                if instance_id in self.storage.all():
                    if len(arg_list) == 2:
                        print("** attribute name missing **")
                    elif len(arg_list) == 3:
                        print("** value missing **")
                    else:
                        obj = self.storage.all()[instance_id]
                        if arg_list[2] in type(obj).__dict__:
                            v_type = type(obj.__class__.__dict__[arg_list[2]])
                            setattr(obj, arg_list[2], v_type(arg_list[3]))
                        else:
                            setattr(obj, arg_list[2], arg_list[3])
                else:
                    print("** no instance found **")

            self.storage.save()

    def do_count(self, arg):
        """ A function that executes the Count menu command and retrieve the 
            number of instances of a class
                            
            PARAMETERS
                self: the constructor variable
                argv: string containing commands
        """
        
        arg1 = parse(arg)
        count = 0
        for obj in models.storage.all().values():
            if arg1[0] == type(obj).__name__:
                count += 1
        print(count)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
