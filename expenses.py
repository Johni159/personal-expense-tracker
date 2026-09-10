import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tabulate import tabulate
import matplotlib.pyplot as plt

DATA_FILE = Path("expenses.json")
EXPORT_FILE = Path("expenses_export.csv")
DATE_FORMAT = "%Y-%m-%d"
MONTHS_UA = {
    1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
    5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
    9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень",
}


def parse_date(value):
    return datetime.strptime(value, DATE_FORMAT)


def validate_expense(amount, category, date_str):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return False
    if amount <= 0 or not str(category).strip():
        return False
    try:
        parse_date(date_str)
    except (TypeError, ValueError):
        return False
    return True


def load_expenses():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    return data


def save_expenses(expenses):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)


def add_expense(expenses, amount=None, category=None, date_str=None):
    if amount is None:
        try:
            amount = float(input("Сума: ").replace(",", "."))
        except ValueError:
            print("Некоректна сума.")
            return False

    if category is None:
        category = input("Категорія: ").strip()

    if date_str is None:
        date_str = input("Дата (YYYY-MM-DD, Enter = сьогодні): ").strip()
        date_str = date_str or datetime.now().strftime(DATE_FORMAT)

    if not validate_expense(amount, category, date_str):
        print("Некоректні дані витрати.")
        return False

    expenses.append({
        "amount": float(amount),
        "category": str(category).strip(),
        "date": date_str,
    })
    save_expenses(expenses)
    print("Запис додано.")
    return True


def show_expenses(expenses):
    if not expenses:
        print("Записів поки немає.")
        return
    rows = [
        [i, item["date"], item["category"], f"{item['amount']:.2f}"]
        for i, item in enumerate(expenses, 1)
    ]
    print("\n--- Список витрат ---")
    print(tabulate(rows, headers=["№", "Дата", "Категорія", "Сума (грн)"], tablefmt="pretty"))
    print(f"Загалом: {sum(item['amount'] for item in expenses):.2f} грн\n")


def edit_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return False
    try:
        index = int(input("Номер запису для редагування: ")) - 1
        item = expenses[index]
    except (ValueError, IndexError):
        print("Некоректний номер.")
        return False

    amount = input(f"Сума [{item['amount']}]: ").strip()
    category = input(f"Категорія [{item['category']}]: ").strip()
    date_str = input(f"Дата [{item['date']}]: ").strip()

    new_amount = float(amount.replace(",", ".")) if amount else item["amount"]
    new_category = category or item["category"]
    new_date = date_str or item["date"]

    if not validate_expense(new_amount, new_category, new_date):
        print("Некоректні дані витрати.")
        return False

    item.update(amount=float(new_amount), category=new_category, date=new_date)
    save_expenses(expenses)
    print("Запис оновлено.")
    return True


def delete_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return False
    try:
        index = int(input("Номер запису для видалення: ")) - 1
        expenses.pop(index)
    except (ValueError, IndexError):
        print("Некоректний номер.")
        return False
    save_expenses(expenses)
    print("Запис видалено.")
    return True


def filter_expenses(expenses):
    if not expenses:
        print("Записів поки немає.")
        return []

    category = input("Категорія (Enter = будь-яка): ").strip().lower()
    start = input("Дата від YYYY-MM-DD (Enter = без обмеження): ").strip()
    end = input("Дата до YYYY-MM-DD (Enter = без обмеження): ").strip()

    try:
        start_date = parse_date(start) if start else None
        end_date = parse_date(end) if end else None
    except ValueError:
        print("Некоректна дата.")
        return []

    if start_date and end_date and start_date > end_date:
        print("Початкова дата не може бути пізніше кінцевої.")
        return []

    result = []
    for item in expenses:
        try:
            date = parse_date(item["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if category and item.get("category", "").lower() != category:
            continue
        if start_date and date < start_date:
            continue
        if end_date and date > end_date:
            continue
        result.append(item)

    show_expenses(result)
    return result


def analyze_by_category(expenses):
    if not expenses:
        print("Записів поки немає.")
        return {}
    by_category = defaultdict(float)
    for item in expenses:
        by_category[item["category"]] += item["amount"]
    rows = [[category, f"{amount:.2f}"] for category, amount in sorted(by_category.items())]
    print(tabulate(rows, headers=["Категорія", "Сума (грн)"], tablefmt="pretty"))
    return dict(by_category)


def monthly_report(expenses, year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    month_expenses = []

    for item in expenses:
        try:
            date = parse_date(item["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if date.year == year and date.month == month:
            month_expenses.append(item)

    if not month_expenses:
        print(f"За {MONTHS_UA[month]} {year} записів немає.")
        return 0.0

    by_category = defaultdict(float)
    for item in month_expenses:
        by_category[item["category"]] += item["amount"]
    total = sum(by_category.values())
    rows = [[category, f"{amount:.2f}"] for category, amount in sorted(by_category.items())]
    print(f"\n--- Звіт за {MONTHS_UA[month]} {year} ---")
    print(f"Загальна сума: {total:.2f} грн")
    print(tabulate(rows, headers=["Категорія", "Сума (грн)"], tablefmt="pretty"))
    return total


def export_csv(expenses):
    if not expenses:
        print("Немає даних для експорту.")
        return False
    with EXPORT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "category", "amount"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Експортовано: {EXPORT_FILE}")
    return True


def show_expenses_chart(expenses):
    if not expenses:
        print("Записів поки немає.")
        return False
    by_category = defaultdict(float)
    for item in expenses:
        by_category[item["category"]] += item["amount"]
    plt.figure(figsize=(9, 5))
    plt.bar(by_category.keys(), by_category.values())
    plt.title("Витрати за категоріями")
    plt.ylabel("Сума (грн)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    return True


def main():
    expenses = load_expenses()
    actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: show_expenses(expenses),
        "3": lambda: edit_expense(expenses),
        "4": lambda: delete_expense(expenses),
        "5": lambda: filter_expenses(expenses),
        "6": lambda: analyze_by_category(expenses),
        "7": lambda: monthly_report(expenses),
        "8": lambda: show_expenses_chart(expenses),
        "9": lambda: export_csv(expenses),
    }
    while True:
        print("\n=== Облік витрат ===")
        print("1. Додати запис\n2. Переглянути всі записи\n3. Редагувати запис")
        print("4. Видалити запис\n5. Фільтр\n6. Аналіз за категоріями")
        print("7. Звіт за місяць\n8. Графік витрат\n9. Експорт у CSV\n0. Вийти")
        choice = input("Оберіть дію: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except (ValueError, KeyError, TypeError) as exc:
                print(f"Помилка введення: {exc}")
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
