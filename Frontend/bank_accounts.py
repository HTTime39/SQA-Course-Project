import random


class BankAccounts:
    def __init__(self):
        self.accounts = []

    def load_accounts(self, filename):
        self.accounts = []
        try:
            with open(filename, "r") as file:  # read through bank account file
                for record in file:
                    record = record.rstrip("\n")
                    account_number = record[0:5]
                    account_holder_name = record[6:26].rstrip("_")
                    account_status = record[27]
                    account_balance = record[29:37]

                    if account_holder_name == "END_OF_FILE":
                        break

                    # assign attributes based on account structure
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
        # check if name on account corresponds to given name
        # check if account number is valid index
        account_holder_name = account_holder_name.replace(" ", "_").lower()
        for account in self.accounts:
            if (
                account["holder_name"].lower() == account_holder_name
                and account["number"] == account_number
            ):
                return True
        return False

    def is_account_active(self, account_number):
        # check if account number is valid index
        # check if status is active
        for account in self.accounts:
            if account["number"] == account_number:
                return account["status"] == "A"
        return False

    def get_account_balance(self, account_number):
        # check if account number is valid index
        for account in self.accounts:
            if account["number"] == account_number:
                return account["balance"]
        return None

    def generate_account_number(self):
        existing_account_numbers = {account["number"] for account in self.accounts}

        while True:
            account_number = f"{random.randint(0, 99999):05d}"
            if account_number not in existing_account_numbers:
                return account_number
