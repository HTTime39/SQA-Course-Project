class TransactionRecordParser:

    def parse_transaction_code(self, transaction_record):
        return transaction_record[0:2].strip() # first two chars are transaction code

    def parse_account_holder_name(self, transaction_record):
        return transaction_record[3:23].strip() # next 20 chars (after _) are name

    def parse_account_number(self, transaction_record):
        return transaction_record[24:29].strip() # next 5 chars (after _) are acc number

    def parse_amount(self, transaction_record):
        
        amount_str = transaction_record[30:38].strip() # next 8 chars (after _) are amount
        try: return float(amount_str) # if valid float
        except ValueError: return 0.0 # otherwise

    def parse_misc_data(self, transaction_record):
        return transaction_record[39:].strip() # last chars are misc
