class BankAccounts:
    """
    Stores bank accounts in memory.
    """

    def __init__(self):
        """
        Constructs a BankAccounts object.
        """
        self.accounts = {}

    def load_accounts(self, master_bank_accounts_file):
        """
        Loads bank account records from the 'master bank accounts' file.
        Stops reading when the END_OF_FILE record is reached.
        :param master_bank_accounts_file: 'Master bank accounts' file path
        """
        with open(master_bank_accounts_file, "r") as file:
            for record in file:
                record = record.rstrip("\n")

                account_number = record[0:5]
                account_holder_name = record[6:26].rstrip(" ")
                account_status = record[27]
                account_balance = float(record[29:37])
                num_transactions = int(record[38:])

                if account_holder_name == "END OF FILE":
                    break

                self.accounts[account_number] = {
                    "holder_name": account_holder_name,
                    "status": account_status,
                    "balance": account_balance,
                    "num_transactions": num_transactions,
                    "plan": "SP",
                }

    def is_account_valid(self, account_number):
        """
        Checks whether an account exists and is not disabled.
        :param account_number: Account number
        :return: True if the account exists or is not disabled, False otherwise
        """
        if account_number not in self.accounts:
            print(f"ERROR: Account {account_number} does not exist.")
            return False

        if self.accounts[account_number]["status"] == "D":
            print(f"ERROR: Account {account_number} is disabled.")
            return False

        return True

    def are_funds_sufficient(self, account_number, account_balance, amount):
        """
        Checks whether an account has sufficient funds for a withdrawal.
        :param account_number: Account number
        :param account_balance: Account balance
        :param amount: Amount to withdraw
        :return: True if the account has sufficient funds, False otherwise
        """
        if account_balance < amount:
            print(f"ERROR: Account {account_number} has insufficient funds.")
            return False

        return True

    def apply_transaction_fee(self, account_number):
        """
        Applies a transaction fee to an account based on its plan.
        :param account_number: Account number
        """
        account_plan = self.accounts[account_number]["plan"]

        if account_plan == "SP":
            transaction_fee = 0.05
        else:
            transaction_fee = 0.10

        if self.accounts[account_number]["balance"] - transaction_fee >= 0:
            self.accounts[account_number]["balance"] -= transaction_fee

    def get_all_accounts(self):
        """
        Provides all accounts.
        :return: Accounts
        """
        return self.accounts
