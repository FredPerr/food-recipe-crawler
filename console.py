import os
import platform
from typing import Union

from log_system import out
from data import web_crawler as crawler
from data import data_saver


def clear():
    if 'Windows' in platform.system():
        os.system('cls')
    else:
        os.system('clear')


class Console:

    def __init__(self):
        clear()
        self.last_output = ''
        self.commands = (
            ('', self.run_help, ''),
            ('help', self.run_help, 'Run the help command'),
            ('quit', self.run_quit, 'Quit the program.'),
            ('sitemap', self.run_sitemap, 'Find the sitemap(s) of a website.'),
            ('export', self.export, 'Export content in an external file.')
        )

        self.output(f"""
            QuickRecipeAPI - Main menu

            What would you like to do ?

            """)

        self.run_help()

        user_input = ''
        while user_input != 'quit':
            user_input = input(':')
            cmd = self.get_command(user_input)
            if cmd is not None:
                args = user_input.split(" ")

                if len(args) != 0:
                    args = args[1:]

                values = {}
                for i in range(len(args)):
                    split = args[i].split('=', 1)
                    if len(split) == 2 and len(split[0]) != 0 and len(split[1]) != 0:
                        values.update({split[0]: split[1]})

                clear()
                cmd[1](**values)

        self.run_quit()

    def export(self, output: str = None, file: str = './export.txt'):

        if output is None:
            output = self.last_output

        data_saver.writeInFile(file, output, True)

    def output(self, message):
        self.last_output = message
        out(message)

    def run_quit(self, **kwargs):
        self.output('Quiting the program !')
        quit(0)

    def run_help(self, **kwargs):
        self.output('Available commands:\n')

        for i in range(1, len(self.commands)):
            self.output(self.commands[i][0] + ': ' + self.commands[i][2])

        print()

    def run_sitemap(self, **kwargs):
        if 'url' not in kwargs.keys():
            self.output('You must specify the url of the website')
            return

        self.output(crawler.find_sitemaps_url(kwargs.get('url')))

    def get_command(self, cmd_name: str) -> Union[tuple, None]:
        """Get a command's attributes.

        :param cmd_name: The command to search for.
        :return:         A tuple if the command was
                         found or None if it has not
                         been found.
        """
        for j in range(len(self.commands)):
            if cmd_name.split(' ', 1)[0] in self.commands[j]:
                return self.commands[j]
        return None


if __name__ == '__main__':
    c = Console()
