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

from data import data_saver


class Console:

    def __init__(self, commands: List[Tuple[str, str, str]]):
        self.commands = commands
        self.last_raw_output = None
        self.log_level = 3

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
    ('help', 'Send a help message', 'help'),
    ('quit', 'Quit the program', 'quit'),
    ('load', 'Load the content of a file in memory.', '')
]

if __name__ == '__main__':
    c = Console(COMMANDS)
