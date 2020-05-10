from typing import Union


def out(message: str, tag: str = '') -> str:
    """Prints a message to the console.

    :param tag:     The tag of the message
    :param message: The message to print.
    :return: The message that has been printed.
    """
    output = f'{tag} {message}'
    print(output)
    return output


def info(message: str = '') -> str:
    """Log an information message via the print function.

    :param message: The message to output.
    :return The value that has been printed.
    """
    return out(message, '[INFO]')


def warn(message: str = '') -> str:
    """Log a warning message via the print function.

    :param message: The message to output.
    :return The value that has been printed.
    """
    return out(message, '[WARN]')


def error(message: str = '', code: Union[str, int, None] = ''):
    """Log an information message via the print function.

    :param message: The message to output.
    :param code:    The code of the error. This can be an string, an integer or None.
    :return The value that has been printed.
    """
    if code is None:
        code = ''

    if isinstance(code, int):
        code = f' {str(code)}'

    return out(message, f'[ERROR{code}]')
