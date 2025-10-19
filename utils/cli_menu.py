from typing import TYPE_CHECKING, Callable

from app.logs import logger
from .errors import (
    EmptyInputError,
    InvalidInputError,
    CategoryNotFoundError,
    TransactionNotFoundError,
)

if TYPE_CHECKING:
    from app import TransactionDictManager


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


def execute_menu_option(
    manager: "TransactionDictManager",
    callback: Callable,
    selected_option: str | None = None,
) -> None:
    """
    Executes a menu action that involves selecting a date range.

    The function prompts the user to input a start and end date, validates them,
    and then calls the provided callback function with the filtered transaction dates.
    If the `option` argument is provided, it will be passed as the first parameter
    to the callback, followed by the list of transaction dates. Otherwise, only
    the transaction dates are passed.

    :param manager: TransactionDictManager
        An instance of TransactionDictManager used to retrieve and filter transactions.
    :param callback: Callable
        The function to execute with the filtered transaction dates (and optionally an option).
    :param selected_option: str | None, optional
        An optional argument to pass to the callback function as the first parameter.
    :raises InvalidInputError:
        If the user inputs an invalid start or end date that does not match the format YYYY-MM-DD
        or if the start date is greater than the end date.
    :raises CategoryNotFoundError:
        If no transactions are found for a given category during callback execution.
    :raises TransactionNotFoundError:
        If no transactions are found within the specified date range during callback execution.
    :return: None
        The function executes the callback and does not return any value.
    """
    while True:
        start_date = input(
            "Enter the start date in YYYY-MM-DD format. "
            "If left empty, all dates up to the specified end date will be considered: "
        )
        try:
            date_range_fn = manager.get_transactions_by_date_range(start_date)
            break
        except InvalidInputError as message:
            print(f"{message}\n")

    while True:
        end_date = input(
            "Enter the end date (YYYY-MM-DD). "
            "If left empty, today's date will be used: "
        )

        try:
            transaction_dates = date_range_fn(end_date)
            if selected_option:
                callback(option, transaction_dates)
            else:
                callback(transaction_dates)

            break
        except InvalidInputError as message:
            print(f"{message}\n")
            continue
        except (CategoryNotFoundError, TransactionNotFoundError) as message:
            print(f"{message}\n")
            break
