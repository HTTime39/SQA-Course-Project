class TransactionRecordParser:
    """
    Parses transaction records.
    """

    def parse_transaction_code(self, transaction_record):
        """
        Parses the transaction code from a transaction record.
        :param transaction_record: Transaction record
        :return: Transaction code
        """
        return transaction_record[0:2]

    def parse_account_holder_name(self, transaction_record):
        """
        Parses the account holder name from a transaction record.
        :param transaction_record: Transaction record
        :return: Account holder name
        """
        return transaction_record[3:23].strip()

    def parse_account_number(self, transaction_record):
        """
        Parses the account number from a transaction record.
        :param transaction_record: Transaction record
        :return: Account number
        """
        return transaction_record[24:29].strip()

    def parse_amount(self, transaction_record):
        """
        Parses the amount from a transaction record.
        :param transaction_record: Transaction record
        :return: Amount
        """
        amount = transaction_record[30:38].strip()
        return float(amount) if amount else 0.0

    def parse_misc_data(self, transaction_record):
        """
        Parses the miscellaneous data from a transaction record.
        :param transaction_record: Transaction record
        :return: Miscellaneous data
        """
        return transaction_record[39:41].strip()
