from enum import Enum
from typing import Tuple, Optional, Union, Dict
import os
import platform


class LogLevel(Enum):
    """The level importance of a message when the snake logs it.

    The more the level is high, the less it is
    important. The level should not go under zero.
    """
    NORMAL = 4, ''
    INFO = 3, '[INFO] '
    WARNING = 2, '[WARN] '
    ERROR = 1, '[ERROR] '
    FATAL = 0, '[FATAL] '
    INPUT = 0, '[INPUT] '


class Snake:
    """This is the snake class.

    A snake learns actions and performs it when
    telling him to via the #tell method.
    """

    def __init__(self):
        self._clear_cmd = 'cls' if 'Windows' in platform.platform() else 'clear'

        # The list of the actions. Each actions has attributes:
        # (name, function, description, usage, specification)
        self._actions = []

        # The level of logging accepted by the snake.
        # Everything lower than that would be ignore.
        self.log_level = LogLevel.NORMAL

        # What does the snake currently has in his mind ?
        # This represents the last data that was asked by the snake.
        self.mind = None

    """

    All the inherited action of the snake are under here:

    """

    def forget(self):
        """Make the snake forget what it has on its mind."""
        self.mind = None

    def remember(self, information):
        """Make the snake remember the given information.

        :param information: The information to set in the mind of the snake.
                            Only one information can reside in its mind.
        """
        self.mind = information

    def learn(self, action_name: str, action: callable, description: str,
              usage: str, specification: str = ''):
        """Make the snake learn a new action.

        :param specification: The specification for the usage of the action or
                              what it does.
        :param usage:         How to use the action.
        :param description:   The short description of the action.
        :param action_name:   The name of the new action.
        :param action:        The function to execute when
                              the snake must perform the action.
        """

        # The snake already knows this action.
        if self._has_learnt(action_name):
            return

        # The action internal types are valid.
        if not callable(action) \
                or not isinstance(description, str) \
                or not isinstance(usage, str) \
                or not isinstance(specification, str):
            return

        self._actions.append((action_name, action, description, usage, specification))

    def perform(self, action_command: str):
        """Make the snake perform an action.

        :param action_command: The command to perform.
        """

        command = self.old_split_action_command(action_command)

        if command is None:
            self.tell('Could not perform the action due to an error in the command syntax.',
                      LogLevel.ERROR)
            return

        action = self._get_action(command[0])

        # Make sure the action exists.
        if action is None:
            return

        try:
            if len(command[1]) == 0:
                action[1]()
            else:
                if isinstance(command[1], tuple):

                    print(command[1])
                    action[1](*command[1])
                else:
                    action[1](**command[1])
        except TypeError:
            self.tell("Could not perform the action '" + command[0] + "'",
                      LogLevel.ERROR, error=None)

    def help(self, action: Optional[Union[None, str]] = None):
        """Send a help message about all the possible actions or a specific action.

        :param action: The action to get the help with or None
                            to get help on every possible actions.
        """
        if action is not None:
            action = self._get_action(action)
            tag_len = 16
            self.tell(f"About the '{action[0]}' action:")
            self.tell('Description: '.ljust(tag_len) + action[2])
            self.tell('Usage: '.ljust(tag_len) + action[3])
            self.tell('Specifications: '.ljust(tag_len) + action[4])

        else:
            if len(self._actions) == 0:
                self.tell('The snake has learnt no action yet !')
            else:
                self.tell("About the available actions:\n")
                for action in self._actions:
                    self.tell(action[0] + ': ' + action[2])
                self.tell("\nType 'help <action>' to get help on a specific action.")
                self.tell('You can always perform a command using a command as follow: \n'
                          'action <arg_name=value> <arg_name2=value2>\n'
                          '        or\n'
                          'action <arg1> <arg2> <...>')

    def tell(self, output, level: LogLevel = LogLevel.NORMAL,
             error: Union[str, int, None] = None):
        """Log a message into the console with a given log level.

        :param error:    The error code or message to add to the error if it
                         one. Set None value to ignore this.
        :param output:   The data to output as a text message.
        :param level:    The level of the output importance.
                         see #LogLevel class for more information.
        """
        # Check if the log level is sufficient.
        if level.value[0] > self.log_level.value[0]:
            return

        # Formatting the message so that it is a string.
        if isinstance(output, list) or isinstance(output, tuple):
            output = ''.join(output)
        elif isinstance(output, int):
            output = str(output)
        elif isinstance(output, bool):
            output = str(output)

        tag = level.value[1]

        if level.value[0] == LogLevel.ERROR.value[0] or level.value[0] == LogLevel.FATAL.value[0]:

            if error is None:
                error = ''
            elif isinstance(error, int):
                error = ''

            tag.format(error)

        print(tag + output)

    def ask(self, question: str = '') -> str:
        """Make the snake ask a question to the user.

        :param question: The question the snake will ask the user.
        :return          A string representing the input given to the snake.
        """
        self.tell(question, LogLevel.INPUT)
        return input('> ')

    def old_split_action_command(self, command: str) \
            -> Union[Tuple[str, Union[Dict[str, str], Tuple[str]]], None]:

        if len(command.replace(' ', '')) == 0:
            return None

        parts = command.split(' ', 1)
        action_name = parts[0]

        if len(parts) == 1:
            return action_name, tuple()

        valid_args = {}

        args = parts[1].split(' ')

        # Positional arguments.
        if '=' not in args[0]:
            for i in range(len(args)):
                args[i] = args[i].strip()
            return action_name, tuple(args)
        # Key-value arguments.
        else:
            def wrong(arg):
                self.tell(f"Could not load the argument '{arg}'. Make sure it "
                          f"uses this pattern: 'key=value'", LogLevel.WARNING)
            for i in range(len(args)):
                if '=' not in args[i]:
                    wrong(args[i])
                    continue

                kv_pair = args[i].split('=', 1)
                if len(kv_pair[0]) > 0 and len(kv_pair[1]) > 0:

                    # Single quote declaration.
                    if kv_pair[1].startswith("'") \
                            and kv_pair[1].endswith("'") \
                            and len(kv_pair[1]) > 1:
                        pass

                    valid_args.update({kv_pair[0]: kv_pair[1]})
                else:
                    wrong(args[i])

        return action_name, valid_args

    def _has_learnt(self, action_name: str) -> bool:
        """Check if the snake has learnt an action.

        :param action_name: The name of the action that the
                            snake would have learned or not.
        :return:            A Boolean value of true if the
                            snake has learnt the given action name.
        """
        return self._get_action(action_name) is not None

    def _get_action(self, action_name: str) -> Union[Tuple[str, callable, str, str], None]:
        """Get an action from its name.

        :param action_name: The name of the actions to get.
        :return: The action or None if the action was not found.
        """
        for action in self._actions:
            if action[0] == action_name:
                return action
        return None

    def clean(self):
        """Clean all the outputs of the snake and inputs.

        Clears the console's so that there are no more text on screen.
        """
        os.system(self._clear_cmd)


