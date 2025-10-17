from pathlib import Path
from app import JsonStorage, TransactionDictManager, logger, TransactionFactory
from utils import (
    EmptyInputError,
    InvalidInputError,
    TransactionNotFoundError,
    CategoryNotFoundError,
)
from utils.deserializer import deserialize_transactions
from utils.menu import main_menu, view_transactions_menu, view_financial_summary
from utils.cli_menu import handle_menu_choice
import sys


PATTERN_MAIN_MENU = ["0", "1", "2", "3", "4"]
PATTERN_VIEW_TRANSACTIONS_MENU = ["0", "1", "2", "3", "4", "5"]
PATTERN_VIEW_FINANCIAL_SUMMARY_MENU = ["0", "1", "2", "3"]

def main(json_path: Path | str | None = None):
    logger.info("Starting the CLI application.")

    json_handler = JsonStorage(json_path)
    json_content = json_handler.read_json()

    manager = TransactionDictManager()

    try:
        deserialize_transactions(json_content, manager)
        while True:
            logger.info("Navigated to main menu of FINANCE TRACKER.")
            main_menu()
            option = input("Select an option: ").strip()
            try:
                handle_menu_choice(option, PATTERN_MAIN_MENU)
            except (EmptyInputError, InvalidInputError) as message:
                print(f"{message}\n")

            if option == "0":
                logger.info("User selected to exit the program.")
                sys.exit(0)
            elif option == "1":
                logger.info("User selected: Add a transaction")
                transaction = TransactionFactory()
                while True:
                    try:
                        transaction_type = (
                            input("Enter transaction type (income/expense): ")
                            .strip()
                            .lower()
                        )
                        transaction.t_type = transaction_type
                        break
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                while True:
                    try:
                        category = input("Enter transaction category: ").strip()
                        transaction.category = category
                        break
                    except EmptyInputError as message:
                        print(f"{message}\n")

                while True:
                    try:
                        amount = input("Enter transaction amount: ").strip()
                        transaction.amount = amount
                        break
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                while True:
                    try:
                        date = input(
                            "Enter transaction date (YYYY-MM-DD, empty = today): "
                        ).strip()
                        transaction.date = date
                        break
                    except InvalidInputError as message:
                        print(f"{message}\n")

                description = (
                    input("Enter transaction description: ").strip().capitalize()
                )
                transaction.description = description

                manager.add_transaction(transaction)
            elif option == "2":
                logger.info("Navigated to VIEW TRANSACTIONS MENU")
                while True:
                    view_transactions_menu()
                    option = input("Select an option: ").strip()
                    try:
                        handle_menu_choice(option, PATTERN_VIEW_TRANSACTIONS_MENU)
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                    if option == "0":
                        logger.info("User selected to exit the main menu.")
                        break

                    elif option == "1":
                        try:
                            manager.show_all_transactions_for_all_time()
                        except TransactionNotFoundError as message:
                            print(f"{message}\n")

                    elif option == "2":
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                manager.show_transaction_by_date_range(transaction_dates)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                            except TransactionNotFoundError as message:
                                print(f"{message}\n")
                                break

                    elif option == "3":
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                manager.show_transaction_income_by_range(transaction_dates)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                            except TransactionNotFoundError as message:
                                print(f"{message}\n")
                                break

                    elif option == "4":
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                manager.show_transaction_expenses_by_range(transaction_dates)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                            except TransactionNotFoundError as message:
                                print(f"{message}\n")
                                break

                    elif option == "5":
                        choice_category = (
                            input("Enter transaction category: ").strip().lower()
                        )
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                manager.show_transaction_by_category(choice_category, transaction_dates)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                                continue
                            except (CategoryNotFoundError, TransactionNotFoundError) as message:
                                print(f"{message}\n")
                                break

            elif option == "3":
                logger.info("Navigated to VIEW FINANCIAL SUMMARY")
                while True:
                    view_financial_summary()

                    option = input("Select an option: ").strip()
                    try:
                        handle_menu_choice(option, PATTERN_VIEW_FINANCIAL_SUMMARY_MENU)
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                    if option == "0":
                        logger.info("User selected to exit the main menu.")
                        break
                    elif option == "1":
                        tr_type = "income"
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                print(manager.show_total_type_by_range(tr_type, transaction_dates))
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                            except TransactionNotFoundError as message:
                                print(f"{message}\n")
                                break

                    elif option == "2":
                        tr_type = "expense"
                        while True:
                            start_date = input(
                                "Enter the start date in YYYY-MM-DD format. "
                                "If left empty, all dates up to the specified end date will be considered: "
                            ).strip()
                            try:
                                date_range_fn = manager.get_transactions_by_date_range(start_date)
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")

                        while True:
                            end_date = input(
                                "Enter the end date (YYYY-MM-DD). "
                                "If left empty, today's date will be used: "
                            ).strip()

                            try:
                                transaction_dates = date_range_fn(end_date)
                                print(manager.show_total_type_by_range(tr_type, transaction_dates))
                                break
                            except InvalidInputError as message:
                                print(f"{message}\n")
                            except TransactionNotFoundError as message:
                                print(f"{message}\n")
                                break

                    elif option == "3":
                        print(manager.show_current_balance())

            elif option == "4":
                while True:
                    choice_date = input("Enter the date of the transaction to delete (YYYY-MM-DD): ").strip()
                    if not choice_date:
                        logger.warning("Input date is empty.")
                        print("Input date cannot be empty.\n")
                        continue
                    try:
                        list_transaction = manager.show_transaction_by_date(
                            choice_date
                        )
                    except InvalidInputError as message:
                        print(f"{message}\n")
                        continue
                    except TransactionNotFoundError as message:
                        print(f"{message}\n")
                        break

                    while True:
                        choice_transaction = input("Select the serial number of the transaction you want to delete: ").strip()
                        try:
                            list_transaction(choice_transaction)
                            break
                        except IndexError as message:
                            print(f"{message}\n")
                    break

    except KeyboardInterrupt:
        logger.info("Program interrupted by user (Ctrl+C). Exiting safely.")
        sys.exit(0)
    finally:
        json_handler.write_json(manager.to_dict())
        logger.info('The data has been successfully saved to the file "data.json".')


if __name__ == "__main__":
    main()
