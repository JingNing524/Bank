import unittest
from banking import BankAccount, BankingSystem

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        # Create test accounts in memory, don't touch actual file
        self.system = BankingSystem()
        self.system.accounts = {}
        self.account1 = BankAccount("alice", "pass1234", 100.0)
        self.account2 = BankAccount("bob", "secure456", 50.0)
        self.system.accounts["alice"] = self.account1
        self.system.accounts["bob"] = self.account2

    def test_account_creation(self):
        acc = BankAccount("charlie", "mypassword", 200.0)
        self.assertEqual(acc.username, "charlie")
        self.assertEqual(acc.password, "mypassword")
        self.assertAlmostEqual(acc.from_twos_complement(), 200.0)

    def test_successful_login(self):
        account = self.system.accounts.get("alice")
        self.assertIsNotNone(account)
        self.assertEqual(account.password, "pass1234")

    def test_failed_login(self):
        account = self.system.accounts.get("notexist")
        self.assertIsNone(account)

    def test_deposit(self):
        self.account1.deposit(50.25)
        self.assertAlmostEqual(self.account1.from_twos_complement(), 150.25)

    def test_withdraw_success(self):
        result = self.account1.withdraw(40)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account1.from_twos_complement(), 60.0)

    def test_withdraw_overdraft_limit(self):
        result = self.account1.withdraw(2000)  # Over £1500 overdraft
        self.assertFalse(result)
        self.assertAlmostEqual(self.account1.from_twos_complement(), 100.0)  # No change

    def test_transfer_success(self):
        result = self.account1.transfer(30.0, self.account2)
        self.assertTrue(result)
        self.assertAlmostEqual(self.account1.from_twos_complement(), 70.0)
        self.assertAlmostEqual(self.account2.from_twos_complement(), 80.0)

    def test_transfer_failure(self):
        result = self.account1.transfer(2000.0, self.account2)  # Over overdraft
        self.assertFalse(result)
        self.assertAlmostEqual(self.account1.from_twos_complement(), 100.0)
        self.assertAlmostEqual(self.account2.from_twos_complement(), 50.0)

    def test_twos_complement_round_trip(self):
        for original in [-1500, -1, 0, 1, 1234, 99999]:
            acc = BankAccount("test", "pw", original, already_in_pennies=False)
            restored = acc.from_twos_complement()
            self.assertAlmostEqual(restored, original)

if __name__ == '__main__':
    unittest.main()
