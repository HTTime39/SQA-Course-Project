class TransactionFileWriter:
    """
    Handles writing transaction records to the output file.
    """

    def __init__(self, filename="frontend/bank_account_transactions.txt"):
        """
        Constructs a TransactionFileWriter object.
        :param filename: Path to the output file
        """
        self.filename = filename

    def write_transaction_record(self, transaction_record):
        """
        Appends a single formatted transaction record to the output file.
        :param transaction_record: Formatted transaction record string
        """
        with open(self.filename, "a") as file:
            file.write(transaction_record + "\n")
