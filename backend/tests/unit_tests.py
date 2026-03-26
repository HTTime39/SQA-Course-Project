import io
import os
import sys
import unittest
from contextlib import redirect_stdout

# Directory configuration
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_SRC = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if BACKEND_SRC not in sys.path:
    sys.path.insert(0, BACKEND_SRC)

from bank_accounts import BankAccounts
from transaction_executor import TransactionExecutor


class AreFundsSufficientStatementCoverageTest(unittest.TestCase):
    """
    Unit tests for statement coverage of the 'are_funds_sufficient' method in BankAccounts.
    """

    def setUp(self):
        """
        Constructs a BankAccounts object.
        """
        self.accounts = BankAccounts()

    def test_sc01_insufficient_funds_error(self):
        pass

    def test_sc02_sufficient_funds(self):
        pass


class ExecuteTransferDecisionAndLoopCoverageTest(unittest.TestCase):
    """
    Unit tests for decision and loop coverage of the 'execute_transfer' method in TransactionExecutor.
    """

    def setUp(self):
        """
        Constructs BankAccounts and TransactionExecutor objects.
        """
        self.accounts = BankAccounts()
        self.executor = TransactionExecutor(self.accounts)

    def test_dlc01_invalid_source_account(self):
        pass

    def test_dlc02_one_loop_iteration_no_match(self):
        pass

    def test_dlc03_two_loop_iterations_match(self):
        pass

    def test_dlc04_disabled_destination_account(self):
        pass

    def test_dlc05_insufficient_funds(self):
        """
        DLC05_Insufficient_Funds

        The destination account is found, but the source account has insufficient funds.
        """
        self.accounts.accounts = {
            "12345": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 25.00,
                "num_transactions": 0,
                "plan": "SP",
            },
            "54321": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
        }

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.executor.execute_transfer("12345", "54", 50.00)

        self.assertIn(
            "ERROR: Account 12345 has insufficient funds.", captured_output.getvalue()
        )
        self.assertEqual(self.accounts.accounts["12345"]["balance"], 25.00)
        self.assertEqual(self.accounts.accounts["54321"]["balance"], 100.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 0)

    def test_dlc06_multiple_loop_iterations(self):
        """
        DLC06_Multiple_Loop_Iterations

        Multiple accounts appear before the destination account is found.
        """
        self.accounts.accounts = {
            "12345": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 300.00,
                "num_transactions": 0,
                "plan": "SP",
            },
            "11111": {
                "holder_name": "Jane Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
            "22222": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
            "54321": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
        }

        self.executor.execute_transfer("12345", "54", 75.00)

        self.assertEqual(self.accounts.accounts["12345"]["balance"], 225.00)
        self.assertEqual(self.accounts.accounts["54321"]["balance"], 175.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 1)
        self.assertEqual(self.accounts.accounts["22222"]["balance"], 100.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
