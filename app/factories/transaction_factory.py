from app.logs import logger
from utils import EmptyInputError, InvalidInputError
from datetime import datetime


class TransactionFactory:
    def __init__(self) -> None:
        self._t_type = None
        self._category = None
        self._amount = None
        self._date = None
        self._description = None

    @property
    def t_type(self) -> str:
        return self._t_type

    @t_type.setter
    def t_type(self, transaction_type: str) -> None:
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
        return self._category

    @category.setter
    def category(self, category: str) -> None:
        if category is None or category.strip() == "":
            logger.warning("Category is empty.")
            raise EmptyInputError("Category cannot be empty.")
        self._category = category
        logger.info(f'Category is set to - "{category}".')

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: str) -> None:
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
        return self._date

    @date.setter
    def date(self, date: str) -> None:
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
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    def __repr__(self):
        return f"TransactionFactory(transaction_type={self.t_type!r}, category={self.category!r}, amount={self.amount!r}, date={self.date!r}, description={self.description!r})"
