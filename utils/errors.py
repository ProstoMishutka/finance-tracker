class FinanceTrackerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptyInputError(FinanceTrackerError):
    pass


class InvalidInputError(FinanceTrackerError):
    pass


class TransactionNotFoundError(FinanceTrackerError):
    pass


class CategoryNotFoundError(FinanceTrackerError):
    pass


class DateNotFoundError(FinanceTrackerError):
    pass
