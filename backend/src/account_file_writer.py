from account_record_builder import AccountRecordBuilder


class AccountFileWriter:
    """
    Handles writing accounts to the output file.
    """
    def __init__(self):
        pass

    def write_new_master_bank_accounts_file(self, accounts, new_master_bank_accounts_file):
        """
        Writes the collection of updated account records to the ‘new master bank accounts’ file using formatted account records.
        """
        with open(new_master_bank_accounts_file, "w") as file:
            file.write(accounts + "\n")

    def write_current_bank_accounts_file(self, accounts, current_bank_accounts_file):
        """
        Writes the collection of active account records to the ‘current bank accounts’ file to be used by future front-end sessions.
        """
        with open(current_bank_accounts_file, "a") as file:
            file.write(accounts + "\n")
