class TransactionExecutor:
    """
    Executes transactions.
    """

    def __init__(self, accounts):
        """
        Constructs a TransactionExecutor object.
        :param accounts: BankAccounts object.
        """
        self.accounts = accounts

    def execute_deposit(self, account_number, amount):
        """
        Executes a 'deposit' transaction.
        :param account_number: Account number
        :param amount: Amount to deposit
        """
        if not self.accounts.is_account_valid(account_number):
            return

        self.accounts.accounts[account_number]["balance"] += amount
        self.accounts.accounts[account_number]["num_transactions"] += 1

    def execute_withdrawal(self, account_number, amount):
        """
        Executes a 'withdrawal' transaction.
        :param account_number: Account number
        :param amount: Amount to withdraw
        """
        if not self.accounts.is_account_valid(account_number):
            return
        if not self.accounts.are_funds_sufficient(
            account_number, self.accounts.accounts[account_number]["balance"], amount
        ):
            return

        self.accounts.accounts[account_number]["balance"] -= amount
        self.accounts.accounts[account_number]["num_transactions"] += 1

    def execute_transfer(self, from_account_number, partial_to_account_number, amount):
        """
        Executes a 'transfer' transaction.
        :param from_account_number: Account number of source account
        :param partial_to_account_number: Partial account number of destination account
        :param amount: Amount to transfer
        """
        if not self.accounts.is_account_valid(from_account_number):
            print(f"ERROR: Source account {from_account_number} not found.")
            return

        from_account = self.accounts.accounts[from_account_number]
        account_holder_name = from_account["holder_name"]

        # Find destination account
        to_account_number = None
        for account_number, account_data in self.accounts.accounts.items():
            if (
                account_data["holder_name"] == account_holder_name
                and account_number[:2] == partial_to_account_number
                and account_number != from_account_number
            ):
                to_account_number = account_number
                break

        if not to_account_number:
            print("ERROR: Destination account not found.")
            return
        if not self.accounts.is_account_valid(to_account_number):
            return
        if not self.accounts.are_funds_sufficient(
            from_account_number, from_account["balance"], amount
        ):
            return

        self.accounts.accounts[from_account_number]["balance"] -= amount
        self.accounts.accounts[to_account_number]["balance"] += amount
        self.accounts.accounts[from_account_number]["num_transactions"] += 1

    def execute_pay_bill(self, account_number, amount):
        """
        Executes a 'pay bill' transaction.
        :param account_number: Account number
        :param amount: Amount to withdraw
        """
        self.execute_withdrawal(account_number, amount)

    def execute_create_account(
        self, account_holder_name, account_number, initial_balance
    ):
        """
        Executes a 'create account' transaction.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param initial_balance: Initial account balance
        """
        if account_number in self.accounts.accounts:
            print(f"ERROR: Account {account_number} already exists.")
            return

        self.accounts.accounts[account_number] = {
            "holder_name": account_holder_name,
            "status": "A",
            "balance": initial_balance,
            "num_transactions": 0,
            "plan": "SP",
        }

    def execute_delete_account(self, account_number):
        """
        Executes a 'delete account' transaction.
        :param account_number: Account number
        """
        if not self.accounts.is_account_valid(account_number):
            return

        del self.accounts.accounts[account_number]

    def execute_disable_account(self, account_number):
        """
        Executes a 'disable account' transaction.
        :param account_number: Account number
        """
        if not self.accounts.is_account_valid(account_number):
            return

        self.accounts.accounts[account_number]["status"] = "D"

    def execute_change_account_plan(self, account_number, new_account_plan):
        """
        Executes a 'change account plan' transaction.
        :param account_number: Account number
        :param new_account_plan: New account plan value
        """
        if not self.accounts.is_account_valid(account_number):
            return

        self.accounts.accounts[account_number]["plan"] = new_account_plan
        self.accounts.accounts[account_number]["num_transactions"] += 1
