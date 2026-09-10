from datetime import datetime


def test_expense_data_is_valid():
    expense = {"amount": 150.50, "category": "Food", "date": "2026-09-10"}

    assert expense["amount"] > 0
    assert expense["category"]
    assert datetime.strptime(expense["date"], "%Y-%m-%d")


def test_category_comparison_is_case_insensitive():
    expenses = [
        {"amount": 100, "category": "Food", "date": "2026-09-10"},
        {"amount": 200, "category": "Transport", "date": "2026-09-10"},
    ]

    category = "food"
    matched = [item for item in expenses if item["category"].lower() == category.lower()]

    assert len(matched) == 1
    assert matched[0]["amount"] == 100
