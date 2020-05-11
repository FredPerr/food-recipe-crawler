"""

Log system:

    variables:
        last_raw_output: the last output value not serialized.

    methods / functions:

        set_output_level(level: int) -> Set the level of the outputs.
            If the level of an output is inferior of the actual level,
            it will not be logged but will be set as the new last_raw_output

        out(object: *, prefix: str = '', level: int) -> Outputs an object
            that will be serialized, set the last_raw_output variable
            and add the tag to the output.

        info(object: *) -> out(object, '[INFO] ', 1)
        warn(object: *) -> out(object, '[WARN]', 2)
        error(object: *, code: Union[str, int, None] = None) -> out(object, '[ERROR{code}]', 3)

Console system:


"""
from typing import Tuple, List, Union
import os
import platform

from data import data_saver


class Console:

    def __init__(self, commands: List[Tuple[str, str, str]]):
        self.commands = commands
        self.last_raw_output = None
        self.log_level = 3

    def input(self) -> str:
        user_input = input('> ')
        if len(user_input) == 0:
            return user_input

        cmd_attributes = user_input.split(' ')

        cmd_args = []
        attributes_length = len(cmd_attributes)
        if attributes_length > 1:
            cmd_args = cmd_attributes[1:]

        cmd_name = cmd_attributes[0]
        # Command pattern key-value arguments: <cmd> -args=something -args2=something2
        # Command pattern positional arguments: <cmd> something something2

        # Testing whether or not the actual pattern is position or key-value.
        key_value_pattern = True
        for arg in cmd_args:
            if not len(arg) > 0 or '=' not in arg or not arg[0] == '-':
                key_value_pattern = False
                break

        try:
            call = globals().get('cmd_' + cmd_name)
            if call is None or not callable(call):
                raise AttributeError
        except AttributeError:
            self.warn(f"The command with the name {cmd_name} was not found.\n"
                      f"Type 'help' to see the list of the available commands.")
            return user_input
        if not key_value_pattern:
            call(*cmd_args)
        else:
            kwargs = {}
            for i in range(len(cmd_args)):
                key_value = cmd_args[i].split('=', 1)
                kwargs.update({key_value[0][1:]: key_value[1]})
            call(**kwargs)

        return user_input

    def get_command(self, command: str) -> tuple:
        """Get a command that have been registered.

        :param command: The command name to search for.
        :return: The command attributes tuple.
        """
        cmd_attributes = command.split(' ', 1)

        # Nothing was entered
        if len(cmd_attributes) == 0:
            return self.commands[0]

        cmd_name = cmd_attributes[0]

        for cmd in self.commands:
            if cmd[0] == cmd_name:
                return cmd
        return self.commands[0]

    def output(self, obj, prefix: str = '', level: int = 0):
        """Prints a value in the console.

        The last raw input is set to the given object. The given object
        to output is formatted if it is not a string. Then, it prints the
        tag followed by the object serialized value.
        :param level:   The level of the output importance. The more the output is
                        high, the less it is important.
        :param obj:     The object to send to the console.
        :param prefix:  The prefix of the message. This can be expressed as a 'tag'.
        """
        self.last_raw_output = obj
        serialized = obj

        if level > self.log_level:
            return

        if not isinstance(obj, str):
            serialized = data_saver.serialize(obj)
        print(prefix + serialized)

    def info(self, obj):
        self.output(obj, '[INFO] ', 3)

    def warn(self, obj):
        self.output(obj, '[WARN] ', 2)

    def error(self, obj, code: Union[str, int, None] = None):
        if isinstance(code, int):
            code = str(code)
        self.output(obj, f'[ERROR{"" if code is None else " NO." + code}] ', 1)

    def set_log_level(self, level: int):
        """Set the current level of the logger.

        Printing a message with a level superior to the level
        of console's level, the message will not be printed.
        :param level: The level to give to the console.
        """
        self.log_level = level


# Command pattern -> name, description, usage.
COMMANDS = [
    ('', '', ''),
    ('help', 'Send a help message', 'help (command) (show_usage)'),
    ('quit', 'Quit the program', 'quit'),
    ('clear', 'Clear the content of the console.', 'clear'),
    ('load', 'Load the content of a file in memory.', 'load -path --replace')
]

CONSOLE = None
PLATFORM = 'Windows'


def cmd_help(cmd: str = '', show_usage: str = ''):

    command = console.get_command(cmd)
    if cmd != '' and command[0] == '':
        console.output(f"There is no registered command has '{cmd}'")
        return

    if cmd == '':
        console.output('Here is the list of all the commands:\n')
        for i in range(1, len(COMMANDS)):
            console.output((COMMANDS[i][2] if show_usage == 'true' else COMMANDS[i][0]) + ': ' + COMMANDS[i][1])
    else:
        console.output(f"Here is the usage of the command '{cmd}':\n    " +
                       command[2])


def cmd_quit():
    console.output('Quitting the program...')
    quit(0)


def cmd_clear():
    if PLATFORM == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':

    if 'Windows' not in platform.system():
        PLATFORM = 'Linux/OSX'

    console = Console(COMMANDS)
    while True:
        console.input()
