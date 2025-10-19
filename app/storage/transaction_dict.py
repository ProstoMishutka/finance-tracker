from collections import defaultdict
from datetime import datetime
from typing import Callable

from app.factories import TransactionFactory
from app.logs import logger
from utils import (
    InvalidInputError,
    TransactionNotFoundError,
    CategoryNotFoundError,
    DateNotFoundError,
)


class TransactionDictManager:
    """
    A class to manage user transactions using a dictionary.
    The dictionary uses dates as keys and lists of transactions as values.
    """

    def __init__(self) -> None:
        """
        Initializes the transaction manager with a defaultdict of lists.
        """
        self.data = defaultdict(list)

    @staticmethod
    def print_transaction_header(date: str) -> None:
        """
        Prints a transaction table header for a given date.

        :param date: str - the date of transactions in YYYY-MM-DD format
        """
        print("\n" + "=" * 50)
        print(f"📅 DATE: {date}")
        print("-" * 50)
        print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
        print("-" * 50)

    def add_transaction(self, transaction: TransactionFactory) -> None:
        """
        Adds a transaction to the manager's dictionary.

        :param transaction: TransactionFactory - the transaction object
        """
        transaction_data = {
            "t_type": transaction.t_type,
            "category": transaction.category,
            "amount": transaction.amount,
            "date": transaction.date,
            "description": (
                transaction.description if transaction.description is not None else "-"
            ),
        }

        self.data[transaction.date].append(transaction_data)
        logger.info(
            f"Added transaction | type={transaction_data['t_type']} | "
            f"amount={transaction_data['amount']} | category={transaction_data['category']} | "
            f"date={transaction_data['date']}"
        )

    def show_all_transactions_for_all_time(self) -> None:
        """
        Displays all transactions sorted by date.

        :raises TransactionNotFoundError: if there are no transactions recorded
        """
        logger.info(f"Showing all transaction data.")

        if not self.data:
            logger.info("No transactions recorded.")
            raise TransactionNotFoundError("No transactions recorded.")

        sorted_dates = sorted(
            self.data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d")
        )

        for date in sorted_dates:
            self.print_transaction_header(date)
            for transaction in self.data[date]:
                print(
                    f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                )
            print("=" * 50)

    def get_transactions_by_date_range(self, start_date: str) -> Callable:
        """
        Returns a function to filter transactions by end date.
        If start_date is empty, all transactions up to end_date are returned.

        :param start_date: str - start date in YYYY-MM-DD format or empty
        :raises InvalidInputError: if date format is invalid
        :return: function(end_date) -> list of filtered dates
        """
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                logger.info(f"Start date: '{start_date}'.")
            except ValueError:
                logger.warning(f"Start date '{start_date}' is not a valid date.")
                raise InvalidInputError("Start date must be in YYYY-MM-DD format.")

        def inner(end_date: str) -> list[str]:
            if end_date:
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    logger.info(f"End date: '{end_date}'.")
                except ValueError:
                    logger.warning(f"End date '{end_date}' is not a valid date.")
                    raise InvalidInputError("End date must be in YYYY-MM-DD format.")
            else:
                end_date = datetime.now().date()
                logger.info(f"End date '{end_date}'.")

            if start_date:
                if start_date > end_date:
                    logger.warning(
                        "The start date is greater than or equal to the end date."
                    )
                    raise InvalidInputError(
                        "The start date cannot be greater than or equal to the end date."
                    )

                # Filter dates between start_date and end_date (inclusive)
                filtered_dates = list(
                    filter(
                        lambda date: start_date
                        <= datetime.strptime(date, "%Y-%m-%d").date()
                        <= end_date,
                        self.data.keys(),
                    )
                )

                if filtered_dates:
                    sorted_dates = sorted(
                        filtered_dates, key=lambda d: datetime.strptime(d, "%Y-%m-%d")
                    )

                    logger.info(
                        f"Transaction dates list filtered by {len(filtered_dates)} dates."
                    )
                    return sorted_dates

                logger.info(f"No transaction dates found for the specified period.")
                return filtered_dates

            else:
                filtered_dates = list(
                    filter(
                        lambda date: datetime.strptime(date, "%Y-%m-%d").date()
                        <= end_date,
                        self.data.keys(),
                    )
                )

                if filtered_dates:
                    sorted_dates = sorted(
                        filtered_dates, key=lambda d: datetime.strptime(d, "%Y-%m-%d")
                    )

                    logger.info(
                        f"Transaction dates list filtered by {len(filtered_dates)} dates."
                    )
                    return sorted_dates

                logger.info(f"No transaction dates found for the specified period.")
                return filtered_dates

        return inner

    def show_transaction_by_date_range(self, sorted_dates: list[str]) -> None:
        """
        Displays transactions for a specified date range.

        :param sorted_dates: list - sorted dates to display
        :raises TransactionNotFoundError: if no transactions exist for the range
        """
        logger.info("User selected to view transactions by date range.")

        if not sorted_dates:
            logger.info("No transactions found.")
            raise TransactionNotFoundError(
                f"No transaction dates found for the specified period."
            )

        for date in sorted_dates:
            self.print_transaction_header(date)
            for transaction in self.data[date]:
                print(
                    f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                )
            print("=" * 50)

        logger.info(
            f"The transactions from the specified date up to today have been successfully viewed."
        )

    def show_transaction_income_by_range(self, sorted_dates: list[str]) -> None:
        """
        Displays only income transactions in the specified date range.

        :param sorted_dates: list - sorted dates to display
        :raises TransactionNotFoundError: if no income transactions exist in the range
        """
        logger.info('User selected to view transactions of type "income".')

        if not sorted_dates:
            logger.info("There are no recorded income transactions.")
            raise TransactionNotFoundError("There are no income transactions.")

        filtered_dates = [
            date
            for date in sorted_dates
            if any(t["t_type"] == "income" for t in self.data[date])
        ]

        if not filtered_dates:
            logger.info("No income transactions found in the specified period.")
            raise TransactionNotFoundError(
                "No income transactions found for the specified period."
            )

        logger.debug(f"Filtered {len(filtered_dates)} dates: {filtered_dates}")

        for date in filtered_dates:
            self.print_transaction_header(date)
            for transaction in self.data[date]:
                if transaction["t_type"] == "income":
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info('Transactions of type "income" have been successfully viewed.')

    def show_transaction_expenses_by_range(self, sorted_dates: list[str]) -> None:
        """
        Displays only expense transactions in the specified date range.

        :param sorted_dates: list - sorted dates to display
        :raises TransactionNotFoundError: if no expense transactions exist in the range
        """
        logger.info('User selected to view transactions of type "expense".')

        if not sorted_dates:
            logger.info("There are no recorded expense transactions.")
            raise TransactionNotFoundError("There are no expense transactions.")

        filtered_dates = [
            date
            for date in sorted_dates
            if any(t["t_type"] == "expense" for t in self.data[date])
        ]

        if not filtered_dates:
            logger.info("No expense transactions found in the specified period.")
            raise TransactionNotFoundError(
                "No expense transactions found for the specified period."
            )

        logger.debug(f"Filtered {len(filtered_dates)} dates: {filtered_dates}")

        for date in filtered_dates:
            self.print_transaction_header(date)
            for transaction in self.data[date]:
                if transaction["t_type"] == "expense":
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info('Transactions of type "expense" have been successfully viewed.')

    def show_transaction_by_category(
        self, category: str, sorted_dates: list[str]
    ) -> None:
        """
        Displays transactions filtered by a specific category.

        :param category: str - the category to filter by
        :param sorted_dates: list - sorted dates to display
        :raises InvalidInputError: if category input is empty
        :raises CategoryNotFoundError: if no transactions exist for the category
        :raises TransactionNotFoundError: if no transactions are found in the range
        """
        logger.info(f'User selected to view transactions of category - "{category}".')

        if category is None or category.strip() == "":
            logger.warning("Input category is empty.")
            raise InvalidInputError("The input category cannot be empty.")

        if not sorted_dates:
            logger.info(f'No transactions recorded in the "{category}" category.')
            raise CategoryNotFoundError(
                f"No transactions recorded in the '{category}' category."
            )

        filtered_dates = [
            date
            for date in sorted_dates
            if any(t["category"].lower() == category for t in self.data[date])
        ]

        if not filtered_dates:
            logger.info(
                f'No  category - "{category}" transactions found in the specified period.'
            )
            raise TransactionNotFoundError(
                f'No category - "{category}" transactions found for the specified period.'
            )

        logger.debug(f"Filtered {len(filtered_dates)} dates: {filtered_dates}")

        for date in filtered_dates:
            self.print_transaction_header(date)
            for transaction in self.data[date]:
                if transaction["category"].lower() == category.strip().lower():
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info(
            f"Transaction in the category {category} have been successfully viewed."
        )

    def show_total_type_by_range(self, tr_type, sorted_dates: list[str]) -> str | None:
        """
        Displays the total amount for a specific transaction type (income/expense) in the given range.

        :param tr_type: str - "income" or "expense"
        :param sorted_dates: list - sorted dates to calculate total
        :raises TransactionNotFoundError: if no transactions exist for the type
        """
        logger.info(
            f"User selected to view the total {tr_type} amount for the specified period."
        )

        if not sorted_dates:
            logger.info(f"There are no recorded {tr_type} transactions.")
            raise TransactionNotFoundError(f"There are no {tr_type} transactions.")

        filtered_dates = [
            date
            for date in sorted_dates
            if any(tr["t_type"] == tr_type for tr in self.data[date])
        ]

        if not filtered_dates:
            logger.info(f"No {tr_type} transactions found in the specified period.")
            raise TransactionNotFoundError(
                f"No {tr_type} transactions found for the specified period."
            )

        logger.debug(f"Filtered {len(filtered_dates)} dates: {filtered_dates}")

        total_type = sum(
            transaction["amount"]
            for date in filtered_dates
            for transaction in self.data[date]
            if transaction["t_type"] == tr_type
        )

        logger.info(f"Total {tr_type} for the specified period — {total_type:.2f}.")
        print(f"Total {tr_type} for the specified period — {total_type:.2f}.")

    def show_current_balance(self) -> None:
        """
        Displays the current balance (total income - total expenses).
        """
        logger.info(f"User selected to view the current balance.")

        transactions = [
            transaction for items in self.data.values() for transaction in items
        ]

        total_income = sum(
            transaction["amount"]
            for transaction in transactions
            if transaction["t_type"] == "income"
        )

        total_expense = sum(
            transaction["amount"]
            for transaction in transactions
            if transaction["t_type"] == "expense"
        )

        balance = total_income - total_expense
        print(f"Current balance: {balance:.2f}")

    def show_transaction_by_date(self, date: str) -> Callable:
        """
        Displays all transactions for a specific date and returns a function
        to delete a transaction by its index.

        :param date: str - the date in YYYY-MM-DD format
        :raises DateNotFoundError: if the input date is empty
        :raises InvalidInputError: if the date format is invalid
        :raises TransactionNotFoundError: if no transactions exist for the given date
        :return: function(index: str) -> None
        Returns a function to delete a transaction by its 1-based index.
        """
        if not date:
            logger.warning("Input date is empty.")
            raise DateNotFoundError(f"Input date is empty.")

        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            date = date.isoformat()
        except ValueError:
            logger.warning(f"Input date is invalid.")
            raise InvalidInputError(
                f"Input date is invalid. It must be in the format YYYY-MM-DD."
            )

        filtered_transaction = [
            transaction
            for items in self.data.values()
            for transaction in items
            if transaction["date"] == date
        ]

        if not filtered_transaction:
            logger.info(f"No transactions found in the date {date}.")
            raise TransactionNotFoundError(
                f"No transactions found for the date - {date}."
            )

        for i, transaction in enumerate(filtered_transaction, start=1):
            print(
                f"{i}: [{transaction['date']}] {transaction['t_type']} | {transaction['category']} | {transaction['amount']:<8} | {transaction['description']}"
            )

        def delete_transaction(index: str) -> None:
            """
            Deletes a transaction by its 1-based index from the specified date.

            :param index: str - 1-based index of the transaction to delete
            :raises IndexError: if the index is out of range
            """
            if not index.isdigit():
                logger.warning(f"Index '{index}' isn`t number.")
                raise InvalidInputError(f"Input value must be an integer.")

            if (int(index) - 1) not in range(len(filtered_transaction)):
                logger.warning(f"The index {index} is out of range.")
                raise IndexError(
                    f"Index must be between 1 and {len(filtered_transaction)}."
                )

            deleted_transaction = filtered_transaction.pop(int(index) - 1)
            self.data[date].remove(deleted_transaction)

            if not self.data[date]:
                del self.data[date]

            logger.info(f"Deleted transaction: {deleted_transaction}")
            print(
                f"Successfully deleted transaction: [{deleted_transaction['date']}] {deleted_transaction['t_type']} | {deleted_transaction['category']} | {deleted_transaction['amount']:<8} | {deleted_transaction['description']}"
            )
            return

        return delete_transaction

    def to_dict(self) -> dict:
        """
        Converts the transaction data to a standard dictionary.

        :return: dict - dictionary with dates as keys and list of transactions as values
        """
        return dict(self.data)
