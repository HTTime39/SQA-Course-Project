class TransactionFileReader:
    """
    Handles reading transaction records from the
    'merged bank account transactions' file.
    """

    def __init__(self, merged_bank_account_transactions_file):
        """
        Constructs a TransactionFileReader object.
        :param merged_bank_account_transactions_file: 'Merged bank account transactions' file path
        """
        self.merged_bank_account_transactions_file = (
            merged_bank_account_transactions_file
        )

    def read_transaction_records(self):
        """
        Reads all transaction records from the 'merged bank account transactions' file.
        :return: List of all transaction records
        """
        transaction_records = []

        with open(self.merged_bank_account_transactions_file, "r") as file:
            for line in file:
                line = line.rstrip("\n")
                if line:
                    transaction_records.append(line)

        return transaction_records
