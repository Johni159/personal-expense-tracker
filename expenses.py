import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tabulate import tabulate
import matplotlib.pyplot as plt

DATA_FILE = Path("expenses.json")
MONTHS_UA = {
    1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
    5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
    9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень",
}


def load_expenses():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d")


def add_expense(expenses, amount=None, category=None, date_str=None):
    if amount is None:
        try:
            amount = float(input("Сума: ").replace(",", "."))
        except ValueError:
            print("Некоректна сума.")
            return False
    if amount <= 0:
        print("Сума має бути більше нуля.")
        return False

    if category is None:
        category = input("Категорія: ").strip()
    if not category:
        print("Категорія не може бути порожньою.")
        return False

    if date_str is None:
        date_str = input("Дата (YYYY-MM-DD, Enter = сьогодні): ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
    try:
        parse_date(date_str)
    except ValueError:
        print("Некоректний формат дати.")
        return False

    expenses.append({"amount": float(amount), "category": category, "date": date_str})
    save_expenses(expenses)
    print("Запис додано.")
    return True


def show_expenses(expenses):
    if not expenses:
        print("Записів поки немає.")
        return
    rows = [[i, x["date"], x["category"], f"{x['amount']:.2f}"] for i, x in enumerate(expenses, 1)]
    print("\n--- Список витрат ---")
    print(tabulate(rows, headers=["№", "Дата", "Категорія", "Сума (грн)"], tablefmt="pretty"))
    print(f"Загалом: {sum(x['amount'] for x in expenses):.2f} грн\n")


def edit_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("Номер запису для редагування: ")) - 1
        item = expenses[index]
    except (ValueError, IndexError):
        print("Некоректний номер.")
        return

    amount = input(f"Сума [{item['amount']}]: ").strip()
    category = input(f"Категорія [{item['category']}]: ").strip()
    date_str = input(f"Дата [{item['date']}]: ").strip()

    if amount:
        try:
            amount_value = float(amount.replace(",", "."))
            if amount_value <= 0:
                raise ValueError
            item["amount"] = amount_value
        except ValueError:
            print("Некоректна сума.")
            return
    if category:
        item["category"] = category
    if date_str:
        try:
            parse_date(date_str)
            item["date"] = date_str
        except ValueError:
            print("Некоректна дата.")
            return
    save_expenses(expenses)
    print("Запис оновлено.")


def delete_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("Номер запису для видалення: ")) - 1
        expenses.pop(index)
    except (ValueError, IndexError):
        print("Некоректний номер.")
        return
    save_expenses(expenses)
    print("Запис видалено.")


def filter_expenses(expenses):
    if not expenses:
        print("Записів поки немає.")
        return
    category = input("Категорія (Enter = будь-яка): ").strip().lower()
    start = input("Дата від YYYY-MM-DD (Enter = без обмеження): ").strip()
    end = input("Дата до YYYY-MM-DD (Enter = без обмеження): ").strip()
    try:
        start_date = parse_date(start) if start else None
        end_date = parse_date(end) if end else None
    except ValueError:
        print("Некоректна дата.")
        return

    result = []
    for item in expenses:
        try:
            date = parse_date(item["date"])
        except ValueError:
            continue
        if category and item["category"].lower() != category:
            continue
        if start_date and date < start_date:
            continue
        if end_date and date > end_date:
            continue
        result.append(item)
    show_expenses(result)


def analyze_by_category(expenses):
    if not expenses:
        print("Записів поки немає.")
        return
    by_category = defaultdict(float)
    for item in expenses:
        by_category[item["category"]] += item["amount"]
    rows = [[category, f"{amount:.2f}"] for category, amount in sorted(by_category.items())]
    print(tabulate(rows, headers=["Категорія", "Сума (грн)"], tablefmt="pretty"))


def monthly_report(expenses):
    now = datetime.now()
    month_expenses = []
    for item in expenses:
        try:
            date = parse_date(item["date"])
            if date.year == now.year and date.month == now.month:
                month_expenses.append(item)
        except ValueError:
            continue
    if not month_expenses:
        print(f"За {MONTHS_UA[now.month]} {now.year} записів немає.")
        return
    by_category = defaultdict(float)
    for item in month_expenses:
        by_category[item["category"]] += item["amount"]
    total = sum(by_category.values())
    rows = [[category, f"{amount:.2f}"] for category, amount in sorted(by_category.items())]
    print(f"\n--- Звіт за {MONTHS_UA[now.month]} {now.year} ---")
    print(f"Загальна сума: {total:.2f} грн")
    print(tabulate(rows, headers=["Категорія", "Сума (грн)"], tablefmt="pretty"))


def export_csv(expenses):
    if not expenses:
        print("Немає даних для експорту.")
        return
    path = Path("expenses_export.csv")
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Експортовано: {path}")


def show_expenses_chart(expenses):
    if not expenses:
        print("Записів поки немає.")
        return
    by_category = defaultdict(float)
    for item in expenses:
        by_category[item["category"]] += item["amount"]
    categories = list(by_category)
    amounts = list(by_category.values())
    plt.figure(figsize=(9, 5))
    plt.bar(categories, amounts)
    plt.title("Витрати за категоріями")
    plt.ylabel("Сума (грн)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def main():
    expenses = load_expenses()
    while True:
        print("\n=== Облік витрат ===")
        print("1. Додати запис")
        print("2. Переглянути всі записи")
        print("3. Редагувати запис")
        print("4. Видалити запис")
        print("5. Фільтр")
        print("6. Аналіз за категоріями")
        print("7. Звіт за місяць")
        print("8. Графік витрат")
        print("9. Експорт у CSV")
        print("0. Вийти")
        choice = input("Оберіть дію: ").strip()
        if choice == "1": add_expense(expenses)
        elif choice == "2": show_expenses(expenses)
        elif choice == "3": edit_expense(expenses)
        elif choice == "4": delete_expense(expenses)
        elif choice == "5": filter_expenses(expenses)
        elif choice == "6": analyze_by_category(expenses)
        elif choice == "7": monthly_report(expenses)
        elif choice == "8": show_expenses_chart(expenses)
        elif choice == "9": export_csv(expenses)
        elif choice == "0": break
        else: print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
