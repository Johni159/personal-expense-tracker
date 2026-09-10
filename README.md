# Personal Expense Tracker 💰

A Python console application for recording, analyzing and visualizing personal expenses.

## Features

- Add expenses with amount, category and date.
- Edit and delete expense records.
- Store data locally in JSON format.
- View expenses in formatted tables.
- Analyze spending by category.
- Generate monthly reports.
- Filter expenses by category and date range.
- Export expense data to CSV.
- Visualize monthly spending with charts.
- Validate user input.

## Tech Stack

- Python 3.11+
- JSON
- CSV
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

The application creates `expenses.json` automatically. Local financial data is ignored by Git.

## Testing

```bash
pytest
```

## Planned Improvements

- Monthly budgets and spending limits.
- Separate application, storage and reporting modules.
- More comprehensive unit tests.
- CI quality checks.

## License

This project is available for educational and portfolio purposes.
