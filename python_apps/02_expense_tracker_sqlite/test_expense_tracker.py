import unittest

from expense_tracker import get_connection, add_expense, list_expenses, delete_expense, monthly_report


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(":memory:")

    def test_add_and_list(self):
        add_expense(self.conn, 42.5, "groceries", "2026-01-15")
        add_expense(self.conn, 15.0, "transport", "2026-01-16")
        rows = list_expenses(self.conn)
        self.assertEqual(len(rows), 2)

    def test_filter_by_category(self):
        add_expense(self.conn, 10.0, "food", "2026-01-01")
        add_expense(self.conn, 20.0, "transport", "2026-01-02")
        rows = list_expenses(self.conn, category="food")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][2], "food")

    def test_delete(self):
        expense_id = add_expense(self.conn, 5.0, "misc", "2026-01-01")
        self.assertTrue(delete_expense(self.conn, expense_id))
        self.assertFalse(delete_expense(self.conn, expense_id))  # already gone
        self.assertEqual(len(list_expenses(self.conn)), 0)

    def test_monthly_report(self):
        add_expense(self.conn, 30.0, "food", "2026-02-01")
        add_expense(self.conn, 20.0, "food", "2026-02-05")
        add_expense(self.conn, 50.0, "rent", "2026-02-01")
        add_expense(self.conn, 99.0, "food", "2026-03-01")  # different month, excluded

        rows, total = monthly_report(self.conn, "2026-02")
        self.assertEqual(total, 100.0)
        categories = {row[0]: row[1] for row in rows}
        self.assertEqual(categories["food"], 50.0)
        self.assertEqual(categories["rent"], 50.0)


if __name__ == "__main__":
    unittest.main()
