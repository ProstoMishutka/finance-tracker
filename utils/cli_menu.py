from app.logs import logger
from .errors import EmptyInputError, InvalidInputError


def handle_menu_choice(option: str, pattern: list[str]) -> bool:
    if option is None or option.strip() == "":
        logger.warning("User entered an empty string when selecting a menu option")
        raise EmptyInputError("Input cannot be empty. Please choose a menu option.")

    if option.strip() not in pattern:
        logger.warning(f'User entered an invalid menu option - "{option}".')
        raise InvalidInputError("Invalid menu option. Please choose a menu option.")

    return True
