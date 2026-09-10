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
    result = [x for x in expenses if x["category"].lower() == "food"]
    assert len(result) == 1
    assert result[0]["amount"] == 100


def test_date_range_filter_logic():
    expenses = [
        {"amount": 100, "category": "Food", "date": "2026-09-01"},
        {"amount": 200, "category": "Food", "date": "2026-09-10"},
        {"amount": 300, "category": "Food", "date": "2026-09-20"},
    ]
    start = datetime.strptime("2026-09-05", "%Y-%m-%d")
    end = datetime.strptime("2026-09-15", "%Y-%m-%d")
    result = [
        x for x in expenses
        if start <= datetime.strptime(x["date"], "%Y-%m-%d") <= end
    ]
    assert len(result) == 1
    assert result[0]["amount"] == 200
