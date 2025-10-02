# ByteBank Expense Tracker

## Overview
**ByteBank Expense Tracker** is a Python-based desktop application built with the `customtkinter` library, designed to help users manage their finances by tracking income and expenses. The application features a user-friendly interface with a secure login system, a dashboard for managing transactions, and real-time financial summaries. Users can add, update, delete, and view transactions, with data stored persistently in JSON files.

---

## Features

### User Authentication
- Secure login and account creation with password validation.
- User credentials stored in `users.json`.

### Transaction Management
- **Add Transactions:** Record income or expenses with fields: amount, description, category, date, payment method, and notes.
- **Update Transactions:** Modify existing transactions via a dropdown selection.
- **Delete Transactions:** Remove transactions by selecting them from a dropdown.
- **View Reports:** Display a detailed history of all transactions in a scrollable text area.

### Real-Time Summaries
- Dashboard displays current balance, total income, total expenses, and total savings, updated in real-time.

### UI & Persistence
- Modern, clean interface using `customtkinter` with consistent styling.
- Transactions saved per user in `<username>_transactions.json`.
- Robust error handling with user-friendly popup dialogs for success and error feedback.

---

## Prerequisites
- **Python 3.8+** — ensure Python is installed on your system.
- **Required libraries:**
  - `customtkinter` — for the GUI components.
  - `Pillow` (PIL) — for handling profile images/icons.

Optional: A profile image at `images/profile.png` to display in the login/dashboard UI. The app runs without it and handles missing images gracefully.

---

## Installation

1. **Clone the repository**
   git clone https://github.com/Jaganbhasker122/ByteBank-Expensives-Tracker.git
   cd bytebank-expense-tracker

2. **Install dependencies**
   pip install customtkinter Pillow

3. **Run the application**
   python expense_tracker.py

---

## Directory Structure
bytebank-expense-tracker/

├── images/

│   └── profile.png            # optional

├── users.json                 # auto-created on first account creation

├── <username>_transactions.json  # auto-created per user

├── MainApp.py         # main application code

└── README.md

---

## Usage

### Launch the app
python MainApp.py

### Create an account
- On the login screen, click "Don't have an account? Create one now!"
- Enter a username, password, confirm the password, then click Create Account.
- A popup confirms account creation; credentials are saved to `users.json`.

### Log in
- Enter your username and password and click Login.
- Valid credentials open the main dashboard; invalid credentials produce an error popup.

### Dashboard features
- **View Summaries:** See current balance, total income, total expenses, and total savings at the top/right of the dashboard.
- **Add Transaction:** Click ➕ Add Expenses/Income, fill the form (type, amount, description, category, date, payment method, notes) and click Add Record.
- **Update Transaction:** Click ✏️ Update Records, select a transaction from the dropdown, edit fields and click Update Record.
- **Delete Transaction:** Click 🗑 Delete Records, select a transaction from the dropdown and click Delete Record.
- **View Reports:** Click 📑 View Reports to view all transactions in a scrollable area.
- Errors (invalid input, missing data, file I/O issues) trigger clear popup dialogs.

---

## Data Storage

- **Credentials:** Stored in `users.json`.  
- **Transactions:** Stored per-user in `<username>_transactions.json`. Each transaction contains these fields: `id`, `type`, `amount`, `description`, `category`, `date`, `payment_method`, `notes`.

### Example transaction file (`<username>_transactions.json`)
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "Expense",
        "amount": 50.0,
        "description": "Lunch",
        "category": "Food",
        "date": "2025-10-02",
        "payment_method": "Cash",
        "notes": "Lunch at cafe"
    },
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "type": "Income",
        "amount": 1000.0,
        "description": "Salary",
        "category": "Salary",
        "date": "2025-10-01",
        "payment_method": "Bank Transfer",
        "notes": "Monthly salary"
    }
]

---

## File Descriptions
- `expense_tracker.py` — Main application code (contains `LoginPage`, `MainDashboard`, and `Operations` classes).
- `users.json` — Stores user credentials (auto-created).
- `<username>_transactions.json` — Stores transactions for each user (auto-created).
- `images/profile.png` — Optional profile icon.

---

## Development Notes

**Libraries Used**
- `customtkinter` — modern UI components.
- `Pillow` — image loading/processing.
- Standard libs: `json`, `os`, `uuid`, `datetime` for data handling.

**Error Handling**
- All major operations (login, account creation, add/update/delete/view transactions) are wrapped in `try-except` blocks to handle file I/O errors, invalid inputs, and other exceptions. User-friendly popup dialogs inform the user of success or failure.

**UI Consistency**
- A `CONFIG` dictionary centralizes colors, fonts, and sizes to keep the UI consistent across the app.

**Data Persistence**
- JSON files are used for simplicity, portability, and easy debugging — suitable for desktop use.

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch:
   git checkout -b feature/your-feature
3. Make changes and test thoroughly.
4. Commit your changes:
   git commit -m "Add your feature"
5. Push to your branch:
   git push origin feature/your-feature
6. Open a pull request describing your changes.

**Guidelines**
- Follow PEP 8 style guidelines.
- Include proper error handling and dialog feedback for new features.
- Preserve UI theme and `CONFIG` settings for consistency.

---

## License
This project is Open-Souce. Anyone can contribute 😉

---
