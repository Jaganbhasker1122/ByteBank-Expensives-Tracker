ByteBank Expense Tracker
Overview
ByteBank Expense Tracker is a Python-based desktop application built with the customtkinter library, designed to help users manage their finances by tracking income and expenses. The application features a user-friendly interface with a login system, a dashboard for managing transactions, and real-time financial summaries. Users can add, update, delete, and view transactions, with data stored in JSON files for persistence.
Features

User Authentication: Secure login and account creation with password validation, stored in users.json.
Transaction Management:
Add Transactions: Record income or expenses with details like amount, description, category, date, payment method, and notes.
Update Transactions: Modify existing transaction details.
Delete Transactions: Remove transactions by selecting them from a dropdown.
View Reports: Display a detailed history of all transactions in a readable format.


Real-Time Summaries: Dashboard displays current balance, total income, total expenses, and total savings, updated every second.
Modern UI: Clean, responsive interface using customtkinter with a consistent color scheme and styling.
Data Persistence: Transactions are saved in user-specific JSON files (e.g., <username>_transactions.json).
Error Handling: Robust exception handling with dialog popups for user feedback on errors or successes.

Prerequisites

Python 3.8+: Ensure Python is installed on your system.
Required Libraries:
customtkinter: For the GUI.
Pillow (PIL): For handling profile image icons.


Optional: A profile image (images/profile.png) for the login and dashboard UI (the app will still run without it).

Installation

Clone the Repository:
git clone https://github.com/<your-username>/bytebank-expense-tracker.git
cd bytebank-expense-tracker


Install Dependencies:Install the required Python libraries using pip:
pip install customtkinter Pillow


Directory Structure:Ensure the following structure in your project folder:
bytebank-expense-tracker/
├── images/
│   └── profile.png (optional)
├── users.json (auto-created on first account creation)
├── <username>_transactions.json (auto-created per user)
├── expense_tracker.py (main application code)
└── README.md


Run the Application:Start the application by running:
python expense_tracker.py



Usage

Launch the Application:Run python expense_tracker.py. The login window will appear.

Create an Account:

Click "Don't have an account? Create one now!" on the login screen.
Enter a username and password, confirm the password, and click "Create Account".
A success popup will confirm account creation, and data is saved to users.json.


Log In:

Enter your username and password on the login screen and click "Login".
If credentials are valid, the main dashboard will open.


Dashboard Features:

View Summaries: The top right shows the current balance, and below it, three buttons display total income, expenses, and savings, updated in real-time.
Add Transaction: Click "➕ Add Expenses/Income" to open a form. Fill in details (type, amount, description, category, date, payment method, notes) and click "Add Record". The form closes on success.
Update Transaction: Click "✏️ Update Records" to select a transaction from a dropdown, edit its details, and click "Update Record".
Delete Transaction: Click "🗑 Delete Records" to select a transaction and click "Delete Record" to remove it.
View Reports: Click "📑 View Reports" to see a list of all transactions in a scrollable text area.
Errors (e.g., invalid input, missing transaction) trigger popup dialogs with clear messages.


Data Storage:

User credentials are stored in users.json.
Transactions are stored in <username>_transactions.json with fields: id, type, amount, description, category, date, payment_method, and notes.



File Structure

expense_tracker.py: Main application code containing LoginPage, MainDashboard, and Operations classes.
users.json: Stores user credentials (username and password).
<username>_transactions.json: Stores transactions for each user.
images/profile.png: Optional profile icon for the UI.

Example Transaction File (<username>_transactions.json)
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

Development Notes

Libraries Used:
customtkinter: For modern, customizable GUI components.
Pillow: For loading profile images.
json, os, uuid, datetime: Standard Python libraries for data handling, file operations, unique IDs, and date/time.


Error Handling: All operations (login, account creation, add/update/delete/view transactions) include try-except blocks to handle file I/O errors, invalid inputs, and other exceptions, with user-friendly popup dialogs.
UI Consistency: The CONFIG dictionary ensures consistent styling across the application (colors, fonts, sizes).
Data Persistence: JSON files are used for simplicity and portability, suitable for a desktop app.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and test thoroughly.
Commit your changes (git commit -m "Add your feature").
Push to your branch (git push origin feature/your-feature).
Open a pull request with a clear description of your changes.

Please ensure:

Code follows PEP 8 style guidelines.
New features include appropriate error handling and dialog feedback.
UI changes maintain the existing theme and CONFIG settings.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For issues or feature requests, please open an issue on the GitHub repository or contact [your-email@example.com].