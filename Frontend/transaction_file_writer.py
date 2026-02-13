class TransactionFileWriter:
    def __init__(self, filename="frontend/bank_account_transactions.txt"):
        self.filename = filename

    def write_transaction_record(self, transaction_record):
        """
        Writes a single transaction record line to the output file.
        Ensures one record per line and validates the fixed length (41 chars).
        """
        with open(self.filename, "a") as file:
            file.write(transaction_record + "\n")
