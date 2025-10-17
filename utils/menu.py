def main_menu():
    menu_text = (
        "\n" + "=" * 33 + "\n"
        "       FINANCE TRACKER\n" + "=" * 33 + "\n"
        "1. Add a transaction\n"
        "2. View transactions\n"
        "3. Financial summary\n"
        "4. Delete a transaction\n"
        "0. Exit\n" + "=" * 33
    )
    print(menu_text)


def view_transactions_menu():
    menu_text = (
        "\n" + "=" * 33 + "\n"
        "   VIEW TRANSACTIONS MENU\n" + "=" * 33 + "\n"
        "1. Show all transactions for all time\n"
        "2. Show transactions by date range\n"
        "3. Show all incomes by date range\n"
        "4. Show all expenses by date range\n"
        "5. Show transactions by category (date range optional)\n"
        "0. Back to main menu\n" + "=" * 33
    )
    print(menu_text)


def view_financial_summary():
    menu_text = (
        "\n" + "=" * 33 + "\n"
        "       VIEW FINANCIAL SUMMARY\n"
        + "=" * 33 + "\n"
        "1. View total income by date range\n"
        "2. View total expenses by date range\n"
        "3. View current balance\n"
        "0. Back to main menu\n"
        + "=" * 33
    )
    print(menu_text)
