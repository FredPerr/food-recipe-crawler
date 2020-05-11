from typing import Union
import json


def arrayToString(var: Union[list, tuple], separator: str = '') -> str:
    """ Convert an array (list or tuple) to a string value (str).

    :param var: The list or tuple to convert.
    :param separator: The separator to put between each item in the array.
    :return: A string representing the converted array with the separator between each item.
    """
    converted = ''
    for x in var:
        converted += str(x) + separator
    return converted


def writeInFile(file: str, data: Union[str, list, tuple], append: bool, array_separator: str = '\n'):
    """ Export content into a new or existing file.

    When exporting the content, if the data is in list or tuple format, the
    #arrayToString function will be called with the data in parameter. The
    separator will be by default the next line character '\n'
    :param file:            The file to write or append in.
    :param data:            The data representing as a string or an array.
    :param append:          Whether or not the file should be appended.
                            If false, the file's content will be cleared.
    :param array_separator: The separator used between each item if the data
                            is in array format.
    """
    if type(data) != str:
        data = arrayToString(data, array_separator)

    with open(file, 'a' if append else 'w') as file:
        file.write(data)
        file.close()


def retrieveFileContent(file: str, array_return: bool = False) -> Union[None, str, list]:
    """ Loads every line of a given file as a string or a list

    :param file:         The path of the file to load.
    :param array_return: Whether or not the content should be returned as
                         an array of all the line in the file.
    :return:             The string representation of the file or its representation
                         as an array of all the lines if the array_return parameter
                         is true. Null is return if the file could not be loaded.
    """
    try:
        with open(file, 'r') as f:
            fileContent = f.read()
            f.close()
        return fileContent if not array_return else fileContent.split('\n')
    except OSError as err:
        print(f'Could not load the following file: {file}')
        return None


def serialize(value) -> str:
    """ Serialize data into a string.

    :param value: The object to serialize.
    :return: The string representation of the object.
    """
    return json.dumps(value.__dict__)


def deserialize(value: str, object_type: type):
    """ Deserialize the a JSON string.

    :param value: The JSON string value.
    :param object_type: The type of the object that has been deserialize.
    :return: The new object of the given type.
    """
    return object_type(**json.loads(value))
