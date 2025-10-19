"""
Finance Tracker CLI Application

This module provides a command-line interface (CLI) for managing personal finance transactions.
Users can add, view, summarize, and delete transactions. Data is stored in JSON format and loaded
at startup. The application logs all actions for auditing and debugging purposes.

Main Features:
- Add transactions (income/expense) with category, amount, date, and description.
- View all transactions, or filter by date range, type, or category.
- View financial summaries including total income, total expenses, and current balance.
- Delete transactions by date and index.

Menu Overview:
- Main Menu:
    0: Exit the program
    1: Add a transaction
    2: View transactions menu
    3: View financial summary menu
    4: Delete a transaction by date

- View Transactions Menu:
    0: Return to main menu
    1: View all transactions for all time
    2: View transactions by date range
    3: View income transactions by date range
    4: View expense transactions by date range
    5: View transactions by category

- View Financial Summary Menu:
    0: Return to main menu
    1: Show total income for a date range
    2: Show total expenses for a date range
    3: Show current balance
"""

import sys
from pathlib import Path

from app import JsonStorage, TransactionDictManager, logger, TransactionFactory
from utils import (
    EmptyInputError,
    InvalidInputError,
    TransactionNotFoundError,
)
from utils.deserializer import deserialize_transactions
from utils.menu import main_menu, view_transactions_menu, view_financial_summary
from utils.cli_menu import handle_menu_choice, execute_menu_option


# Allowed options for main menu and submenus
PATTERN_MAIN_MENU = ["0", "1", "2", "3", "4"]
PATTERN_VIEW_TRANSACTIONS_MENU = ["0", "1", "2", "3", "4", "5"]
PATTERN_VIEW_FINANCIAL_SUMMARY_MENU = ["0", "1", "2", "3"]


def main(json_path: Path | str | None = None):
    """
    Entry point for the Finance Tracker CLI application.

    :param json_path: Optional path to a JSON file to load/save transactions.
                      Defaults to None (will use default data.json).
    """
    logger.info("Starting the CLI application.")

    # Load existing transactions from JSON
    json_handler = JsonStorage(json_path)
    json_content = json_handler.read_json()

    manager = TransactionDictManager()

    try:
        deserialize_transactions(json_content, manager)
        while True:
            logger.info("Navigated to main menu of FINANCE TRACKER.")
            main_menu()  # Display main menu

            option = input("Select an option: ").strip()
            try:
                handle_menu_choice(option, PATTERN_MAIN_MENU)
            except (EmptyInputError, InvalidInputError) as message:
                print(f"{message}\n")

            # Main menu options
            if option == "0":
                # Exit program
                logger.info("User selected to exit the program.")
                sys.exit(0)
            elif option == "1":
                # Add a transaction
                logger.info("User selected: Add a transaction")
                transaction = TransactionFactory()

                # Input type (income/expense)
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

                # Input category
                while True:
                    try:
                        category = input("Enter transaction category: ").strip()
                        transaction.category = category
                        break
                    except EmptyInputError as message:
                        print(f"{message}\n")

                # Input amount
                while True:
                    try:
                        amount = input("Enter transaction amount: ").strip()
                        transaction.amount = amount
                        break
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                # Input date (empty defaults to today)
                while True:
                    try:
                        date = input(
                            "Enter transaction date (YYYY-MM-DD, empty = today): "
                        ).strip()
                        transaction.date = date
                        break
                    except InvalidInputError as message:
                        print(f"{message}\n")

                # Input description
                description = (
                    input("Enter transaction description: ").strip().capitalize()
                )
                transaction.description = description

                # Add transaction to manager
                manager.add_transaction(transaction)

            elif option == "2":
                # View transactions submenu
                logger.info("Navigated to VIEW TRANSACTIONS MENU")
                while True:
                    view_transactions_menu()  # Display submenu
                    option = input("Select an option: ").strip()
                    try:
                        handle_menu_choice(option, PATTERN_VIEW_TRANSACTIONS_MENU)
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                    # Submenu options
                    if option == "0":
                        # Return to main menu
                        logger.info("User selected to exit the main menu.")
                        break

                    elif option == "1":
                        # Show all transactions
                        try:
                            manager.show_all_transactions_for_all_time()
                        except TransactionNotFoundError as message:
                            print(f"{message}\n")

                    elif option == "2":
                        # Show transactions by date range
                        execute_menu_option(
                            manager, manager.show_transaction_by_date_range
                        )

                    elif option == "3":
                        # Show only income transactions by date range
                        execute_menu_option(
                            manager, manager.show_transaction_income_by_range
                        )

                    elif option == "4":
                        # Show only expense transactions by date range
                        execute_menu_option(
                            manager, manager.show_transaction_expenses_by_range
                        )

                    elif option == "5":
                        # Show transactions filtered by category
                        while True:
                            choice_category = (
                                input("Enter transaction category: ").strip().lower()
                            )
                            try:
                                if not choice_category:
                                    logger.warning("The 'category' field is empty")
                                    raise EmptyInputError(
                                        "Please enter the transaction category"
                                    )
                            except EmptyInputError as message:
                                print(f"{message}\n")
                                continue

                            break
                        execute_menu_option(
                            manager,
                            manager.show_transaction_by_category,
                            choice_category,
                        )

            elif option == "3":
                # View financial summary submenu
                logger.info("Navigated to VIEW FINANCIAL SUMMARY")
                while True:
                    view_financial_summary()

                    option = input("Select an option: ").strip()
                    try:
                        handle_menu_choice(option, PATTERN_VIEW_FINANCIAL_SUMMARY_MENU)
                    except (EmptyInputError, InvalidInputError) as message:
                        print(f"{message}\n")

                    # Submenu options
                    if option == "0":
                        # Return to main menu
                        logger.info("User selected to exit the main menu.")
                        break

                    elif option == "1":
                        # Show total income for date range
                        tr_type = "income"
                        execute_menu_option(
                            manager, manager.show_total_type_by_range, tr_type
                        )

                    elif option == "2":
                        # Show total expenses for date range
                        tr_type = "expense"
                        execute_menu_option(
                            manager, manager.show_total_type_by_range, tr_type
                        )

                    elif option == "3":
                        # Show current balance
                        manager.show_current_balance()

            elif option == "4":
                # Delete transaction by date
                while True:
                    choice_date = input(
                        "Enter the date of the transaction to delete (YYYY-MM-DD): "
                    ).strip()
                    if not choice_date:
                        logger.warning("Input date is empty.")
                        print("Input date cannot be empty.\n")
                        continue
                    try:
                        list_transaction = manager.show_transaction_by_date(choice_date)
                    except InvalidInputError as message:
                        print(f"{message}\n")
                        continue
                    except TransactionNotFoundError as message:
                        print(f"{message}\n")
                        break

                    while True:
                        choice_transaction = input(
                            "Select the serial number of the transaction you want to delete: "
                        ).strip()
                        try:
                            list_transaction(choice_transaction)
                            break
                        except (InvalidInputError, IndexError) as message:
                            print(f"{message}\n")
                    break

    except KeyboardInterrupt:
        logger.info("Program interrupted by user (Ctrl+C). Exiting safely.")
        sys.exit(0)
    finally:
        # Save all transactions to JSON on exit
        json_handler.write_json(manager.to_dict())
        logger.info('The data has been successfully saved to the file "data.json".')


if __name__ == "__main__":
    main()
