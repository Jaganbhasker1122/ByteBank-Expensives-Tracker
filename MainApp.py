from customtkinter import *
from PIL import Image, ImageTk
import os
import json
import datetime
import uuid

# Set global theme
set_appearance_mode("light")
set_default_color_theme("blue")

# Configuration for consistent styling
CONFIG = {
    "primary": "#2563EB", "secondary": "#059669", "accent": "#DC2626", "warning": "#D97706",
    "success": "#10B981", "info": "#3B82F6", "neutral": "#6B7280", "background": "#F8FAFC",
    "surface": "#FFFFFF", "text_primary": "#1E293B", "text_secondary": "#64748B", 
    "border": "#E2E8F0", "hover_primary": "#1D4ED8", "hover_secondary": "#047857",
    "hover_accent": "#B91C1C", "hover_warning": "#B45309", "hover_success": "#059669",
    "hover_info": "#2563EB", "hover_neutral": "#4B5563",
    "title": ("Roboto", 24, "bold"), "subheading": ("Roboto", 20, "bold"),
    "body": ("Roboto", 16, "bold"), "label": ("Roboto", 14), "small": ("Roboto", 12),
    "button_width": 200, "button_height": 40, "entry_height": 35, "border_width": 2,
    "corner_radius": 10, "padding_y": 10, "padding_x": 10, "spacing": 10
}

# Load or initialize users.json
Users = {}
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        Users = json.load(f)
else:
    with open("users.json", "w") as f:
        json.dump(Users, f)

def create_button(parent, text, command=None, width=CONFIG["button_width"], height=CONFIG["button_height"],
                  fg_color=CONFIG["primary"], hover_color=CONFIG["hover_primary"], 
                  text_color="white", font=CONFIG["body"]):
    """Create a styled button with consistent properties."""
    return CTkButton(
        parent, text=text, width=width, height=height, border_width=CONFIG["border_width"],
        corner_radius=CONFIG["corner_radius"], fg_color=fg_color, hover_color=hover_color,
        text_color=text_color, font=font, cursor="hand2", command=command
    )

def show_popup(parent, message, title="Success", text_color=CONFIG["text_primary"]):
    """Show a popup dialog for success or error messages."""
    popup = CTkToplevel(parent)
    popup.geometry("300x150")
    popup.title(title)
    popup.resizable(False, False)
    popup.grab_set()
    popup.lift()
    popup.configure(fg_color=CONFIG["background"])

    dialog_label = CTkLabel(popup, text=message, font=CONFIG["body"], text_color=text_color)
    dialog_label.pack(pady=CONFIG["spacing"])

    ok_button = create_button(popup, "OK", width=100, height=30,
                              fg_color=CONFIG["secondary"], hover_color=CONFIG["hover_secondary"],
                              command=popup.destroy)
    ok_button.pack(pady=CONFIG["padding_y"])

