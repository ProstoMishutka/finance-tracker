class FinanceTrackerError(Exception):
    """
    Base exception class for the Finance Tracker application.

    Serves as the parent class for all specialized errors
    that may occur while working with financial transactions.

    Attributes:
        message (str): The error message.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyInputError(FinanceTrackerError):
    """
    Exception raised when a required input from the user is empty.

    Inherits from FinanceTrackerError.
    """


class InvalidInputError(FinanceTrackerError):
    """
    Exception raised when the user provides input that is invalid
    or does not meet the expected format or criteria.

    Inherits from FinanceTrackerError.
    """


class TransactionNotFoundError(FinanceTrackerError):
    """
    Exception raised when a requested transaction cannot be found
    in the system or within the specified criteria (e.g., date range, category).

    Inherits from FinanceTrackerError.
    """


class CategoryNotFoundError(FinanceTrackerError):
    """
    Exception raised when no transactions are found for a specified category.

    Inherits from FinanceTrackerError.
    """


class DateNotFoundError(FinanceTrackerError):
    """
    Exception raised when no transactions are found for a specified date
    or when the date input is empty or invalid.

    Inherits from FinanceTrackerError.
    """