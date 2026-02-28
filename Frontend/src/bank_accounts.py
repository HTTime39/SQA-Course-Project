import random


class BankAccounts:
    """
    Manages bank accounts loaded from the input file.
    Allows for account validation, status checks, balance retrieval,
    and account number generation.
    """

    def __init__(self):
        """
        Constructs a BankAccounts object.
        """
        self.accounts = []

    def load_accounts(self, filename):
        """
        Loads bank account records from the input file.
        Stops reading when the END_OF_FILE record is reached.
        :param filename: Path to the input file
        """
        self.accounts = []
        try:
            with open(filename, "r") as file:
                for record in file:
                    record = record.rstrip("\n")
                    account_number = record[0:5]
                    account_holder_name = record[6:26].rstrip(" ")
                    account_status = record[27]
                    account_balance = record[29:37]

                    if account_holder_name == "END OF FILE":
                        break

                    account = {
                        "number": account_number,
                        "holder_name": account_holder_name,
                        "status": account_status,
                        "balance": account_balance,
                    }

                    self.accounts.append(account)

        except FileNotFoundError:
            self.accounts = []

    def account_exists(self, account_holder_name, account_number):
        """
        Checks whether an account exists with the provided holder name
        and account number.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :return: True if the account exists, False otherwise
        """
        account_holder_name = account_holder_name.lower()
        for account in self.accounts:
            if (
                account["holder_name"].lower() == account_holder_name
                and account["number"] == account_number
            ):
                return True
        return False

    def is_account_active(self, account_number):
        """
        Checks whether the account with the provided account number is active.
        :param account_number: Account number
        :return: True if the account is active, False otherwise
        """
        for account in self.accounts:
            if account["number"] == account_number:
                return account["status"] == "A"
        return False

    def get_account_balance(self, account_number):
        """
        Retrieves the balance of the account with the provided account number.
        :param account_number: Account number
        :return: Account balance as a string, or None if not found
        """
        for account in self.accounts:
            if account["number"] == account_number:
                return account["balance"]
        return None

    def generate_account_number(self):
        """
        Generates a unique 5-digit account number for new accounts, sequentially.
        :return: A unique 5-digit account number string
        """
        if not self.accounts:
            return "00001"

        existing_numbers = [
            int(account["number"])
            for account in self.accounts
            if account["number"].isdigit()
        ]

        next_number = max(existing_numbers) + 1
        return f"{next_number:05d}"
