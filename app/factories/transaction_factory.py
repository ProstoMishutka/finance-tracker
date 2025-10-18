from app.logs import logger
from utils import EmptyInputError, InvalidInputError
from datetime import datetime


class TransactionFactory:
    """
    A class used to create transaction objects for a Finance Tracker application.

    Each transaction object has the following encapsulated attributes, accessible via getters
    and modifiable via setters:

        - t_type (str): Type of the transaction ("income" or "expense").
        - category (str): Category of the transaction (e.g., salary, groceries).
        - amount (float): Amount of income or expense.
        - date (str): Transaction date in "YYYY-MM-DD" format. Defaults to today's date if empty.
        - description (str): Optional description of the transaction.

    Setters perform validation and raise exceptions if invalid data is provided.
    """

    def __init__(self) -> None:
        """
        Initializes a new TransactionFactory object with all attributes set to None.

        :return: None
        """
        self._t_type = None
        self._category = None
        self._amount = None
        self._date = None
        self._description = None

    @property
    def t_type(self) -> str:
        """
        Gets the transaction type.

        :return: str, either "income" or "expense"
        """
        return self._t_type

    @t_type.setter
    def t_type(self, transaction_type: str) -> None:
        """
        Sets the transaction type after validation.

        :param transaction_type: str, must be "income" or "expense"
        :raises EmptyInputError: if transaction_type is empty
        :raises InvalidInputError: if transaction_type is invalid
        :return: None
        """
        if transaction_type is None or transaction_type.strip() == "":
            logger.warning("Transaction type is empty.")
            raise EmptyInputError("Transaction type cannot be empty.")
        if transaction_type not in ["income", "expense"]:
            logger.warning(f"Transaction type is invalid - {transaction_type}.")
            raise InvalidInputError(
                f"Transaction type is invalid - {transaction_type}."
            )
        self._t_type = transaction_type
        logger.info(f'Transaction type is set to - "{self._t_type}".')

    @property
    def category(self) -> str:
        """
        Gets the transaction category.

        :return: str
        """
        return self._category

    @category.setter
    def category(self, category: str) -> None:
        """
        Sets the transaction category after validation.

        :param category: str, non-empty category name
        :raises EmptyInputError: if category is empty
        :return: None
        """
        if category is None or category.strip() == "":
            logger.warning("Category is empty.")
            raise EmptyInputError("Category cannot be empty.")
        self._category = category
        logger.info(f'Category is set to - "{category}".')

    @property
    def amount(self) -> float:
        """
        Gets the transaction amount.

        :return: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount: str) -> None:
        """
        Sets the transaction amount after validation.

        :param amount: str or float, must be a positive number
        :raises EmptyInputError: if amount is empty
        :raises InvalidInputError: if amount is not a valid positive number
        :return: None
        """
        if amount is None or amount.strip() == "":
            logger.warning("Amount is empty.")
            raise EmptyInputError("Amount cannot be empty.")
        try:
            amount = float(amount)
        except ValueError:
            logger.warning(f'Amount is invalid - "{amount}".')
            raise InvalidInputError(
                f"Amount is invalid - {amount}. It must be a number."
            )

        if amount < 0:
            logger.warning(f'Amount is invalid - "{amount}".')
            raise InvalidInputError(
                f"Amount is invalid - {amount}. It must be greater than zero."
            )

        self._amount = amount
        logger.info(f'Amount is set to - "{amount}".')

    @property
    def date(self) -> str:
        """
        Gets the transaction date.

        :return: str in "YYYY-MM-DD" format
        """
        return self._date

    @date.setter
    def date(self, date: str) -> None:
        """
        Sets the transaction date after validation.

        :param date: str in "YYYY-MM-DD" format, defaults to today if empty
        :raises InvalidInputError: if date format is invalid
        :return: None
        """
        if date is None or date.strip() == "":
            now = datetime.now().date()
            self._date = now.strftime("%Y-%m-%d")
            logger.info(f'Date is set to - "{self._date}".')
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                logger.warning(f"Date is invalid - {date}.")
                raise InvalidInputError(
                    f"Date is invalid - {date}. It must be in YYYY-MM-DD format."
                )
            self._date = date
            logger.info(f'Date is set to - "{date}".')

    @property
    def description(self) -> str:
        """
        Gets the transaction description.

        :return: str or None
        """
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """
        Sets the transaction description.

        :param description: str, optional
        :return: None
        """
        self._description = description

    def __repr__(self):
        """
        Returns a string representation of the transaction object.

        :return: str
        """
        return f"TransactionFactory(transaction_type={self.t_type!r}, category={self.category!r}, amount={self.amount!r}, date={self.date!r}, description={self.description!r})"