class Operations:
    """Class to handle transaction operations (add, update, delete, view)."""
    @staticmethod
    def add_transaction(username, type_dropdown, amount_entry, description_entry, category_dropdown, 
                       date_entry, payment_dropdown, notes_entry, parent_window):
        """Add a new transaction to the user's file."""
        try:
            # Collect and validate data
            transaction_type = type_dropdown.get()
            amount_str = amount_entry.get().strip()
            description = description_entry.get().strip()
            category = category_dropdown.get()
            date = date_entry.get().strip() or datetime.datetime.now().strftime("%Y-%m-%d")
            payment_method = payment_dropdown.get()
            notes = notes_entry.get().strip()

            if not transaction_type or transaction_type not in ["Expense", "Income"]:
                show_popup(parent_window, "Please select a valid type.", "Error", CONFIG["accent"])
                return
            if not amount_str or not amount_str.replace('.', '', 1).isdigit() or float(amount_str) <= 0:
                show_popup(parent_window, "Please enter a valid amount (> 0).", "Error", CONFIG["accent"])
                return
            if not description:
                show_popup(parent_window, "Description is required.", "Error", CONFIG["accent"])
                return
            if not category:
                show_popup(parent_window, "Please select a category.", "Error", CONFIG["accent"])
                return
            if not payment_method:
                show_popup(parent_window, "Please select a payment method.", "Error", CONFIG["accent"])
                return

            amount = float(amount_str)
            transaction_id = str(uuid.uuid4())
            transaction_data = {
                "id": transaction_id,
                "type": transaction_type,
                "amount": amount,
                "description": description,
                "category": category,
                "date": date,
                "payment_method": payment_method,
                "notes": notes
            }

            # Load or create user file
            user_file = f"{username}_transactions.json"
            transactions = []
            if os.path.exists(user_file):
                with open(user_file, "r") as f:
                    transactions = json.load(f)

            transactions.append(transaction_data)

            # Save to file
            with open(user_file, "w") as f:
                json.dump(transactions, f, indent=4)

            show_popup(parent_window, "Transaction added successfully!")
            parent_window.destroy()
        except Exception as e:
            show_popup(parent_window, f"Error adding transaction: {str(e)}", "Error", CONFIG["accent"])

    @staticmethod
    def update_transaction(username, transaction_id, type_dropdown, amount_entry, description_entry, 
                          category_dropdown, date_entry, payment_dropdown, notes_entry, parent_window):
        """Update an existing transaction."""
        try:
            user_file = f"{username}_transactions.json"
            if not os.path.exists(user_file):
                show_popup(parent_window, "No transactions found.", "Error", CONFIG["accent"])
                return

            with open(user_file, "r") as f:
                transactions = json.load(f)

            # Find transaction
            for transaction in transactions:
                if transaction["id"] == transaction_id:
                    # Collect and validate data
                    transaction_type = type_dropdown.get()
                    amount_str = amount_entry.get().strip()
                    description = description_entry.get().strip()
                    category = category_dropdown.get()
                    date = date_entry.get().strip() or transaction["date"]
                    payment_method = payment_dropdown.get()
                    notes = notes_entry.get().strip()

                    if not transaction_type or transaction_type not in ["Expense", "Income"]:
                        show_popup(parent_window, "Please select a valid type.", "Error", CONFIG["accent"])
                        return
                    if not amount_str or not amount_str.replace('.', '', 1).isdigit() or float(amount_str) <= 0:
                        show_popup(parent_window, "Please enter a valid amount (> 0).", "Error", CONFIG["accent"])
                        return
                    if not description:
                        show_popup(parent_window, "Description is required.", "Error", CONFIG["accent"])
                        return
                    if not category:
                        show_popup(parent_window, "Please select a category.", "Error", CONFIG["accent"])
                        return
                    if not payment_method:
                        show_popup(parent_window, "Please select a payment method.", "Error", CONFIG["accent"])
                        return

                    # Update transaction
                    transaction.update({
                        "type": transaction_type,
                        "amount": float(amount_str),
                        "description": description,
                        "category": category,
                        "date": date,
                        "payment_method": payment_method,
                        "notes": notes
                    })

                    with open(user_file, "w") as f:
                        json.dump(transactions, f, indent=4)

                    show_popup(parent_window, "Transaction updated successfully!")
                    parent_window.destroy()
                    return

            show_popup(parent_window, "Transaction not found.", "Error", CONFIG["accent"])
        except Exception as e:
            show_popup(parent_window, f"Error updating transaction: {str(e)}", "Error", CONFIG["accent"])

    @staticmethod
    def delete_transaction(username, transaction_id, parent_window):
        """Delete a transaction by ID."""
        try:
            user_file = f"{username}_transactions.json"
            if not os.path.exists(user_file):
                show_popup(parent_window, "No transactions found.", "Error", CONFIG["accent"])
                return

            with open(user_file, "r") as f:
                transactions = json.load(f)

            original_count = len(transactions)
            transactions = [t for t in transactions if t["id"] != transaction_id]

            if len(transactions) == original_count:
                show_popup(parent_window, "Transaction not found.", "Error", CONFIG["accent"])
                return

            with open(user_file, "w") as f:
                json.dump(transactions, f, indent=4)

            show_popup(parent_window, "Transaction deleted successfully!")
            parent_window.destroy()
        except Exception as e:
            show_popup(parent_window, f"Error deleting transaction: {str(e)}", "Error", CONFIG["accent"])

    @staticmethod
    def view_transactions(username):
        """Retrieve all transactions for a user."""
        try:
            user_file = f"{username}_transactions.json"
            if not os.path.exists(user_file):
                return []
            with open(user_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error viewing transactions: {str(e)}")
            return []

    @staticmethod
    def get_summary(username):
        """Calculate total income, expense, savings, and balance."""
        try:
            transactions = Operations.view_transactions(username)
            total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
            total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
            total_savings = total_income - total_expense
            current_balance = total_savings
            return {
                "total_income": total_income,
                "total_expense": total_expense,
                "total_savings": total_savings,
                "current_balance": current_balance
            }
        except Exception as e:
            print(f"Error calculating summary: {str(e)}")
            return {
                "total_income": 0.0,
                "total_expense": 0.0,
                "total_savings": 0.0,
                "current_balance": 0.0
            }

class LoginPage:
    """Class to manage the login page UI and functionality."""
    def __init__(self):
        self.app = CTk()
        self.app.geometry("400x500")
        self.app.title("ByteBank - Expense Tracker")
        self.app.resizable(False, False)
        self.app.configure(fg_color=CONFIG["background"])
        self.setup_ui()

    def setup_ui(self):
        """Set up the login page UI elements."""
        # Title
        title = CTkLabel(self.app, text="Welcome to ByteBank", font=CONFIG["title"], 
                        text_color=CONFIG["primary"])
        title.pack(pady=CONFIG["spacing"] * 2)

        # Profile Icon
        try:
            profile_icon = CTkImage(Image.open("images/profile.png"), size=(100, 100))
            profile_label = CTkLabel(self.app, image=profile_icon, text="", font=CONFIG["body"])
            profile_label.pack(pady=CONFIG["spacing"])
        except:
            pass

        # Username Entry
        self.username_entry = CTkEntry(self.app, placeholder_text="Username", width=300, 
                                     height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                     corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                     text_color=CONFIG["text_primary"], 
                                     placeholder_text_color=CONFIG["text_secondary"])
        self.username_entry.pack(pady=CONFIG["padding_y"])

        # Password Entry
        self.password_entry = CTkEntry(self.app, placeholder_text="Password", width=300, 
                                      height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                      corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                      text_color=CONFIG["text_primary"], show="*",
                                      placeholder_text_color=CONFIG["text_secondary"])
        self.password_entry.pack(pady=CONFIG["padding_y"])

        # Login Button
        login_button = create_button(self.app, "Login", command=self.login)
        login_button.pack(pady=CONFIG["spacing"])

        # Create Account Link
        create_account_label = CTkLabel(self.app, text="Don't have an account? Create one now!",
                                       font=CONFIG["label"], text_color=CONFIG["secondary"], 
                                       cursor="hand2")
        create_account_label.pack(pady=CONFIG["padding_y"])
        create_account_label.bind("<Button-1>", lambda e: self.create_account_window())

    def login(self):
        """Handle login action."""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            if not username or not password:
                show_popup(self.app, "Please fill all fields.", "Error", CONFIG["accent"])
                return
            if username in Users and Users[username]["password"] == password:
                print(f"Login successful for {username}")
                self.app.destroy()
                MainDashboard(username).run()
            else:
                show_popup(self.app, "Invalid username or password!", "Login Failed", CONFIG["accent"])
        except Exception as e:
            show_popup(self.app, f"Login error: {str(e)}", "Error", CONFIG["accent"])

    def create_account_window(self):
        """Open create account window."""
        try:
            create_acc = CTkToplevel(self.app)
            create_acc.geometry("400x400")
            create_acc.title("Create Account")
            create_acc.resizable(False, False)
            create_acc.grab_set()
            create_acc.lift()

            # Title
            create_acc_label = CTkLabel(create_acc, text="Create Account", font=CONFIG["subheading"], 
                                       text_color=CONFIG["text_primary"])
            create_acc_label.pack(pady=CONFIG["spacing"])

            # Entries
            new_username_entry = CTkEntry(create_acc, placeholder_text="New Username", width=250, 
                                        height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                        corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                        text_color=CONFIG["text_primary"], 
                                        placeholder_text_color=CONFIG["text_secondary"])
            new_username_entry.pack(pady=CONFIG["padding_y"])

            new_password_entry = CTkEntry(create_acc, placeholder_text="New Password", width=250, 
                                         height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                         corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                         text_color=CONFIG["text_primary"], show="*",
                                         placeholder_text_color=CONFIG["text_secondary"])
            new_password_entry.pack(pady=CONFIG["padding_y"])

            confirm_password_entry = CTkEntry(create_acc, placeholder_text="Confirm Password", width=250, 
                                            height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                            corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                            text_color=CONFIG["text_primary"], show="*",
                                            placeholder_text_color=CONFIG["text_secondary"])
            confirm_password_entry.pack(pady=CONFIG["padding_y"])

            # Create Button
            create_acc_button = create_button(create_acc, "Create Account")
            create_acc_button.pack(pady=CONFIG["spacing"])

            def create_account_action():
                try:
                    for child in create_acc.winfo_children():
                        if isinstance(child, CTkLabel) and "error" in str(child.cget("text")).lower():
                            child.destroy()
                    
                    username = new_username_entry.get().strip()
                    password = new_password_entry.get()
                    confirm_password = confirm_password_entry.get()

                    if not username or not password:
                        error_label = CTkLabel(create_acc, text="Please fill all fields!", font=CONFIG["small"], 
                                              text_color=CONFIG["accent"])
                        error_label.pack(pady=CONFIG["padding_y"])
                        return
                    elif password != confirm_password:
                        error_label = CTkLabel(create_acc, text="Passwords do not match!", font=CONFIG["small"], 
                                              text_color=CONFIG["accent"])
                        error_label.pack(pady=CONFIG["padding_y"])
                        return
                    elif username in Users:
                        error_label = CTkLabel(create_acc, text="Username already exists!", font=CONFIG["small"], 
                                              text_color=CONFIG["accent"])
                        error_label.pack(pady=CONFIG["padding_y"])
                        return
                    else:
                        Users[username] = {"password": password}
                        with open("users.json", "w") as f:
                            json.dump(Users, f, indent=4)
                        print(f"Account created for {username}")
                        create_acc.destroy()
                        show_popup(self.app, "Account successfully created!")
                except Exception as e:
                    show_popup(create_acc, f"Error creating account: {str(e)}", "Error", CONFIG["accent"])

            create_acc_button.configure(command=create_account_action)
        except Exception as e:
            show_popup(self.app, f"Error opening create account window: {str(e)}", "Error", CONFIG["accent"])

    def run(self):
        """Run the login page application."""
        self.app.mainloop()

class MainDashboard:
    """Class to manage the main dashboard UI and functionality."""
    def __init__(self, username):
        self.username = username
        self.dashboard = CTk()
        self.dashboard.geometry("800x600")
        self.dashboard.title("ByteBank - Main Dashboard")
        self.dashboard.resizable(False, False)
        self.dashboard.configure(fg_color=CONFIG["background"])
        self.setup_ui()

    def setup_ui(self):
        """Set up the dashboard UI elements."""
        # Profile Icon + Username
        try:
            profile_icon = CTkImage(Image.open("images/profile.png"), size=(40, 40))
        except:
            profile_icon = None
        profile_label = CTkLabel(
            self.dashboard, text=f"Welcome, {self.username}", image=profile_icon,
            compound="left", font=CONFIG["body"], text_color=CONFIG["text_primary"]
        )
        profile_label.place(x=20, y=10)

        # Date & Time
        date_text = CTkLabel(self.dashboard, text="Date:", font=CONFIG["label"], 
                            text_color=CONFIG["text_secondary"])
        date_text.place(x=20, y=50)
        self.date_value = CTkLabel(self.dashboard, text="", font=CONFIG["body"], 
                                  text_color=CONFIG["info"])
        self.date_value.place(x=80, y=50)

        time_text = CTkLabel(self.dashboard, text="Time:", font=CONFIG["label"], 
                            text_color=CONFIG["text_secondary"])
        time_text.place(x=20, y=80)
        self.time_value = CTkLabel(self.dashboard, text="", font=CONFIG["body"], 
                                  text_color=CONFIG["warning"])
        self.time_value.place(x=80, y=80)

        self.update_datetime()

        # Summary Buttons
        btn_width = 200
        btn_height = 50
        btn_y = 140
        spacing = 20
        start_x = (800 - (3 * btn_width + 2 * spacing)) // 2

        self.current_balance_btn = create_button(self.dashboard, "Current Balance: ₹0.00", width=200, height=35,
                                               fg_color=CONFIG["success"], hover_color=CONFIG["hover_success"],
                                               text_color=CONFIG["text_primary"], font=("Roboto", 14, "bold"))
        self.current_balance_btn.place(x=550, y=45)

        self.total_income_btn = create_button(self.dashboard, "Total Income: ₹0.00", width=btn_width, height=btn_height,
                                            fg_color=CONFIG["success"], hover_color=CONFIG["hover_success"],
                                            text_color="white", font=CONFIG["body"])
        self.total_income_btn.place(x=start_x, y=btn_y)

        self.total_expense_btn = create_button(self.dashboard, "Total Expense: ₹0.00", width=btn_width, height=btn_height,
                                             fg_color=CONFIG["warning"], hover_color=CONFIG["hover_warning"],
                                             text_color="white", font=CONFIG["body"])
        self.total_expense_btn.place(x=start_x + btn_width + spacing, y=btn_y)

        self.savings_btn = create_button(self.dashboard, "Total Savings: ₹0.00", width=btn_width, height=btn_height,
                                       fg_color=CONFIG["secondary"], hover_color=CONFIG["hover_secondary"],
                                       text_color="white", font=CONFIG["body"])
        self.savings_btn.place(x=start_x + 2*(btn_width + spacing), y=btn_y)

        self.update_summary()

        # Horizontal Separator
        separator = CTkFrame(self.dashboard, fg_color=CONFIG["border"], height=2)
        separator.place(x=0, y=120, relwidth=1)

        # Form Frame
        form_frame = CTkFrame(self.dashboard, width=400, height=350, 
                             fg_color=CONFIG["surface"], corner_radius=15)
        form_frame.place(x=200, y=220)
        form_frame.pack_propagate(False)

        title = CTkLabel(form_frame, text="📊 Dashboard Menu", font=CONFIG["subheading"], 
                        text_color=CONFIG["text_primary"])
        title.pack(pady=(CONFIG["spacing"], CONFIG["spacing"] * 2))

        btn_add = create_button(form_frame, "➕ Add Expenses/Income", width=280, height=45,
                               fg_color=CONFIG["primary"], hover_color=CONFIG["hover_primary"],
                               command=self.add_expense_form)
        btn_add.pack(pady=CONFIG["padding_y"])

        btn_update = create_button(form_frame, "✏️ Update Records", width=280, height=45,
                                 fg_color=CONFIG["warning"], hover_color=CONFIG["hover_warning"],
                                 command=self.update_records_form)
        btn_update.pack(pady=CONFIG["padding_y"])

        btn_delete = create_button(form_frame, "🗑 Delete Records", width=280, height=45,
                                 fg_color=CONFIG["accent"], hover_color=CONFIG["hover_accent"],
                                 command=self.delete_records_form)
        btn_delete.pack(pady=CONFIG["padding_y"])

        btn_report = create_button(form_frame, "📑 View Reports", width=280, height=45,
                                 fg_color=CONFIG["info"], hover_color=CONFIG["hover_info"],
                                 command=self.view_reports_form)
        btn_report.pack(pady=CONFIG["padding_y"])

    def update_datetime(self):
        """Update date and time display."""
        try:
            now = datetime.datetime.now()
            self.date_value.configure(text=now.strftime("%Y-%m-%d"))
            self.time_value.configure(text=now.strftime("%H:%M:%S"))
            self.dashboard.after(1000, self.update_datetime)
        except Exception as e:
            print(f"Error updating datetime: {str(e)}")

    def update_summary(self):
        """Update summary buttons with current totals."""
        try:
            summary = Operations.get_summary(self.username)
            self.current_balance_btn.configure(text=f"Current Balance: ₹{summary['current_balance']:.2f}")
            self.total_income_btn.configure(text=f"Total Income: ₹{summary['total_income']:.2f}")
            self.total_expense_btn.configure(text=f"Total Expense: ₹{summary['total_expense']:.2f}")
            self.savings_btn.configure(text=f"Total Savings: ₹{summary['total_savings']:.2f}")
            self.dashboard.after(1000, self.update_summary)
        except Exception as e:
            print(f"Error updating summary: {str(e)}")

    def add_expense_form(self):
        """Open form for adding expenses/income."""
        try:
            add_window = CTkToplevel(self.dashboard)
            add_window.geometry("700x500")
            add_window.title("Add Expense/Income")
            add_window.resizable(False, False)
            add_window.grab_set()
            add_window.lift()
            add_window.configure(fg_color=CONFIG["background"])

            add_window.grid_columnconfigure(1, weight=1)
            add_window.grid_columnconfigure(3, weight=1)

            form_title = CTkLabel(add_window, text="➕ Add New Expense / Income", 
                                 font=CONFIG["subheading"], text_color=CONFIG["text_primary"])
            form_title.grid(row=0, column=0, columnspan=4, 
                           pady=(CONFIG["spacing"], CONFIG["spacing"] * 2), sticky="ew")

            # Type Dropdown
            type_label = CTkLabel(add_window, text="Type:", font=CONFIG["label"], 
                                 text_color=CONFIG["text_secondary"])
            type_label.grid(row=1, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            type_dropdown = CTkOptionMenu(add_window, values=["Expense", "Income"], width=140, 
                                         corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                         text_color=CONFIG["text_primary"], button_color=CONFIG["primary"],
                                         button_hover_color=CONFIG["hover_primary"], 
                                         dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            type_dropdown.grid(row=1, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Amount Entry
            amount_label = CTkLabel(add_window, text="Amount:", font=CONFIG["label"], 
                                   text_color=CONFIG["text_secondary"])
            amount_label.grid(row=1, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            amount_entry = CTkEntry(add_window, placeholder_text="₹0.00", width=140, 
                                   height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                   corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                   text_color=CONFIG["text_primary"], 
                                   placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            amount_entry.grid(row=1, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Description Entry
            description_label = CTkLabel(add_window, text="Description:", font=CONFIG["label"], 
                                        text_color=CONFIG["text_secondary"])
            description_label.grid(row=2, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            description_entry = CTkEntry(add_window, placeholder_text="Enter details (e.g., Lunch, Salary)", 
                                        width=350, height=CONFIG["entry_height"], 
                                        border_width=CONFIG["border_width"], corner_radius=CONFIG["corner_radius"],
                                        fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                        placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            description_entry.grid(row=2, column=1, columnspan=3, padx=CONFIG["padding_x"], 
                                  pady=CONFIG["padding_y"], sticky="ew")

            # Category Dropdown
            category_label = CTkLabel(add_window, text="Category:", font=CONFIG["label"], 
                                     text_color=CONFIG["text_secondary"])
            category_label.grid(row=3, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            category_dropdown = CTkOptionMenu(add_window, values=["Food", "Travel", "Bills", "Shopping", "Salary", "Other"], 
                                            width=140, corner_radius=CONFIG["corner_radius"], 
                                            fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                            button_color=CONFIG["secondary"], 
                                            button_hover_color=CONFIG["hover_secondary"],
                                            dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            category_dropdown.grid(row=3, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Date Entry
            date_label = CTkLabel(add_window, text="Date:", font=CONFIG["label"], 
                                 text_color=CONFIG["text_secondary"])
            date_label.grid(row=3, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            date_entry = CTkEntry(add_window, placeholder_text="YYYY-MM-DD", width=140, 
                                 height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                 corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                 text_color=CONFIG["text_primary"], 
                                 placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            date_entry.grid(row=3, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Payment Method Dropdown
            payment_label = CTkLabel(add_window, text="Payment:", font=CONFIG["label"], 
                                    text_color=CONFIG["text_secondary"])
            payment_label.grid(row=4, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            payment_dropdown = CTkOptionMenu(add_window, values=["Cash", "Card", "UPI", "Bank Transfer"], width=140,
                                            corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                            text_color=CONFIG["text_primary"], button_color=CONFIG["info"],
                                            button_hover_color=CONFIG["hover_info"], 
                                            dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            payment_dropdown.grid(row=4, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Notes Entry
            notes_label = CTkLabel(add_window, text="Notes:", font=CONFIG["label"], 
                                  text_color=CONFIG["text_secondary"])
            notes_label.grid(row=4, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            notes_entry = CTkEntry(add_window, placeholder_text="Optional notes", width=140, 
                                  height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                  corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                  text_color=CONFIG["text_primary"], 
                                  placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            notes_entry.grid(row=4, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Buttons
            button_frame = CTkFrame(add_window, fg_color="transparent")
            button_frame.grid(row=5, column=0, columnspan=4, pady=(CONFIG["spacing"] * 2, CONFIG["padding_y"]))

            add_button = create_button(button_frame, "Add Record", width=160, height=CONFIG["button_height"],
                                     fg_color=CONFIG["secondary"], hover_color=CONFIG["hover_secondary"],
                                     command=lambda: Operations.add_transaction(
                                         self.username, type_dropdown, amount_entry, description_entry,
                                         category_dropdown, date_entry, payment_dropdown, notes_entry, add_window
                                     ))
            add_button.pack(side="left", padx=CONFIG["padding_x"])

            cancel_button = create_button(button_frame, "Cancel", width=120, height=CONFIG["button_height"],
                                         fg_color=CONFIG["neutral"], hover_color=CONFIG["hover_neutral"],
                                         text_color="white", command=add_window.destroy)
            cancel_button.pack(side="left", padx=CONFIG["padding_x"])
        
        except Exception as e:
            show_popup(self.dashboard, f"Error opening add expense form: {str(e)}", "Error", CONFIG["accent"])

    def update_records_form(self):
        """Open form for updating transactions."""
        try:
            update_window = CTkToplevel(self.dashboard)
            update_window.geometry("700x600")
            update_window.title("Update Records")
            update_window.resizable(False, False)
            update_window.grab_set()
            update_window.lift()
            update_window.configure(fg_color=CONFIG["background"])

            update_window.grid_columnconfigure(1, weight=1)
            update_window.grid_columnconfigure(3, weight=1)

            form_title = CTkLabel(update_window, text="✏️ Update Transaction", 
                                 font=CONFIG["subheading"], text_color=CONFIG["text_primary"])
            form_title.grid(row=0, column=0, columnspan=4, 
                           pady=(CONFIG["spacing"], CONFIG["spacing"] * 2), sticky="ew")

            # Transaction Selection
            transaction_label = CTkLabel(update_window, text="Select Transaction:", font=CONFIG["label"], 
                                        text_color=CONFIG["text_secondary"])
            transaction_label.grid(row=1, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            transactions = Operations.view_transactions(self.username)
            transaction_options = [f"{t['description']} ({t['type']}: ₹{t['amount']:.2f})" for t in transactions]
            transaction_ids = [t["id"] for t in transactions]
            transaction_dropdown = CTkOptionMenu(update_window, values=transaction_options or ["No transactions"], 
                                               width=400, corner_radius=CONFIG["corner_radius"], 
                                               fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                               button_color=CONFIG["primary"], button_hover_color=CONFIG["hover_primary"],
                                               dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            transaction_dropdown.grid(row=1, column=1, columnspan=3, padx=CONFIG["padding_x"], 
                                    pady=CONFIG["padding_y"], sticky="ew")

            # Type Dropdown
            type_label = CTkLabel(update_window, text="Type:", font=CONFIG["label"], 
                                 text_color=CONFIG["text_secondary"])
            type_label.grid(row=2, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            type_dropdown = CTkOptionMenu(update_window, values=["Expense", "Income"], width=140, 
                                         corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                         text_color=CONFIG["text_primary"], button_color=CONFIG["primary"],
                                         button_hover_color=CONFIG["hover_primary"], 
                                         dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            type_dropdown.grid(row=2, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Amount Entry
            amount_label = CTkLabel(update_window, text="Amount:", font=CONFIG["label"], 
                                   text_color=CONFIG["text_secondary"])
            amount_label.grid(row=2, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            amount_entry = CTkEntry(update_window, placeholder_text="₹0.00", width=140, 
                                   height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                   corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                   text_color=CONFIG["text_primary"], 
                                   placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            amount_entry.grid(row=2, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Description Entry
            description_label = CTkLabel(update_window, text="Description:", font=CONFIG["label"], 
                                        text_color=CONFIG["text_secondary"])
            description_label.grid(row=3, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            description_entry = CTkEntry(update_window, placeholder_text="Enter details (e.g., Lunch, Salary)", 
                                        width=350, height=CONFIG["entry_height"], 
                                        border_width=CONFIG["border_width"], corner_radius=CONFIG["corner_radius"],
                                        fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                        placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            description_entry.grid(row=3, column=1, columnspan=3, padx=CONFIG["padding_x"], 
                                  pady=CONFIG["padding_y"], sticky="ew")

            # Category Dropdown
            category_label = CTkLabel(update_window, text="Category:", font=CONFIG["label"], 
                                     text_color=CONFIG["text_secondary"])
            category_label.grid(row=4, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            category_dropdown = CTkOptionMenu(update_window, values=["Food", "Travel", "Bills", "Shopping", "Salary", "Other"], 
                                            width=140, corner_radius=CONFIG["corner_radius"], 
                                            fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                            button_color=CONFIG["secondary"], 
                                            button_hover_color=CONFIG["hover_secondary"],
                                            dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            category_dropdown.grid(row=4, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Date Entry
            date_label = CTkLabel(update_window, text="Date:", font=CONFIG["label"], 
                                 text_color=CONFIG["text_secondary"])
            date_label.grid(row=4, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            date_entry = CTkEntry(update_window, placeholder_text="YYYY-MM-DD", width=140, 
                                 height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                 corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                 text_color=CONFIG["text_primary"], 
                                 placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            date_entry.grid(row=4, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Payment Method Dropdown
            payment_label = CTkLabel(update_window, text="Payment:", font=CONFIG["label"], 
                                    text_color=CONFIG["text_secondary"])
            payment_label.grid(row=5, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            payment_dropdown = CTkOptionMenu(update_window, values=["Cash", "Card", "UPI", "Bank Transfer"], width=140,
                                            corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                            text_color=CONFIG["text_primary"], button_color=CONFIG["info"],
                                            button_hover_color=CONFIG["hover_info"], 
                                            dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            payment_dropdown.grid(row=5, column=1, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            # Notes Entry
            notes_label = CTkLabel(update_window, text="Notes:", font=CONFIG["label"], 
                                  text_color=CONFIG["text_secondary"])
            notes_label.grid(row=5, column=2, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            notes_entry = CTkEntry(update_window, placeholder_text="Optional notes", width=140, 
                                  height=CONFIG["entry_height"], border_width=CONFIG["border_width"],
                                  corner_radius=CONFIG["corner_radius"], fg_color=CONFIG["surface"],
                                  text_color=CONFIG["text_primary"], 
                                  placeholder_text_color=CONFIG["text_secondary"], font=CONFIG["label"])
            notes_entry.grid(row=5, column=3, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="w")

            def load_transaction():
                """Load selected transaction data into form fields."""
                try:
                    selected_index = transaction_dropdown.get()
                    if selected_index == "No transactions":
                        return
                    selected_index = transaction_options.index(selected_index)
                    selected_transaction = transactions[selected_index]
                    type_dropdown.set(selected_transaction["type"])
                    amount_entry.delete(0, "end")
                    amount_entry.insert(0, str(selected_transaction["amount"]))
                    description_entry.delete(0, "end")
                    description_entry.insert(0, selected_transaction["description"])
                    category_dropdown.set(selected_transaction["category"])
                    date_entry.delete(0, "end")
                    date_entry.insert(0, selected_transaction["date"])
                    payment_dropdown.set(selected_transaction["payment_method"])
                    notes_entry.delete(0, "end")
                    notes_entry.insert(0, selected_transaction["notes"])
                except Exception as e:
                    show_popup(update_window, f"Error loading transaction: {str(e)}", "Error", CONFIG["accent"])

            transaction_dropdown.configure(command=lambda _: load_transaction())

            # Buttons
            button_frame = CTkFrame(update_window, fg_color="transparent")
            button_frame.grid(row=6, column=0, columnspan=4, pady=(CONFIG["spacing"] * 2, CONFIG["padding_y"]))

            update_button = create_button(button_frame, "Update Record", width=160, height=CONFIG["button_height"],
                                        fg_color=CONFIG["warning"], hover_color=CONFIG["hover_warning"],
                                        command=lambda: Operations.update_transaction(
                                            self.username, transaction_ids[transaction_options.index(transaction_dropdown.get())] if transaction_options else None,
                                            type_dropdown, amount_entry, description_entry, category_dropdown,
                                            date_entry, payment_dropdown, notes_entry, update_window
                                        ) if transaction_dropdown.get() != "No transactions" else show_popup(update_window, "Please select a transaction.", "Error", CONFIG["accent"]))
            update_button.pack(side="left", padx=CONFIG["padding_x"])

            cancel_button = create_button(button_frame, "Cancel", width=120, height=CONFIG["button_height"],
                                         fg_color=CONFIG["neutral"], hover_color=CONFIG["hover_neutral"],
                                         text_color="white", command=update_window.destroy)
            cancel_button.pack(side="left", padx=CONFIG["padding_x"])
        except Exception as e:
            show_popup(self.dashboard, f"Error opening update form: {str(e)}", "Error", CONFIG["accent"])

    def delete_records_form(self):
        """Open form for deleting transactions."""
        try:
            delete_window = CTkToplevel(self.dashboard)
            delete_window.geometry("700x300")
            delete_window.title("Delete Records")
            delete_window.resizable(False, False)
            delete_window.grab_set()
            delete_window.lift()
            delete_window.configure(fg_color=CONFIG["background"])

            delete_window.grid_columnconfigure(1, weight=1)

            form_title = CTkLabel(delete_window, text="🗑 Delete Transaction", 
                                 font=CONFIG["subheading"], text_color=CONFIG["text_primary"])
            form_title.grid(row=0, column=0, columnspan=2, 
                           pady=(CONFIG["spacing"], CONFIG["spacing"] * 2), sticky="ew")

            # Transaction Selection
            transaction_label = CTkLabel(delete_window, text="Select Transaction:", font=CONFIG["label"], 
                                        text_color=CONFIG["text_secondary"])
            transaction_label.grid(row=1, column=0, padx=CONFIG["padding_x"], pady=CONFIG["padding_y"], sticky="e")
            transactions = Operations.view_transactions(self.username)
            transaction_options = [f"{t['description']} ({t['type']}: ₹{t['amount']:.2f})" for t in transactions]
            transaction_ids = [t["id"] for t in transactions]
            transaction_dropdown = CTkOptionMenu(delete_window, values=transaction_options or ["No transactions"], 
                                               width=400, corner_radius=CONFIG["corner_radius"], 
                                               fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"],
                                               button_color=CONFIG["accent"], button_hover_color=CONFIG["hover_accent"],
                                               dropdown_fg_color=CONFIG["surface"], font=CONFIG["label"])
            transaction_dropdown.grid(row=1, column=1, padx=CONFIG["padding_x"], 
                                    pady=CONFIG["padding_y"], sticky="ew")

            # Buttons
            button_frame = CTkFrame(delete_window, fg_color="transparent")
            button_frame.grid(row=2, column=0, columnspan=2, pady=(CONFIG["spacing"] * 2, CONFIG["padding_y"]))

            delete_button = create_button(button_frame, "Delete Record", width=160, height=CONFIG["button_height"],
                                        fg_color=CONFIG["accent"], hover_color=CONFIG["hover_accent"],
                                        command=lambda: Operations.delete_transaction(
                                            self.username, transaction_ids[transaction_options.index(transaction_dropdown.get())] if transaction_options else None,
                                            delete_window
                                        ) if transaction_dropdown.get() != "No transactions" else show_popup(delete_window, "Please select a transaction.", "Error", CONFIG["accent"]))
            delete_button.pack(side="left", padx=CONFIG["padding_x"])

            cancel_button = create_button(button_frame, "Cancel", width=120, height=CONFIG["button_height"],
                                         fg_color=CONFIG["neutral"], hover_color=CONFIG["hover_neutral"],
                                         text_color="white", command=delete_window.destroy)
            cancel_button.pack(side="left", padx=CONFIG["padding_x"])
        except Exception as e:
            show_popup(self.dashboard, f"Error opening delete form: {str(e)}", "Error", CONFIG["accent"])

    def view_reports_form(self):
        """Open form to view transaction history."""
        try:
            report_window = CTkToplevel(self.dashboard)
            report_window.geometry("700x500")
            report_window.title("View Reports")
            report_window.resizable(False, False)
            report_window.grab_set()
            report_window.lift()
            report_window.configure(fg_color=CONFIG["background"])

            form_title = CTkLabel(report_window, text="📑 Transaction History", 
                                 font=CONFIG["subheading"], text_color=CONFIG["text_primary"])
            form_title.pack(pady=(CONFIG["spacing"], CONFIG["spacing"] * 2))

            # Transaction List
            transactions = Operations.view_transactions(self.username)
            if not transactions:
                no_transactions_label = CTkLabel(report_window, text="No transactions found.", 
                                                font=CONFIG["body"], text_color=CONFIG["text_secondary"])
                no_transactions_label.pack(pady=CONFIG["padding_y"])
            else:
                text_area = CTkTextbox(report_window, width=650, height=350, font=CONFIG["label"], 
                                      fg_color=CONFIG["surface"], text_color=CONFIG["text_primary"])
                text_area.pack(pady=CONFIG["padding_y"])
                for t in transactions:
                    text_area.insert("end", f"ID: {t['id']}\n"
                                          f"Type: {t['type']}\n"
                                          f"Amount: ₹{t['amount']:.2f}\n"
                                          f"Description: {t['description']}\n"
                                          f"Category: {t['category']}\n"
                                          f"Date: {t['date']}\n"
                                          f"Payment Method: {t['payment_method']}\n"
                                          f"Notes: {t['notes'] or 'None'}\n"
                                          f"{'-'*40}\n")
                text_area.configure(state="disabled")

            # Close Button
            close_button = create_button(report_window, "Close", width=120, height=CONFIG["button_height"],
                                       fg_color=CONFIG["neutral"], hover_color=CONFIG["hover_neutral"],
                                       command=report_window.destroy)
            close_button.pack(pady=CONFIG["padding_y"])
        except Exception as e:
            show_popup(self.dashboard, f"Error opening reports: {str(e)}", "Error", CONFIG["accent"])

    def run(self):
        """Run the dashboard application."""
        self.dashboard.mainloop()

if __name__ == "__main__":
#     # Uncomment the following line for normal login flow
    LoginPage().run()
    
#     # Direct dashboard access for development
#     # MainDashboard("Jagan bhasker").run()