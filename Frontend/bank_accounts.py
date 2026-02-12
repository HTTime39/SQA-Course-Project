import os

class BankAccounts:

  def __init__(self):
    self.accounts = {} # dictionary of accounts

  def load_accounts(self, filename):

    # Get current directory
    base = os.path.dirname(__file__)
    path = os.path.join(base, filename)


    with open(path, 'r') as file: # read through bank account file

      for line in file:

        line = line.rstrip('\n')

        name_field = line[6:26].strip()
        if name_field == 'END_OF_FILE': break

        # assign attributes based on account structure
        account_number = line[0:5]
        account_holder_name = name_field
        status = line[27]
        
        balance_string = line[30:38]
        # convert balance to double if valid
        try: 
          balance = float(balance_string) 
        except ValueError: 
          balance = 0.0 

        # dict is updated with scanned information
        self.accounts[account_number] = {

          'name': account_holder_name,
          'status': status,
          'balance': balance,
          'plan': None

        }
  
  def account_exists(self, account_holder_name, account_number):
    
    # check if account number is valid index
    if account_number not in self.accounts: return False

    # check if name on account corresponds to given name
    return self.accounts[account_number]['name'] == account_holder_name
  
  def is_account_active(self, account_number):
    
    # check if account number is valid index
    if account_number not in self.accounts: return False

    # check if status is active
    return self.accounts[account_number]['status'] == 'A'
  
  def get_account_balance(self, account_number):
    
    # check if account number is valid index
    if account_number not in self.accounts: return False

    # return balance
    return self.accounts[account_number]['balance']
  
  def get_account_plan(self, account_number):
    
    # check if account number is valid index
    if account_number not in self.accounts: return False

    # return plan
    return self.accounts[account_number]['plan']