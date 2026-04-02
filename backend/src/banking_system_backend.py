"""
Banking System Backend

The backend of the program first loads accounts from the 'master bank accounts' file.
Afterwards, it reads transaction records from the 'merged bank account transactions' file.
It then processes and executes transactions based on the transaction records.
Finally, it writes an updated 'master bank accounts' file and 'current bank accounts' file.

Input files:
- master_bank_accounts.txt: Contains all bank accounts.
- merged_bank_account_transactions.txt: Contains all daily bank account transactions.

Output files:
- new_master_bank_accounts.txt: Contains updated bank accounts.
- current_bank_accounts.txt: Contains all active bank accounts.

Instructions:
1. Open the terminal
2. Change the directory to 'backend/src': cd backend/src
3. Run this file:
   python banking_system_backend.py <master_bank_accounts_file> <merged_bank_account_transactions_file>
   <new_master_bank_accounts_file> <current_bank_accounts_file>
"""

from bank_accounts import BankAccounts
from transaction_file_reader import TransactionFileReader
from transaction_processor import TransactionProcessor
from account_file_writer import AccountFileWriter
import sys


class BankingSystemBackend:
    """
    Main class for the banking system back-end.
    Coordinates loading bank accounts, processing transactions, and writing output files.
    """

    def __init__(
        self,
        master_bank_accounts_file,
        merged_bank_account_transactions_file,
        new_master_bank_accounts_file,
        current_bank_accounts_file,
    ):
        """
        Constructs a BankingSystemBackend object.
        :param master_bank_accounts_file: 'Master bank accounts' file path
        :param merged_bank_account_transactions_file: 'Merged bank account transactions' file path
        :param new_master_bank_accounts_file: 'New master bank accounts' file path
        :param current_bank_accounts_file: 'Current bank accounts' file path
        """
        self.master_bank_accounts_file = master_bank_accounts_file
        self.merged_bank_account_transactions_file = (
            merged_bank_account_transactions_file
        )
        self.new_master_bank_accounts_file = new_master_bank_accounts_file
        self.current_bank_accounts_file = current_bank_accounts_file
        self.accounts = BankAccounts()

    def run(self):
        """
        Runs backend jobs.
        """
        self.load_accounts()
        self.process_transactions()
        self.write_new_account_files()

    def load_accounts(self):
        """
        Loads bank accounts.
        """
        self.accounts.load_accounts(self.master_bank_accounts_file)

    def process_transactions(self):
        """
        Processes transactions.
        """
        reader = TransactionFileReader(self.merged_bank_account_transactions_file)
        processor = TransactionProcessor(self.accounts)

        transaction_records = reader.read_transaction_records()
        for transaction_record in transaction_records:
            if transaction_record.startswith("00"):
                continue

            processor.process_transaction(transaction_record)

    def write_new_account_files(self):
        """
        Writes output files.
        """
        writer = AccountFileWriter()
        accounts = self.accounts.get_all_accounts()

        writer.write_new_master_bank_accounts_file(
            accounts, self.new_master_bank_accounts_file
        )
        writer.write_current_bank_accounts_file(
            accounts, self.current_bank_accounts_file
        )


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python banking_system_backend.py "
            "<master_bank_accounts_file> "
            "<merged_bank_account_transactions_file> "
            "<new_master_bank_accounts_file> "
            "<current_bank_accounts_file>"
        )
        sys.exit(1)

    master_bank_accounts_file = sys.argv[1]
    merged_bank_account_transactions_file = sys.argv[2]
    new_master_bank_accounts_file = sys.argv[3]
    current_bank_accounts_file = sys.argv[4]

    backend = BankingSystemBackend(
        master_bank_accounts_file,
        merged_bank_account_transactions_file,
        new_master_bank_accounts_file,
        current_bank_accounts_file,
    )
    backend.run()
