from app.storage import TransactionDictManager
from app.factories import TransactionFactory


def deserialize_transactions(json_data: dict, manager: TransactionDictManager) -> None:
    """
    Deserialize JSON data and add transactions to the TransactionDictManager.

    :param json_data: dict
       A dictionary of transactions in the format "YYYY-MM-DD": [list of transaction dicts].
    :param manager: TransactionDictManager
       An instance of TransactionDictManager where the deserialized transactions will be added.
    :return: None
    """
    for key, value in json_data.items():
        for item in value:
            transaction = TransactionFactory()
            transaction.t_type = item["t_type"]
            transaction.category = item["category"]
            transaction.amount = str(item["amount"])
            transaction.date = item["date"]
            transaction.description = item["description"]

            manager.add_transaction(transaction)
