from enum import Enum
from typing import List, Tuple
import os
import platform


class LogLevel(Enum):
    """The level importance of a message when the snake logs it.

    The more the level is high, the less it is
    important. The level should not go under zero.
    """
    NORMAL = 4
    INFO = 3
    WARNING = 2
    ERROR = 1
    FATAL = 0


class Snake:
    """This is the snake class.

    A snake learns actions and performs it when
    telling him to via the #tell method.
    """

    def __init__(self):
        self._clear_cmd = 'cls' if 'Windows' in platform.platform() else 'clear'

        self._actions = List[Tuple[str, callable]]

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

    def learn(self, action_name: str, action: callable):
        """Make the snake learn a new action.

        :param action_name: The name of the new action.
        :param action:      The function to execute when
                            the snake must perform the action.
        """

        # The snake already knows this action.
        if self.has_learnt(action_name):
            return

        # The action is not a callable type or a function
        if not isinstance(action, callable):
            return

        self._actions.append((action_name, action))

    def tell(self, output, level: LogLevel = LogLevel.NORMAL):
        """Log a message into the console with a given log level.

        :param output:   The data to output as a text message.
        :param level:    The level of the output importance.
                         see #LogLevel class for more information.
        """
        pass

    def clean(self):
        """Clean all the outputs of the snake and inputs.

        Clears the console's so that there are no more text on screen.
        """
        os.system(self._clear_cmd)

    def ask(self, question: str = '') -> str:
        """Make the snake ask a question to the user.

        :param question: The question the snake will ask the user.
        :return          A string representing the input given to the snake.
        """
        pass

    def has_learnt(self, action_name) -> bool:
        """Check if the snake has learnt an action.

        :param action_name: The name of the action that the
                            snake would have learned or not.
        :return:            A Boolean value of true if the
                            snake has learnt the given action name.
        """
        for action in self._actions:
            if isinstance(action, tuple):
                if isinstance(action[0], str):
                    if action_name == action[0]:
                        return True
        return False
