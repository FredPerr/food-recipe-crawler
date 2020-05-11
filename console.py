"""

Log system:

    variables:
        clipboard: the last output value not serialized.

    methods / functions:

        set_output_level(level: int) -> Set the level of the outputs.
            If the level of an output is inferior of the actual level,
            it will not be logged but will be set as the new clipboard

        out(object: *, prefix: str = '', level: int) -> Outputs an object
            that will be serialized, set the clipboard variable
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
from data import web_crawler


class Console:

    def __init__(self, commands: List[Tuple[str, str, str, str]]):
        self.commands = commands
        self.clipboard = None
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
        try:
            if not key_value_pattern:
                call(*cmd_args)
            else:
                kwargs = {}
                for i in range(len(cmd_args)):
                    key_value = cmd_args[i].split('=', 1)
                    kwargs.update({key_value[0][1:]: key_value[1]})

                call(**kwargs)
        except TypeError:
            console.error('Please use the command parameters: \n     ' + self.get_command(cmd_name)[2])
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

    def output(self, obj, prefix: str = '', level: int = 0, copyInClipboard: bool = False):
        """Prints a value in the console.

        The last raw input is set to the given object. The given object
        to output is formatted if it is not a string. Then, it prints the
        tag followed by the object serialized value.
        :param copyInClipboard: A boolean value of true to copy the content in the clipboard.
        :param level:   The level of the output importance. The more the output is
                        high, the less it is important.
        :param obj:     The object to send to the console.
        :param prefix:  The prefix of the message. This can be expressed as a 'tag'.
        """
        if copyInClipboard:
            self.clipboard = obj
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

    def add_command(self, attributes: Tuple[str, str, str]) -> bool:
        """Add a command to the registered commands.

        :param attributes: The attributes of the command (name, description, usage).
        :return: A boolean value of true if the command was successfully added.
        """
        if self.get_command(attributes[0]) == '':
            return False
        else:
            self.commands.append(attributes)
            return True

    def remove_command(self, name: str) -> bool:
        """Remove a command from the registered commands.

        :param name: The name of the command.
        :return: A boolean value of true if the command was removed.
                 False is returned otherwise.
        """
        command = self.get_command(name)
        try:
            self.commands.remove(command)
            return True
        except ValueError:
            return False


# Command pattern -> name, description, usage.
COMMANDS = [
    ('', '', ''),
    ('help', 'Send a help message.', 'help (command) (show_usage)', ''),
    ('quit', 'Quit the program.', 'quit', ''),
    ('clear', 'Clear the content of the console.', 'clear', ''),
    ('clipboard', 'See or clear the actual clipboard value.', 'clipboard (clear)', ''),
    ('load', 'Load the content of a file in memory.', 'load <path>', ''),
    ('export', 'Export the content of the clipboard in a file.', 'export <path>', ''),
    ('replace', 'Replace content in a file.', 'replace <path> <str_from> <str_to>', ''),
    ('sitemap', 'Find the sitemap(s) of one or many websites.', 'sitemap <exportFile> <urls>', '@urls '
                                                                'may be a file with a link '
                                                                'on every line or \n'
                                                                'urls separated by | character '
                                                                'with inline command.')
]

CONSOLE = None
PLATFORM = 'Windows'


def cmd_help(cmd: str = '', show_usage: str = ''):
    command = console.get_command(cmd)
    if cmd != '' and command[0] == '':
        console.output(f"There is no registered command named '{cmd}'")
        return

    if cmd == '':
        console.output('Here is the list of all the commands:\n')
        for i in range(1, len(COMMANDS)):
            console.output((COMMANDS[i][2] if show_usage == 'true' else COMMANDS[i][0].ljust(12)) + ': ' + COMMANDS[i][1])
    else:
        console.output(f"Here is the usage of the command '{cmd}':\n    " + command[2])
        if command[3] != '':
            console.output(command[3])


def cmd_quit():
    console.output('Quitting the program...')
    quit(0)


def cmd_clear():
    if PLATFORM == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def cmd_load(path: str, arrayType: str = 'false'):
    content = data_saver.retrieveFileContent(path, True if arrayType == 'true' else False)

    if content is None:
        console.error(f'Could not load the following file: {path}')
        return

    console.clipboard = content
    size = len(content)
    console.info(f'The content of the file has been copied in the clipboard. ({size} characters)')


def cmd_export(path: str, append: str = 'true', lineSep: str = '\n'):
    if console.clipboard is None:
        console.error('Could not export the content of the clipboard because it is empty.')
        return
    data_saver.writeInFile(path, console.clipboard, True if append == 'true' else False, lineSep)
    console.info(f'Pasted the content of the clipboard into the following file: {path}')


def cmd_clipboard(option: str = ''):
    if option == 'clear':
        console.info('The clipboard has been cleared')
        console.clipboard = None
    else:
        console.output(console.clipboard)


def cmd_replace(path: str, str_from: str, str_to: str):
    content = data_saver.retrieveFileContent(path)

    if content is None:
        console.error(f'Could not load the content of the following file: {path}')
        return False

    data_saver.writeInFile(path, content.replace(str_from, str_to), False)
    console.info(f'The replacements have been made in the following file: {path}')


LAST_SITEMAP = False

def cmd_sitemap(exportFile: str, urls: str):

    if urls.startswith('http'):
        urls = urls.split('|')
    else:
        urls = data_saver.retrieveFileContent(urls, True)
        if urls is None:
            console.error(f'Could not load the content of the following file: {urls}')
            return False

    if urls is None or len(urls) == 0:
        console.error(f'Could not load the urls in {urls}')
        return

    data = []
    for url in urls:
        sm = web_crawler.find_sitemaps_url(url)
        if sm is not None:
            data.append(sm)

    console.clipboard = data
    console.info('Copied the sitemap list to the clipboard.')
    data_saver.writeInFile(exportFile, data, False)
    console.info(f'Sitemap list exported into the file {exportFile}')


#sitemap ./test.txt ./urls.txt

if __name__ == '__main__':

    if 'Windows' not in platform.system():
        PLATFORM = 'Linux/OSX'

    console = Console(COMMANDS)
    while True:
        console.input()
