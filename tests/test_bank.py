import unittest
from decimal import Decimal
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from modern_bank import FixedDepositAccount

class TestFinancialMigration(unittest.TestCase):
    def test_standard_deposit(self):
        # 1000 at 5% for 2 years
        # Year 1: 1050
        # Year 2: 1102.50
        # Interest: 102.50
        fd = FixedDepositAccount(1000, 5, 2)
        self.assertEqual(fd.calculate_interest(), Decimal("102.50"))

    def test_precision_integrity(self):
        # 10000 at 3.5% for 5 years
        fd = FixedDepositAccount(10000, 3.5, 5)
        # Expected: 10000 * (1.035)^5 = 11876.863.. -> 11876.86
        # Interest: 1876.86
        self.assertEqual(fd.calculate_interest(), Decimal("1876.86"))

    def test_negative_safeguards(self):
        # Modern systems must catch errors that legacy COBOL might have missed or handled poorly
        with self.assertRaises(ValueError):
            FixedDepositAccount(-100, 5, 1).calculate_interest()

if __name__ == '__main__':
    unittest.main()