def process_command_input(command: str) \
        -> Union[Tuple[str, Union[Union[Dict[str, str], Tuple[str]]], None], None]:
    """Process an input command to parse it.

    First, it checks if the command input is valid. For that, the argument #command must not be
    None, be a string and have a length of 1 or more. The
    Secondly, it splits the command taking in account the arguments surrounded by double quotes
    ('"'). This step removes unnecessary whitespaces that are outside the double quotes and between
    the arguments and the command name.
    Thirdly, it checks if the type of the type of the argument are positional or key-value type.
    Then, it splits the key-value arguments if the type of the arguments is key-value. The split
    is done using the first equal ('=') character and the hyphen ('-') at the beginning of the key
    name.
    Finally, it creates a new tuple for the positional values or a dictionary for the key-values
    arguments.

    :param command: The command to parse. The form of the command should follow this pattern:
                    '<action> <argument1> <"argument2"> <...>' or '<action> <-argument_name="value">
                    <-argument_name2="value2">'. NB that the double quotes are used to keep
                    whitespace split disable inside them. They will not affect the value. The hyphen
                    at the beginning of the key-value arguments are mandatory in order to take them
                    in account as a key-value type. Positional type will be used otherwise. Those
                    quotes must be placed at the beginning and at the end of the value.
    :return:        A tuple with the command name in the first index and the key-value ('**kwargs')
                    dictionary or the values ('*values') tuple in the second index. If the command
                    has no argument, the second index value will be None. If the command is empty or
                    equal to None, it will return None.
    """
    pass


if __name__ == '__main__':

    s = Snake()
    s.learn('help', s.help, 'Get the help of the snake on something.', 'help (action)',
            'This action can be used to get a general help on every possible actions the snake '
            'can perform or on a specific action by providing its name as the action argument.')
    s.perform('help ')

