import sys
class TransactionFileReader:

    def __init__(self, merged_bank_account_transactions_file):
        self.merged_bank_account_transactions_file = merged_bank_account_transactions_file

    def read_transaction_records(self):
        
        transaction_records = []

        try:

            with open(self.merged_bank_account_transactions_file, 'r') as file:

                for line in file:

                    record = line.strip('\n') # get transaction record
                    if len(record) != 40: # If not of appropriate length
                        print(f"ERROR: Bad input length in file '{self.merged_bank_account_transactions_file}'")
                        sys.exit(1)
                    transaction_records.append(record)

        except FileNotFoundError: # if not found

            print(f"ERROR: Transaction file '{self.merged_bank_account_transactions_file}' was not found")
            sys.exit(1)

        return transaction_records
