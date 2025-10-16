from app.factories import TransactionFactory
from datetime import datetime
from app.logs import logger
from utils import InvalidInputError, TransactionNotFoundError, CategoryNotFoundError
from collections import defaultdict


class TransactionDictManager:
    def __init__(self) -> None:
        self.data = defaultdict(list)

    def add_transaction(self, transaction: TransactionFactory) -> None:
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

    def show_all_transactions_for_all_time(self):
        logger.info(f"Showing all transaction data.")

        if self.data:
            sorted_dates = sorted(
                self.data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d")
            )

            print("\n" + "=" * 50)
            for date in sorted_dates:
                print(f"📅 DATE: {date}")
                print("-" * 50)
                print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
                print("-" * 50)
                for transaction in self.data[date]:
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
                print("=" * 50)

        else:
            logger.info("No transactions recorded.")
            raise TransactionNotFoundError("No transactions recorded.")

    def _get_transactions_by_date_range(
        self, start_date: str, end_date: str
    ) -> list:
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                logger.info(f"End date: {end_date}.")
            except ValueError:
                logger.warning(f"End date {end_date} is not a valid date.")
                raise InvalidInputError("End date must be in YYYY-MM-DD format.")
        else:
            end_date = datetime.now().date()
            logger.info(f"End date {end_date}.")

        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                logger.info(f"Start date: {start_date}.")
            except ValueError:
                logger.warning(f"Start date {start_date} is not a valid date.")
                raise InvalidInputError("Start date must be in YYYY-MM-DD format.")

            if start_date > end_date:
                logger.warning(
                    "The start date is greater than or equal to the end date."
                )
                raise InvalidInputError(
                    "The start date cannot be greater than or equal to the end date."
                )

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
                    lambda date: datetime.strptime(date, "%Y-%m-%d").date() <= end_date,
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

    def show_transaction_by_date_range(self, start_date: str, end_date: str):
        logger.info("User selected to view transactions by date range.")

        sorted_dates = self._get_transactions_by_date_range(start_date, end_date)

        if not sorted_dates:
            logger.info("No transactions found.")
            raise TransactionNotFoundError(
                f"No transaction dates found for the specified period."
            )

        print("\n" + "=" * 50)
        for date in sorted_dates:
            print(f"📅 DATE: {date}")
            print("-" * 50)
            print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
            print("-" * 50)
            for transaction in self.data[date]:
                print(
                    f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                )
            print("=" * 50)

        logger.info(
            f"The transactions from the specified date up to today have been successfully viewed."
        )

    def show_transaction_income_by_range(self, start_date: str, end_date: str):
        logger.info('User selected to view transactions of type "income".')

        sorted_dates = self._get_transactions_by_date_range(start_date, end_date)

        if not sorted_dates:
            logger.info("There are no recorded income transactions.")
            raise TransactionNotFoundError("There are no income transactions.")

        filtered_dates = [
            date
            for date in sorted_dates
            if any(tx["t_type"] == "income" for tx in self.data[date])
        ]

        print("\n" + "=" * 50)
        for date in filtered_dates:
            print(f"📅 DATE: {date}")
            print("-" * 50)
            print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
            print("-" * 50)
            for transaction in self.data[date]:
                if transaction["t_type"] == "income":
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info('Transactions of type "income" have been successfully viewed.')

    def show_transaction_expenses_by_range(self, start_date: str, end_date: str):
        logger.info('User selected to view transactions of type "expense".')

        sorted_dates = self._get_transactions_by_date_range(start_date, end_date)

        if not sorted_dates:
            logger.info("There are no recorded expense transactions.")
            raise TransactionNotFoundError("There are no expense transactions.")

        filtered_dates = [
            date
            for date in sorted_dates
            if any(tx["t_type"] == "expense" for tx in self.data[date])
        ]

        print("\n" + "=" * 50)
        for date in filtered_dates:
            print(f"📅 DATE: {date}")
            print("-" * 50)
            print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
            print("-" * 50)
            for transaction in self.data[date]:

                if transaction["t_type"] == "expense":
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info('Transactions of type "expense" have been successfully viewed.')

    def show_transaction_by_category(
        self, category: str, start_date: str, end_date: str
    ):
        logger.info(f'User selected to view transactions of category - "{category}".')

        if category is None or category.strip() == "":
            logger.warning("Input category is empty.")
            raise InvalidInputError("The input category cannot be empty.")

        sorted_dates = self._get_transactions_by_date_range(start_date, end_date)

        if not sorted_dates:
            logger.info(f'No transactions recorded in the "{category}" category.')
            raise CategoryNotFoundError(
                f"No transactions recorded in the '{category}' category."
            )

        filtered_dates = [
            date
            for date in sorted_dates
            if any(tx["t_type"] == "expense" for tx in self.data[date])
        ]

        print("\n" + "=" * 50)
        for date in filtered_dates:
            print(f"📅 DATE: {date}")
            print("-" * 50)
            print(f"{'TYPE':<10} | {'CATEGORY':<12} | {'AMOUNT':<8} | DESCRIPTION")
            print("-" * 50)
            for transaction in self.data[date]:
                if transaction["category"].lower() == category.strip().lower():
                    print(
                        f"{transaction['t_type']:<10} | {transaction['category']:<12} | {transaction['amount']:<8} | {transaction['description']}"
                    )
            print("=" * 50)

        logger.info(
            f"Transaction in the category {category} have been successfully viewed."
        )

    def to_dict(self) -> dict:
        return dict(self.data)
