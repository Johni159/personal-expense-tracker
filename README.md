# Personal Expense Tracker 💰

A Python console application for recording, analyzing and visualizing personal expenses.

## Features

- Add expenses with amount, category and date.
- Store data locally in JSON format.
- Display all recorded expenses in a formatted table.
- Analyze spending by category.
- Generate a report for the current month.
- Visualize monthly spending with pie and bar charts.
- Validate amounts, categories and dates.

## Tech Stack

- Python 3.11+
- JSON
- pathlib
- tabulate
- Matplotlib
- pytest

## Installation

```bash
git clone https://github.com/Johni159/Proj.git
cd Proj
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python expenses.py
```

The application creates `expenses.json` automatically when the first expense is saved. Local expense data is ignored by Git.

## Usage

The main menu provides:

1. Add an expense
2. View all expenses
3. Analyze expenses by category
4. Generate a monthly report
5. Display expense charts
6. Exit

Example data:

```text
Date        Category       Amount
2026-09-01  Food           250.00
2026-09-02  Transport       80.00
2026-09-03  Entertainment  300.00
```

## Testing

```bash
pytest
```

## Planned Improvements

- Edit and delete expenses.
- Date-range filtering.
- CSV export.
- Monthly budgets and spending limits.
- Separate application, storage and reporting modules.
- More unit tests and CI checks.

## License

This project is available for educational and portfolio purposes.
