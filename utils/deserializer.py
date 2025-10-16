from app.storage import TransactionDictManager
from app.factories import TransactionFactory


def deserialize_transactions(json_data: dict, manager: TransactionDictManager):
    for key, value in json_data.items():
        for item in value:
            transaction = TransactionFactory()
            transaction.t_type = item["t_type"]
            transaction.category = item["category"]
            transaction.amount = str(item["amount"])
            transaction.date = item["date"]
            transaction.description = item["description"]

            manager.add_transaction(transaction)
