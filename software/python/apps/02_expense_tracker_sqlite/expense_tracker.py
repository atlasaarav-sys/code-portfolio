"""CLI expense tracker backed by SQLite."""

import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "expenses.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT DEFAULT ''
)
"""


def get_connection(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def add_expense(conn, amount, category, date, note=""):
    cur = conn.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note),
    )
    conn.commit()
    return cur.lastrowid


def list_expenses(conn, category=None, month=None):
    query = "SELECT id, amount, category, date, note FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if month:
        query += " AND date LIKE ?"
        params.append(f"{month}%")
    query += " ORDER BY date"
    return conn.execute(query, params).fetchall()


def delete_expense(conn, expense_id):
    cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return cur.rowcount > 0


def monthly_report(conn, month):
    rows = conn.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM expenses WHERE date LIKE ? GROUP BY category ORDER BY SUM(amount) DESC",
        (f"{month}%",),
    ).fetchall()
    total = sum(r[1] for r in rows)
    return rows, total


def cmd_add(args, conn):
    expense_id = add_expense(conn, args.amount, args.category, args.date, args.note or "")
    print(f"Added expense #{expense_id}: ${args.amount:.2f} ({args.category}) on {args.date}")


def cmd_list(args, conn):
    rows = list_expenses(conn, category=args.category, month=args.month)
    if not rows:
        print("No expenses found.")
        return
    for id_, amount, category, date, note in rows:
        note_str = f" — {note}" if note else ""
        print(f"#{id_}  {date}  ${amount:>8.2f}  {category}{note_str}")


def cmd_report(args, conn):
    rows, total = monthly_report(conn, args.month)
    if not rows:
        print(f"No expenses for {args.month}.")
        return
    print(f"Report for {args.month}:")
    for category, amount, count in rows:
        pct = amount / total * 100 if total else 0
        print(f"  {category:<15} ${amount:>8.2f}  ({count} entries, {pct:.1f}%)")
    print(f"  {'TOTAL':<15} ${total:>8.2f}")


def cmd_delete(args, conn):
    if delete_expense(conn, args.id):
        print(f"Deleted expense #{args.id}")
    else:
        print(f"No expense with id {args.id}")


def build_parser():
    parser = argparse.ArgumentParser(description="Expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category")
    p_add.add_argument("--date", required=True, help="YYYY-MM-DD")
    p_add.add_argument("--note")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list")
    p_list.add_argument("--category")
    p_list.add_argument("--month", help="YYYY-MM")
    p_list.set_defaults(func=cmd_list)

    p_report = sub.add_parser("report")
    p_report.add_argument("--month", required=True, help="YYYY-MM")
    p_report.set_defaults(func=cmd_report)

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    conn = get_connection()
    args.func(args, conn)
    conn.close()


if __name__ == "__main__":
    main()
