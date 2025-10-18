from app.logs import logger
from .errors import EmptyInputError, InvalidInputError


def handle_menu_choice(option: str, pattern: list[str]) -> bool:
    """
    Validates a user's menu selection against a given pattern of valid options.

    The function checks whether the user's input is empty or not included in the allowed menu options.
    If the input is empty or invalid, it raises an appropriate exception. Otherwise, it returns True.

    :param option: str
        The menu option entered by the user as a string.
    :param pattern: list[str]
        A list of valid menu option strings.
    :raises EmptyInputError: if the user's input is empty.
    :raises InvalidInputError: if the user's input is not included in the pattern of valid options.
    :return: bool
        Returns True if the user's input is valid.
    """
    if option is None or option.strip() == "":
        logger.warning("User entered an empty string when selecting a menu option")
        raise EmptyInputError("Input cannot be empty. Please choose a menu option.")

    if option.strip() not in pattern:
        logger.warning(f'User entered an invalid menu option - "{option}".')
        raise InvalidInputError("Invalid menu option. Please choose a menu option.")

    return True
