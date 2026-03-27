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
        """
        SC01_Insufficient_Funds_Error

        The condition evaluates to True.
        The method should return False and display an error message.
        """
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = self.accounts.are_funds_sufficient("12345", 100.00, 150.00)

        self.assertFalse(result)
        self.assertIn(
            "ERROR: Account 12345 has insufficient funds.", captured_output.getvalue()
        )

    def test_sc02_sufficient_funds(self):
        """
        SC02_Sufficient_Funds

        The condition evaluates to False.
        The method should return True.
        """
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = self.accounts.are_funds_sufficient("12345", 100.00, 50.00)

        self.assertTrue(result)
        self.assertEqual(captured_output.getvalue(), "")


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
        """
        DLC01_Invalid_Source_Account

        The source account is invalid.
        The method should return before entering the loop.
        """
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.executor.execute_transfer("00000", "54", 50.00)

        self.assertIn(
            "ERROR: Account 00000 does not exist.", captured_output.getvalue()
        )
        self.assertEqual(self.accounts.accounts, {})

    def test_dlc02_one_loop_iteration_no_match(self):
        """
        DLC02_One_Loop_Iteration_No_Match

        Only the source account exists.
        The loop executes once and no destination account is found.
        """
        self.accounts.accounts = {
            "12345": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            }
        }

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.executor.execute_transfer("12345", "54", 50.00)

        self.assertIn(
            "ERROR: Destination account not found.", captured_output.getvalue()
        )
        self.assertEqual(self.accounts.accounts["12345"]["balance"], 100.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 0)

    def test_dlc03_two_loop_iterations_match(self):
        """
        DLC03_Two_Loop_Iterations_Match

        The destination account is found on the second iteration.
        """
        self.accounts.accounts = {
            "12345": {
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

        self.executor.execute_transfer("12345", "54", 50.00)

        self.assertEqual(self.accounts.accounts["12345"]["balance"], 50.00)
        self.assertEqual(self.accounts.accounts["54321"]["balance"], 150.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 1)

    def test_dlc04_disabled_destination_account(self):
        """
        DLC04_Disabled_Destination_Account

        The destination account is found, but disabled.
        """
        self.accounts.accounts = {
            "12345": {
                "holder_name": "John Doe",
                "status": "A",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
            "54321": {
                "holder_name": "John Doe",
                "status": "D",
                "balance": 100.00,
                "num_transactions": 0,
                "plan": "SP",
            },
        }

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.executor.execute_transfer("12345", "54", 50.00)

        self.assertIn("ERROR: Account 54321 is disabled.", captured_output.getvalue())
        self.assertEqual(self.accounts.accounts["12345"]["balance"], 100.00)
        self.assertEqual(self.accounts.accounts["54321"]["balance"], 100.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 0)

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
                "balance": 100.00,
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

        self.executor.execute_transfer("12345", "54", 50.00)

        self.assertEqual(self.accounts.accounts["12345"]["balance"], 50)
        self.assertEqual(self.accounts.accounts["54321"]["balance"], 150.00)
        self.assertEqual(self.accounts.accounts["12345"]["num_transactions"], 1)
        self.assertEqual(self.accounts.accounts["11111"]["balance"], 100.00)
        self.assertEqual(self.accounts.accounts["22222"]["balance"], 100.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
