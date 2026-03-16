from account_record_builder import AccountRecordBuilder


class AccountFileWriter:
    """
    Writes new account data to output files.
    """

    def __init__(self):
        """
        Constructs a AccountFileWriter object.
        """
        self.builder = AccountRecordBuilder()

    def write_new_master_bank_accounts_file(
        self, accounts, new_master_bank_accounts_file
    ):
        """
        Writes the 'new master bank accounts' file.
        :param accounts: BankAccounts object.
        :param new_master_bank_accounts_file: 'New master bank accounts' file path
        """
        with open(new_master_bank_accounts_file, "w") as file:
            for account_number, account_data in sorted(accounts.items()):
                account_record = self.builder.build_account_record(
                    "new_master_bank_accounts_file", account_number, account_data
                )
                file.write(account_record + "\n")

    def write_current_bank_accounts_file(self, accounts, current_bank_accounts_file):
        """
        Writes the 'current bank accounts' file.
        :param accounts: BankAccounts object.
        :param current_bank_accounts_file: 'Current bank accounts' file path
        """
        with open(current_bank_accounts_file, "w") as file:
            for account_number, account_data in sorted(accounts.items()):
                if account_data["status"] == "A":
                    account_record = self.builder.build_account_record(
                        "current_bank_accounts_file", account_number, account_data
                    )
                    file.write(account_record + "\n")
