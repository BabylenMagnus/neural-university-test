import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum


class AccountType(Enum):
    BASE = 'base'
    SAVING = 'saving'
    CREDIT = 'credit'


class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdraw'


class Client:
    def __init__(self):
        self.accounts = []

    def create_account(self, account_type, interest_rate=None, limit=None, date_creation=None):
        if (
                account_type == AccountType.SAVING or account_type == AccountType.CREDIT
        ) and (
                interest_rate is None or limit is None
        ):
            raise ValueError("Interest rate and limit must be provided for saving and credit account")

        if account_type == AccountType.SAVING:
            account = SavingsAccount(limit, interest_rate, date_creation)
        elif account_type == AccountType.CREDIT:
            account = CreditAccount(limit, interest_rate, date_creation)
        elif account_type == AccountType.BASE:
            account = Account()
        else:
            raise ValueError("Invalid account type")

        self.accounts.append(account)
        return account


class Account:
    def __init__(self):
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction(TransactionType.DEPOSIT, amount))

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        self.transactions.append(Transaction(TransactionType.WITHDRAWAL, amount))

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return "Выписка по счёту:\n" + "\n".join(map(str, self.transactions))


class SavingsAccount(Account):
    def __init__(self, limit, interest_rate, date_creation: datetime = datetime.datetime.now()):
        super().__init__()
        self.interest_rate = interest_rate
        self.date_creation = datetime.datetime.now() if date_creation is None else date_creation
        self.current_balance = self.balance
        self.balance = limit

    def calculate_interest(self):
        delt = relativedelta(datetime.date.today(), self.date_creation)
        months = delt.years * 12 + delt.months
        self.current_balance = self.balance * (self.interest_rate / 12 * months / 100 + 1)
        return self.current_balance

    def withdraw(self, *args, **kwargs):
        raise "Операция невозможна"


class CreditAccount(Account):
    def __init__(self, limit, interest_rate, date_creation: datetime = datetime.datetime.now()):
        super().__init__()
        self.start_balance = limit
        self.balance = limit
        self.date_creation = datetime.datetime.now() if date_creation is None else date_creation
        self.interest_rate = interest_rate

    def calculate_loan(self):
        delt = relativedelta(datetime.date.today(), self.date_creation)
        months = delt.years * 12 + delt.months
        loan_amount = self.start_balance * (self.interest_rate / 12 * months / 100 + 1)
        return loan_amount


class Transaction:
    def __init__(self, transaction_type, amount):
        self.type = transaction_type
        self.amount = amount
        self.date = datetime.datetime.now()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} {self.type.value} - {self.amount}"


if __name__ == '__main__':
    interest_rate = 12

    client = Client()
    credit_account = client.create_account(
        AccountType.CREDIT, interest_rate=interest_rate, limit=200000, date_creation=datetime.date(2023, 3, 10)
    )
    credit_account.withdraw(15000)
    print("задолженность по кредиту: ", credit_account.calculate_loan())

    saving_account = client.create_account(
        AccountType.SAVING, interest_rate=interest_rate, limit=1500000, date_creation=datetime.date(2022, 7, 10)
    )
    print("Баланс на накопительном счёте: ", saving_account.calculate_interest())

    base_account = client.create_account(AccountType.BASE)
    base_account.deposit(10000)
    base_account.withdraw(7000)
    base_account.withdraw(400)
    base_account.withdraw(500)
    base_account.deposit(5000)
    print(base_account.get_transactions())

