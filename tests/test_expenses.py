import json

import expenses


def test_validate_expense():
    assert expenses.validate_expense(100, "Food", "2026-09-10")
    assert not expenses.validate_expense(0, "Food", "2026-09-10")
    assert not expenses.validate_expense(100, "", "2026-09-10")
    assert not expenses.validate_expense(100, "Food", "10-09-2026")


def test_add_expense(monkeypatch, tmp_path):
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(expenses, "DATA_FILE", data_file)

    items = []
    assert expenses.add_expense(items, 150.50, "Food", "2026-09-10")
    assert items == [{"amount": 150.50, "category": "Food", "date": "2026-09-10"}]

    with data_file.open(encoding="utf-8") as file:
        assert json.load(file) == items


def test_filter_logic():
    items = [
        {"amount": 100, "category": "Food", "date": "2026-09-01"},
        {"amount": 200, "category": "Transport", "date": "2026-09-10"},
        {"amount": 300, "category": "Food", "date": "2026-09-20"},
    ]
    result = [
        item for item in items
        if item["category"].lower() == "food"
        and "2026-09-05" <= item["date"] <= "2026-09-25"
    ]
    assert len(result) == 1
    assert result[0]["amount"] == 300


def test_monthly_report(monkeypatch):
    class FixedDateTime:
        @classmethod
        def now(cls):
            from datetime import datetime
            return datetime(2026, 9, 10)

    monkeypatch.setattr(expenses, "datetime", FixedDateTime)
    items = [
        {"amount": 100, "category": "Food", "date": "2026-09-01"},
        {"amount": 200, "category": "Transport", "date": "2026-09-10"},
        {"amount": 50, "category": "Food", "date": "2026-08-20"},
    ]
    assert expenses.monthly_report(items) == 300


def test_export_csv(monkeypatch, tmp_path):
    export_file = tmp_path / "export.csv"
    monkeypatch.setattr(expenses, "EXPORT_FILE", export_file)
    items = [{"amount": 100, "category": "Food", "date": "2026-09-10"}]

    assert expenses.export_csv(items)
    content = export_file.read_text(encoding="utf-8-sig")
    assert "date,category,amount" in content
    assert "2026-09-10,Food,100" in content
