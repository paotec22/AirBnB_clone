#!/usr/bin/python3
"""
    Console entry point for Airbnb
"""

import cmd
import sys
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '(hbnb) '

    def __checkModel__(self, arg):
        try:
            new_constructor = globals()[arg[0]]
        except KeyError:
            print("** class doesn't exist **")
            return
        if (len(arg) < 2):
            print("** instance id missing **")
            return
        data = storage.all()
        for obj_id in data.keys():
            obj = data[obj_id]
            if (obj.id == arg[1]):
                return obj
        print("** no instance found **")

    def emptyline(self):
        """ Called when the enter button is hit without an input"""
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_quit(self, arg):
        sys.exit(1)

    def do_EOF(self, arg):
        sys.exit(1)

    def do_create(self, arg):
        """ Creates a new instance of BaseModel """
        if (arg == ''):
            print("** class name missing **")
        else:
            try:
                new_constructor = globals()[arg]
                new_instance = new_constructor()
            except KeyError:
                print("** class doesn't exist **")
                return
            new_instance.save()
            print("{}".format(new_instance.id))

    def do_show(self, arg):
        args = arg.split()
        if (len(args) < 1):
            print("** class name missing **")
            return
        obj = self.__checkModel__(args)
        if (obj is not None):
            print(str(obj))

    def do_destroy(self, arg):
        args = arg.split()
        if (len(args) < 1):
            print("** class name missing **")
            return
        obj = self.__checkModel__(args)
        if (obj is not None):
            data = storage.all()
            del_key = ''
            for key, value in data.items():
                if (value.id == args[1]):
                    del_key = key
            del data[del_key]
            return

    def do_all(self, arg):
        if (arg == ''):
            arg = 'BaseModel'
        try:
            new_constructor = globals()[arg]
        except KeyError:
            print("** class doesn't exist **")
            return
        data = storage.all()
        data_str = []
        for obj_id in data.keys():
            obj = data[obj_id]
            data_str.append(str(obj))
        print(data_str)
        return

    def do_update(self, arg):
        args = arg.split()
        if (len(args) < 1):
            print("** class name missing **")
            return
        obj = self.__checkModel__(args)
        if (obj is None):
            return
        if (len(args) < 3):
            print("** attribute name missing **")
            return
        if (len(args) < 4):
            print("** value missing **")
            return
        data = storage.all()
        for key, value in data.items():
            if (value.id == obj.id):
                dict_value = value.to_dict()
                print(dict_value)
                print(args[3])
                dict_value[args[2]] = type([args[3]])(args[3])
                print(dict_value)
                #del data[key]
                #print(type(data))
                #print(type(value)(dict_value))
                return

    def help_quit(self):
        print('Quit command to exit the program')

    def help_EOF(self):
        print('EOF exits the program')


if __name__ == '__main__':
    HBNBCommand().cmdloop()