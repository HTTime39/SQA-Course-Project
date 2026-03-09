from transaction_executor import TransactionExecutor
from transaction_record_parser import TransactionRecordParser


class TransactionProcessor:
    """
    Processes transactions and applies updates to bank accounts.
    """

    def __init__(self, accounts):
        """
        Constructs TransactionProcessor objects.
        :param accounts: BankAccounts object.
        """
        self.accounts = accounts
        self.executor = TransactionExecutor(self.accounts)
        self.parser = TransactionRecordParser()

    def process_transaction(self, transaction_record):
        """
        Processes a transaction.
        :param transaction_record: Transaction record from 'merged bank account transactions' file
        """
        transaction_code = self.parser.parse_transaction_code(transaction_record)

        if transaction_code == "04":
            self.handle_deposit_transaction(transaction_record)
        elif transaction_code == "01":
            self.handle_withdrawal_transaction(transaction_record)
        elif transaction_code == "02":
            self.handle_transfer_transaction(transaction_record)
        elif transaction_code == "03":
            self.handle_pay_bill_transaction(transaction_record)
        elif transaction_code == "05":
            self.handle_create_account_transaction(transaction_record)
        elif transaction_code == "06":
            self.handle_delete_account_transaction(transaction_record)
        elif transaction_code == "07":
            self.handle_disable_account_transaction(transaction_record)
        elif transaction_code == "08":
            self.handle_change_account_plan_transaction(transaction_record)

    def handle_deposit_transaction(self, transaction_record):
        """
        Handles a 'deposit' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        amount = self.parser.parse_amount(transaction_record)
        self.executor.execute_deposit(account_number, amount)
        self.accounts.apply_transaction_fee(account_number)

    def handle_withdrawal_transaction(self, transaction_record):
        """
        Handles a 'withdrawal' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        amount = self.parser.parse_amount(transaction_record)
        self.executor.execute_withdrawal(account_number, amount)
        self.accounts.apply_transaction_fee(account_number)

    def handle_transfer_transaction(self, transaction_record):
        """
        Handles a 'transfer' transaction.
        :param transaction_record: Transaction record
        """
        from_account_number = self.parser.parse_account_number(transaction_record)
        partial_to_account_number = self.parser.parse_misc_data(transaction_record)
        amount = self.parser.parse_amount(transaction_record)
        self.executor.execute_transfer(
            from_account_number, partial_to_account_number, amount
        )
        self.accounts.apply_transaction_fee(from_account_number)

    def handle_pay_bill_transaction(self, transaction_record):
        """
        Handles a 'pay bill' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        amount = self.parser.parse_amount(transaction_record)
        self.executor.execute_pay_bill(account_number, amount)
        self.accounts.apply_transaction_fee(account_number)

    def handle_create_account_transaction(self, transaction_record):
        """
        Handles a 'create account' transaction.
        :param transaction_record: Transaction record
        """
        account_holder_name = self.parser.parse_account_holder_name(transaction_record)
        account_number = self.parser.parse_account_number(transaction_record)
        amount = self.parser.parse_amount(transaction_record)
        self.executor.execute_create_account(
            account_holder_name, account_number, amount
        )

    def handle_delete_account_transaction(self, transaction_record):
        """
        Handles a 'delete' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        self.executor.execute_delete_account(account_number)

    def handle_disable_account_transaction(self, transaction_record):
        """
        Handles a 'disable' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        self.executor.execute_disable_account(account_number)

    def handle_change_account_plan_transaction(self, transaction_record):
        """
        Handles a 'change account plan' transaction.
        :param transaction_record: Transaction record
        """
        account_number = self.parser.parse_account_number(transaction_record)
        account_plan = self.parser.parse_misc_data(transaction_record)
        self.executor.execute_change_account_plan(account_number, account_plan)
        self.accounts.apply_transaction_fee(account_number)
