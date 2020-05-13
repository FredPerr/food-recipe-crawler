from enum import Enum
from typing import List, Tuple, Optional, Union
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
    ERROR = 1, '[ERROR{code}] '
    FATAL = 0, '[FATAL{code}] '
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
        if self.has_learnt(action_name):
            return

        # The action internal types are valid.
        if not callable(action) \
                or not isinstance(description, str) \
                or not isinstance(usage, str) \
                or not isinstance(specification, str):
            return

        self._actions.append((action_name, action, description, usage, specification))

    def perform(self, action_name: str, **kwargs):
        """Make the snake perform an action.

        :param action_name: The name of the action to perform.
        :param kwargs:      The key-value arguments of the action.
        """
        action = self.get_action(action_name)

        # Make sure the action exists.
        if action is None:
            return

        try:
            if len(kwargs) == 0:
                action[1]()
            else:
                action[1](kwargs)
        except TypeError as err:
            self.tell('Could not perform the action ' + action_name, LogLevel.ERROR)
            print(err)

    def help(self, action_name=Optional[None]):
        pass

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

        if level == LogLevel.ERROR or level == LogLevel.FATAL:

            if error is None:
                error = ''
            elif isinstance(error, int):
                error = ''

            tag.format(code=error)

        print(tag + output)

    def ask(self, question: str = '') -> str:
        """Make the snake ask a question to the user.

        :param question: The question the snake will ask the user.
        :return          A string representing the input given to the snake.
        """
        self.tell(question, LogLevel.INPUT)
        return input('> ')

    def has_learnt(self, action_name: str) -> bool:
        """Check if the snake has learnt an action.

        :param action_name: The name of the action that the
                            snake would have learned or not.
        :return:            A Boolean value of true if the
                            snake has learnt the given action name.
        """
        return self.get_action(action_name) is not None

    def get_action(self, action_name: str) -> Union[Tuple[str, callable, str, str], None]:
        """Get an action from its name.

        :param action_name: The name of the actions to get.
        :return: The action or None if the action was not found.
        """
        try:
            for action in self._actions:
                if action[0] == action_name:
                    return action
            return None
        except TypeError as err:
            print(err)

    def clean(self):
        """Clean all the outputs of the snake and inputs.

        Clears the console's so that there are no more text on screen.
        """
        os.system(self._clear_cmd)


def hello():
    print('Hello World')


if __name__ == '__main__':
    s = Snake()
    s.learn('hello', hello, 'Say hello', 'hello', 'Specification')
    s.perform('hello')
