class TransactionExecutor:

    def __init__(self, accounts):
        pass

    def execute_deposit(self, account_number, amount):
        pass

    def execute_withdrawal(self, account_number, amount):
        pass

    def execute_transfer(self, from_account_number, partial_to_account_number, amount):
        pass

    def execute_pay_bill(self, account_number, amount):
        pass

    def execute_create_account(
        self, account_holder_name, account_number, initial_balance
    ):
        pass

    def execute_delete_account(self, account_number):
        pass

    def execute_disable_account(self, account_number):
        pass

    def execute_change_account_plan(self, account_number, new_account_plan):
        pass
