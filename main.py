from os.path import exists, join
from tkinter import Tk, Frame, Label, Button, Entry, Toplevel, messagebox, ttk, Radiobutton, PhotoImage, StringVar
import sqlite3
import bcrypt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ctypes import windll
from tkcalendar import DateEntry

DATA = "data.db"

FONT1 = "Calibri"
FONT2 = "Century Gothic"

BLUE = "#0B70A3"
DARK = "#215679"
GREEN = "#3ECCD7"
GREY = "#EDEDED"
ORANGE = "#FF6600"
BLACK = "#464646"
WHITE = '#FFFFFF'

def main():
    # Check for required image files.
    if not exists("assets"):
        messagebox.showerror("Error - Folder not found", "The 'assets' folder is missing from the src folder."
            "\nThe program will now terminate.")
    else:
        image_files = ("logo.ico", "logo.png", "up.png", "down.png")
        for file in image_files:
            file = join("assets", file)
            if not exists(file):
                messagebox.showerror("Error - File not found", "The image file in path '{}' is missing."
                    "\nThe program will terminate.".format(file))

    default_expenses = ["Unlabeled",
                        "Housing",
                        "Food",
                        "Transportation",
                        "Utilities",
                        "Healthcare",
                        "Insurance",
                        "Personal",
                        "Taxes"
                        ]

    default_incomes = ["Unlabeled",
                       "Earned Income",
                       "Passive Income",
                       "Portfolio Income"
                       ]
    # Add categories in the lists above as needed (affects all users).
    # Removing has no effect once the 'DATA' file has been created.
    # To remove a category, delete the 'DATA' file first (data will be lost).
    # 'DATA' file will be automatically (re)created.

    # Database setup:
    con = sqlite3.connect(DATA)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS expense_types (id INTEGER PRIMARY KEY, category TEXT UNIQUE)")
    for expense in default_expenses:
        cur.execute("INSERT OR IGNORE INTO expense_types (category) VALUES (?)", (expense,))
    cur.execute("CREATE TABLE IF NOT EXISTS income_types (id INTEGER PRIMARY KEY, category TEXT UNIQUE)")
    for income in default_incomes:
        cur.execute("INSERT OR IGNORE INTO income_types (category) VALUES (?)", (income,))
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user TEXT UNIQUE, pw TEXT, budget REAL)")
    cur.close()
    con.close()

    # ctypes.windll adjusts resolution and scaling.
    login = LoginPage()
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        messagebox.showwarning("Warning", "Failed to set DPI awareness. Resolution may not properly scale.")

    login.mainloop()


class LoginPage(Tk):
    def __init__(self):
        super().__init__()
        self.title("slice- LOGIN")
        self.iconbitmap("assets/logo.ico")
        self.geometry("1000x600+1000+500")
        self.configure(bg=WHITE)
        self.logo = PhotoImage(file="assets/logo.png")

        frame1 = Frame()
        frame1.configure(bg=WHITE)
        Label(frame1, image=self.logo, borderwidth=0).grid(row=0, column=0, columnspan=2, pady=40)

        Label(frame1, text="username ", font=(FONT2, 26), fg=BLACK, bg=WHITE).grid(row=1, column=0, sticky="w")
        user = Entry(frame1, font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        user.grid(row=2, column=0, sticky="w")

        Label(frame1, text="password ", font=(FONT2, 26), fg=BLACK, bg=WHITE).grid(row=3, column=0, sticky="w")
        pw = Entry(frame1, font=(FONT1, 30), show='•', fg=BLACK, bg=GREY, bd=0, width=21)
        pw.grid(row=4, column=0, sticky="w")

        Button(frame1, text="LOGIN", font=(FONT2, 20, "bold"), fg=WHITE, bg=DARK, bd=0, activebackground=ORANGE,
            activeforeground=WHITE, width=26, command=lambda: [self.login(user.get(), pw.get()), pw.delete(0, "end"), 
                user.delete(0, "end")]).grid(row=5, column=0, columnspan=2, pady=20)
        frame1.pack()

        frame2 = Frame()
        frame2.configure(bg=WHITE)
        Label(frame2, text="Don't have an account?", font=(FONT1, 24), fg=BLUE, bg=WHITE, bd=0).grid(row=0, column=0, pady=4)

        Button(frame2, text="Register", font=(FONT1, 24, "bold"), bg=WHITE, fg=DARK, bd=0, activebackground=WHITE,
            activeforeground=ORANGE, command=self.register).grid(row=0, column=1)
        frame2.pack()

    @staticmethod
    def check_password(pw, hashed):
        encoded = pw.encode("utf-8")
        return bcrypt.checkpw(encoded, hashed)

    def login(self, username, pw1):
        if len(username) != 0 and len(pw1) != 0:
            con = sqlite3.connect(DATA)
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE user = ?", (username,))
            row = cur.fetchone()
            if row and self.check_password(pw1, row[1]):
                budget = row[2]
                MainPage(self, username, budget) # Successful login, load user homepage.
                cur.close()
                con.close()
            else:
                messagebox.showerror("Try again", "Incorrect username or password")
        else:
            messagebox.showerror("Try again", "Fields cannot be empty")

    def register(self):
        RegisPage(self) # Load a registration page.


class RegisPage(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.iconbitmap("assets/logo.ico")
        self.title("slice- REGISTER")
        self.geometry("1000x600+1000+500")
        self.configure(bg=WHITE)

        frame1 = Frame(self)
        frame1.configure(bg=WHITE)
        Label(frame1, text="\nCreate a new account", font=(FONT2, 30, "bold"), fg=BLUE, bg=WHITE)\
            .grid(row=0, column=0, pady=10)

        Label(frame1, text="username", font=(FONT2, 26), fg=BLACK, bg=WHITE).grid(row=1, column=0, sticky="w")
        user = Entry(frame1, font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        user.grid(row=2, column=0, sticky="w")

        Label(frame1, text="password", font=(FONT2, 26), fg=BLACK, bg=WHITE).grid(row=3, column=0, sticky="w")
        pw1 = Entry(frame1, show='•', font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        pw1.grid(row=4, column=0, sticky="w")

        Label(frame1, text="confirm password", font=(FONT2, 26), fg=BLACK, bg=WHITE)\
            .grid(row=5, column=0, sticky="w")
        pw2 = Entry(frame1, show='•', font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        pw2.grid(row=6, column=0, sticky="w")

        Button(frame1, text="REGISTER", font=(FONT2, 20, "bold"), fg=WHITE, bg=DARK, bd=0, activebackground=ORANGE,
            activeforeground=WHITE, width=26, command=lambda: self.add_user(user.get(), pw1.get(), pw2.get()))\
                .grid(row=7, column=0, pady=20, sticky="w")
        frame1.pack()

        frame2 = Frame(self)
        frame2.configure(bg=WHITE)
        Label(frame2, text="Already have an account?", font=(FONT1, 24), fg=BLUE, bg=WHITE, bd=0,)\
            .grid(row=0, column=0, pady=4)

        Button(frame2, text="Login", font=(FONT1, 24, "bold"), bg=WHITE, fg=DARK, bd=0, activebackground=WHITE,
            activeforeground=ORANGE, command=self.destroy).grid(row=0, column=1)
        frame2.pack()

    @staticmethod
    def hash_password(pw):
        encoded = pw.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded, salt)
        return hashed

    # Add new user login info to database.
    def add_user(self, username, pw1, pw2):
        if len(username) == 0 or len(pw1) == 0 or len(pw2) == 0:
            messagebox.showerror("Try again", "Fields cannot be empty", parent=self)
        elif pw1 != pw2:
            messagebox.showerror("Try again", "Passwords do not match", parent=self)
        else:
            con = sqlite3.connect(DATA)
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE user = ?", (username,))  # Check username uniqueness.
            if not cur.fetchall():
                cur.execute("INSERT INTO users (user, pw, budget) VALUES (?, ?, 0)", (username, self.hash_password(pw1)))
                cur.execute("CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, exp_inc TEXT, trn_date DATE, "
                    "category TEXT, notes TEXT, amount REAL)".format('u' + username))
                # Prefix 'u' to prevent errors from table names starting with numbers.
                con.commit()
                messagebox.showinfo("Success", "Your account is ready", parent=self)
                self.destroy()
            else:
                messagebox.showerror("Try again", "This username is taken", parent=self)
            cur.close()
            con.close()


class MainPage(Toplevel):
    def __init__(self, parent, user, budget):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.month_budget = budget
        self.month_expense = self.calculate_total("expenses", "%Y-%m")
        self.month_income = self.calculate_total("income", "%Y-%m")
        self.year_expense = self.calculate_total("expenses", "%Y")
        self.year_income = self.calculate_total("income", "%Y")
        self.logo = PhotoImage(file="assets/logo.png")
        self.up = PhotoImage(file="assets/up.png")
        self.down = PhotoImage(file="assets/down.png")
        self.title("slice- HOME")
        self.iconbitmap("assets/logo.ico")
        self.geometry("2200x1300+300+200")
        self.configure(bg=WHITE)

        # Allow cells to fill window.
        for r in range(4):
            self.grid_rowconfigure(r, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Menu buttons at the top:
        frame1 = Frame(self)
        frame1.configure(bg=WHITE)

        Label(frame1, image=self.logo, borderwidth=0).grid(row=0, column=0, padx=50, pady=30)

        Button(frame1, text="EDIT  INCOME", font=(FONT2, 30, "bold"), fg=WHITE, bg=GREEN, bd=0, width=15,
            command=lambda: EditPage(self, "income", self.user), activeforeground=WHITE, activebackground=ORANGE)\
                .grid(row=0, column=1)

        Button(frame1, text="EDIT  EXPENSES", font=(FONT2, 30, "bold"), fg=WHITE, bg=ORANGE, bd=0, width=15,
            command=lambda: EditPage(self, "expenses", self.user), activeforeground=WHITE, activebackground=ORANGE)\
                .grid(row=0, column=2, padx=50)

        Button(frame1, text="ANALYTICS", font=(FONT2, 30, "bold"), fg=WHITE, bg=BLUE, bd=0, width=15,
            command=lambda: Analytics(self, self.user), activebackground=ORANGE, activeforeground=WHITE)\
                .grid(row=0, column=3)

        frame1.grid(row=0, column=0, columnspan=2, pady=40, padx=20)

        # Display current month's summary:
        frame2 = Frame(self)
        frame2.configure(bg=WHITE)
        Label(frame2, text=datetime.now().strftime('%B').upper() + " BALANCE", font=(FONT1, 30, 'bold'), fg=BLACK,
            bg=WHITE).grid(row=0, column=0, columnspan=5)

        Label(frame2, text="{:.2f}".format(float(self.month_income) - float(self.month_expense)),
            font=(FONT2, 60, 'bold'), fg=BLUE, bg=WHITE).grid(row=1, column=0, columnspan=5, pady=10)

        Label(frame2, image=self.up, borderwidth=0).grid(row=2, column=0)
        Label(frame2, text="{:.2f}".format(float(self.month_income)), font=(FONT2, 40), fg=GREEN, bg=WHITE)\
            .grid(row=2, column=1)

        Label(frame2, text="", background=WHITE, width=2).grid(row=2, column=2)
        Label(frame2, image=self.down, borderwidth=0).grid(row=2, column=3)
        Label(frame2, text="{:.2f}".format(float(self.month_expense)),
            font=(FONT2, 40), fg=ORANGE, bg=WHITE).grid(row=2, column=4)
        frame2.grid(row=1, column=0)

        # Display current year's summary:
        frame3 = Frame(self)
        frame3.configure(bg=WHITE)
        Label(frame3, text=datetime.now().strftime('%Y').upper() + " BALANCE", font=(FONT1, 30, 'bold'), fg=BLACK,
            bg=WHITE).grid(row=0, column=0, columnspan=5)

        Label(frame3, text="{:.2f}".format(float(self.year_income) - float(self.year_expense)),
            font=(FONT2, 60, 'bold'), fg=BLUE, bg=WHITE).grid(row=1, column=0, columnspan=5, pady=10)

        Label(frame3, image=self.up, borderwidth=0).grid(row=2, column=0)
        Label(frame3, text="{:.2f}".format(float(self.year_income)), font=(FONT2, 40),
            fg=GREEN, bg=WHITE).grid(row=2, column=1)

        Label(frame3, text="", background=WHITE, width=2).grid(row=2, column=2)
        Label(frame3, image=self.down, borderwidth=0).grid(row=2, column=3)
        Label(frame3, text="{:.2f}".format(float(self.year_expense)),
            font=(FONT2, 40), fg=ORANGE, bg=WHITE).grid(row=2, column=4)
        frame3.grid(row=1, column=1, pady=42)

        # Monthly budget tool:
        frame4 = Frame(self)
        frame4.configure(bg=WHITE)
        Label(frame4, text=datetime.now().strftime('%B').upper() + ' BUDGET', font=(FONT1, 30, 'bold'),
            fg=BLACK, bg=WHITE).grid(row=0, column=0, sticky='w')

        Button(frame4, text='Edit budget', font=(FONT1, 26), fg=BLUE, bg=WHITE, bd=0,
            activebackground=WHITE, activeforeground=ORANGE, command=self.set_month_budget)\
                .grid(row=0, column=1, columnspan=2, sticky="e")

        # Set progress bar status for monthly budget tool.
        bar = ttk.Progressbar(frame4, style="CustomStyle.Horizontal.TProgressbar", orient="horizontal", length=500,
            mode="determinate")
        try:
            remaining = int((1 - float(self.month_expense)/float(self.month_budget)) * 100)
            if remaining >= 0:
                bar["value"] = remaining
            else:
                bar["value"] = 0
        except ZeroDivisionError:
            bar["value"] = 0

        color = ttk.Style()
        color.theme_use("alt")

        # Progress bar color based on remaining budget percentage.
        if bar["value"] >= 20:
            color.configure("CustomStyle.Horizontal.TProgressbar", troughcolor=GREY, background=GREEN, bordercolor=GREY,
                darkcolor=GREEN, lightcolor=GREEN)
        else:
            color.configure("CustomStyle.Horizontal.TProgressbar", troughcolor=GREY, background=ORANGE,
                bordercolor=GREY, darkcolor=ORANGE, lightcolor=ORANGE)
        bar.grid(row=1, column=0, columnspan=2)

        Label(frame4, text=" {:.2f}".format(float(self.month_budget)), font=(FONT2, 30, "bold"), fg=BLUE, bg=WHITE) \
            .grid(row=1, column=2, sticky="w")

        Label(frame4, text="spent {:.2f},  remaining".format(float(self.month_expense)),
            font=(FONT1, 30), fg=DARK, bg=WHITE).grid(row=2, column=0, sticky="w")

        # Color of remaining budget text based on negativity.
        remaining = float(self.month_budget) - float(self.month_expense)
        if remaining > 0:
            Label(frame4, text="{:.2f}".format(remaining), font=(FONT2, 30, 'underline', 'bold'), fg=DARK, bg=WHITE)\
                .grid(row=2, column=1, columnspan=2, sticky="w")
        else:
            Label(frame4, text="{:.2f}".format(remaining), font=(FONT2, 30, 'underline', 'bold'), fg=ORANGE, bg=WHITE)\
                .grid(row=2, column=1, columnspan=2, sticky="w")
        frame4.grid(row=2, column=0, columnspan=2)

        # Today's transactions dashboard on the right:
        frame5 = Frame(self)
        frame5.configure(bg=GREY)
        
        Label(frame5, text=("Hello, " + self.user), font=(FONT2, 40, "bold"), fg=BLUE, bg=GREY, bd=0)\
            .grid(row=0, column=0, sticky="w", padx=30, pady=50)

        Label(frame5, text=("Today is " + datetime.now().strftime("%B %d, %Y")), font=(FONT1, 30),
            fg=BLACK, bg=GREY, bd=0).grid(row=1, column=0, sticky="w", padx=20)

        Label(frame5, text="TRANSACTIONS", font=(FONT1, 30, "bold"),
            fg=BLACK, bg=GREY, bd=0).grid(row=2, column=0, sticky="w", padx=20, pady=20)

        tree = ttk.Style()
        tree.configure("Treeview", font=(FONT1, 24))
        tree.configure("Treeview.Heading", font=(FONT1, 24, "bold"))
        tree.configure('Treeview', rowheight=35)
        tree.map("Treeview", background=[('selected', ORANGE)])

        columns = ("notes", "amount")
        self.tree_table = ttk.Treeview(frame5, show="headings", height=37)
        self.tree_table.configure(columns=columns)
        self.tree_table.heading("notes", text="Notes", anchor="w")
        self.tree_table.column("notes", width=300, minwidth=50)
        self.tree_table.heading("amount", text="Amount", anchor="w")
        self.tree_table.column("amount", width=800, minwidth=50)
        self.tree_table.grid(row=3, column=0, sticky="w", padx=20)

        con = sqlite3.connect(DATA)
        cur = con.cursor()
        cur.execute("SELECT * FROM {} WHERE trn_date = DATE('now')".format('u' + self.user))
        rows = cur.fetchall()
        for row in rows:
            index = row[0]
            exp_inc = row[1]
            category = row[3]
            notes = row[4]
            amount = "{:.2f}".format(float(row[5]))

            # Tags for tree_table text color based on exp_inc.
            if exp_inc == "income":
                tag = "inc"
                amount = '+' + amount
            elif exp_inc == "expenses":
                tag = "exp"
                amount = '-' + amount

            # First column = notes or category (if no note was input).
            # Second column = amount.
            if notes != "":
                self.tree_table.insert(parent='', index=0, iid=str(index), text='', values=(notes, amount), tags=(tag,))
            else:
                self.tree_table.insert(parent='', index=0, iid=str(index), text='', values=(category, amount), tags=(tag,))
            self.tree_table.tag_configure("inc", foreground=GREEN) # Display income in green.
            self.tree_table.tag_configure("exp", foreground=ORANGE) # Display expenses in orange.

        cur.close()
        con.close()
        frame5.grid(row=0, rowspan=4, column=2, sticky="nsew") # Allow cell to fill available space on the right.

        frame6 = Frame(self)
        frame6.configure(bg=WHITE)
        Button(frame6, text="LOG OUT", font=(FONT1, 22, "bold"), bg=BLUE, fg=WHITE, bd=0, activebackground=ORANGE,
            activeforeground=WHITE, width=12, command=self.logout).grid(row=0, column=0, padx=15, pady=15)
        frame6.grid(row=3, column=1, sticky="se")

    # Total calculation for month/year summary:
    def calculate_total(self, exp_inc, fmt):
        con = sqlite3.connect(DATA)
        cur = con.cursor()
        cur.execute("SELECT * FROM {} WHERE exp_inc = ? AND strftime(?, trn_date) = strftime(?, 'now')"
            .format('u' + self.user), (exp_inc, fmt, fmt))
        rows = cur.fetchall()
        amount = 0
        for row in rows:
            amount += float(row[5])
        cur.close()
        con.close()
        return amount

    # Destroys all windows except 'LoginPage'.
    def logout(self):
        for window in self.parent.winfo_children():
            if isinstance(window, Toplevel):
                window.destroy()

    def set_month_budget(self):
        BudgetPage(self, self.user, self.month_income)

    # Keeps the 'MainPage' updated after 'EditPage' makes changes to 'DATA'.
    # 'MainPage' will not be updated if window's close/X button is used instead of 'GO BACK'.
    # This function is called from the 'EditPage' and 'BudgetPage':
    def refresh(self):
        try:
            self.destroy() # Destroy current MainPage.
        except AttributeError:
            pass
        MainPage(self.parent, self.user, self.month_budget) # Create new MainPage.


# Monthly budget tool:
class BudgetPage(Toplevel):
    def __init__(self, parent, user, month_income):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.month_income = month_income
        self.title("slice- BUDGET")
        self.iconbitmap("assets/logo.ico")
        self.geometry("1000x600+1000+500")
        self.configure(bg=WHITE)

        frame1 = Frame(self)
        frame1.configure(bg=WHITE)
        Label(frame1, text="\nMonthly Budget Calculator", font=(FONT1, 30, "bold"), fg=BLUE, bg=WHITE)\
            .grid(row=0, column=0, columnspan=3, sticky="w")
        Label(frame1, text='savings goal', font=(FONT2, 26), bg=WHITE).grid(row=1, column=0, sticky="w")

        tool = Entry(frame1, font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        tool.grid(row=2, column=0)

        Button(frame1, text="AMT", font=(FONT1, 20, "bold"), fg=WHITE, bg=BLUE, bd=0, width=7, activebackground=ORANGE,
            activeforeground=WHITE, command=lambda: self.get_amt(tool.get())).grid(row=2, column=1, padx=15)

        Button(frame1, text="INC%", font=(FONT1, 20, "bold"), fg=WHITE, bg=BLUE, bd=0, width=7, activebackground=ORANGE,
            activeforeground=WHITE, command=lambda: self.get_percent(tool.get())).grid(row=2, column=2, sticky="w")

        Label(frame1, text="\n\nmonthly budget ", font=(FONT2, 26), fg=BLACK, bg=WHITE).grid(row=3, column=0, sticky="w")
        
        self.budget_input = Entry(frame1, font=(FONT1, 30), fg=BLACK, bg=GREY, bd=0, width=21)
        self.budget_input.grid(row=4, column=0, sticky="w")

        Button(frame1, text="SET", font=(FONT1, 20, "bold"), fg=WHITE, bg=DARK, bd=0, width=16, activebackground=ORANGE,
            activeforeground=WHITE, command=self.set_budget).grid(row=4, column=1, columnspan=2, padx=15, sticky="w")
        frame1.pack()

        frame2 = Frame(self)
        frame2.configure(bg=WHITE)
        Label(frame2, text="Click SET to save changes or ", font=(FONT1, 24), fg=BLUE, bg=WHITE, bd=0,)\
            .grid(row=0, column=0)

        Button(frame2, text="Cancel", font=(FONT1, 24, "bold"), bg=WHITE, fg=DARK, bd=0, activebackground=WHITE,
            activeforeground=ORANGE, command=self.destroy).grid(row=0, column=1, pady=5, padx=5)
        frame2.pack(side="bottom", anchor="e")

    # Calculates budget based on savings amount.
    def get_amt(self, tool):
        if len(tool) != 0:
            try:
                budget = "{:.2f}".format(float(self.month_income) - float(tool))
            except ValueError:
                messagebox.showerror("Try again", "Amount must be numerical", parent=self)
            else:
                # Calculated amount added to 'budget' input box.
                self.budget_input.delete(0, "end")
                self.budget_input.insert("end", budget)
        else:
            messagebox.showerror("Try again", "Enter the amount you want to save this month", parent=self)

    # Calculates budget based on percentage of income.
    def get_percent(self, tool):
        if len(tool) != 0:
            try:
                budget = "{:.2f}".format(((100-float(tool)) / 100) * float(self.month_income))
            except ValueError:
                messagebox.showerror("Try again", "Amount must be numerical", parent=self)
            else:
                # Calculated amount added to 'budget' input box.
                self.budget_input.delete(0, "end")
                self.budget_input.insert("end", budget)
        else:
            messagebox.showerror("Try again", "Enter the percentage of your income you want to save this month",
                parent=self)

    def set_budget(self):
        if len(self.budget_input.get()) != 0:
            try:
                if float(self.budget_input.get()) >= 0:
                    # Modify user's monthly budget in database:
                    self.parent.month_budget = self.budget_input.get()
                    con = sqlite3.connect(DATA)
                    cur = con.cursor()
                    cur.execute("UPDATE users SET budget = ? WHERE user = ?", (self.budget_input.get(), self.user))
                    con.commit()
                    cur.close()
                    con.close()
                    # Refresh MainPage to update data:
                    self.parent.refresh()
                else:
                    messagebox.showerror("Try again", "Budget cannot be negative\nMake sure the amount you want to"
                        " save is not more than your income", parent=self)
            except ValueError:
                messagebox.showerror("Try again", "Amount must be numerical", parent=self)
        else:
            messagebox.showerror("Try again", "Enter your preferred expense budget this month\nOr use the tool"
                " above to calculate a budget based on how much you would like to save", parent=self)


# 'EditPage' is called for both editing expense and editing income
class EditPage(Toplevel):
    def __init__(self, parent, exp_inc, user):
        super().__init__(parent)
        self.parent = parent
        self.exp_inc = exp_inc # Transaction type: expense or income.
        self.user = 'u' + user
        self.title("slice- " + self.exp_inc.upper())
        self.iconbitmap("assets/logo.ico")
        self.geometry("2200x1300+300+200")
        self.configure(bg=WHITE)
        self.category_types = []

        con = sqlite3.connect(DATA)
        cur = con.cursor()
        if self.exp_inc == "expenses":
            cur.execute("SELECT category FROM expense_types")
            for category in cur.fetchall():
                self.category_types.append(category[0])
        elif self.exp_inc == "income":
            cur.execute("SELECT category FROM income_types")
            for category in cur.fetchall():
                self.category_types.append(category[0])

        frame1 = Frame(self)
        frame1.configure(bg=WHITE)
        Label(frame1, text="YOUR " + self.exp_inc.upper() + "\t       ", font=(FONT2, 35, "bold"), fg=DARK,
            bg=WHITE).grid(row=0, column=0, padx=20, pady=20)

        # Data filter tool by date range.
        Label(frame1, text="From ", font=(FONT1, 28), fg=DARK, bg=WHITE, bd=0).grid(row=0, column=1)

        self.start_date = DateEntry(frame1, selectmode="day", font=(FONT1, 24), date_pattern="yyyy-mm-dd", 
            width=20, showweeknumbers=False, showothermonthdays=False, foreground=BLACK, background=GREY, 
                normalforeground=BLACK, selectbackground=ORANGE, normalbackground=WHITE, weekendbackground=WHITE,
                    weekendforeground=BLACK, bordercolor=GREY, headersbackground=GREY)
        self.start_date.grid(row=0, column=2)

        Label(frame1, text=" to ", font=(FONT1, 28), fg=DARK, bg=WHITE).grid(row=0, column=3)

        self.end_date = DateEntry(frame1, selectmode="day", font=(FONT1, 24), date_pattern="yyyy-mm-dd", 
            width=20, showweeknumbers=False, showothermonthdays=False, foreground=BLACK, background=GREY, 
                normalforeground=BLACK, selectbackground=ORANGE, normalbackground=WHITE, weekendbackground=WHITE,
                    weekendforeground=BLACK, bordercolor=GREY, headersbackground=GREY)
        self.end_date.grid(row=0, column=4)

        self.start_date.delete(0, "end")
        self.end_date.delete(0, "end")

        Button(frame1, text="FILTER", font=(FONT1, 20, "bold"), fg=WHITE, bg=DARK, bd=0, activebackground=ORANGE, 
            activeforeground=WHITE, command=self.filter_date, width=10).grid(row=0, column=5, padx=30)

        Button(frame1, text="SHOW ALL", font=(FONT1, 20, "bold"), fg=WHITE, bg=DARK, bd=0, activeforeground=WHITE,
               activebackground=ORANGE, command=self.revert_filter, width=10).grid(row=0, column=6)
        frame1.pack(side="top", padx=20)

        frame2 = Frame(self)
        frame2.configure(bg=WHITE)
        tree = ttk.Style()
        tree.theme_use("vista")
        tree.configure("Treeview", font=(FONT1, 24))
        tree.configure("Treeview.Heading", font=(FONT1, 24, "bold"))
        tree.configure('Treeview', rowheight=35)
        tree.map("Treeview", background=[('selected', ORANGE)])

        columns = ("date", "category", "notes", "amount")
        self.tree_table = ttk.Treeview(frame2, show="headings", height=25)
        self.tree_table.configure(columns=columns)
        self.tree_table.pack()
        self.tree_table.heading("date", text="Date", anchor="w")
        self.tree_table.column("date", width=300, minwidth=50)
        self.tree_table.heading("category", text="Category", anchor="w")
        self.tree_table.column("category", width=400, minwidth=50)
        self.tree_table.heading("notes", text="Notes", anchor="w")
        self.tree_table.column("notes", width=1000, minwidth=50)
        self.tree_table.heading("amount", text="Amount", anchor="w")
        self.tree_table.column("amount", width=400, minwidth=50)

        # Orders table rows by most recent date first.
        cur.execute("SELECT * FROM {} WHERE exp_inc = ? ORDER BY trn_date".format(self.user), (self.exp_inc,))
        rows = cur.fetchall()
        for row in rows:
            index = row[0]
            date = row[2]
            category = row[3]
            notes = row[4]
            amount = "{:.2f}".format(float(row[5]))
            self.tree_table.insert(parent='', index=0, iid=str(index), text='', values=(date, category, notes, amount))
        cur.close()
        con.close()
        frame2.pack(pady=7)

        frame3 = Frame(self)
        frame3.configure(bg=WHITE)

        Label(frame3, font=(FONT2, 26), text="\tdate ", fg=BLACK, bg=WHITE, bd=0).grid(row=0, column=0)
        self.date_entry = DateEntry(frame3, selectmode="day", font=(FONT1, 24), date_pattern="yyyy-mm-dd", 
            width=20, showweeknumbers=False, showothermonthdays=False, foreground=BLACK, background=GREY, 
                normalforeground=BLACK, selectbackground=ORANGE, normalbackground=WHITE, weekendbackground=WHITE,
                    weekendforeground=BLACK, bordercolor=GREY, headersbackground=GREY)
        self.date_entry.grid(row=0, column=1, pady=10)

        Label(frame3, font=(FONT2, 26), text="         notes ", fg=BLACK, bg=WHITE, bd=0).grid(row=0, column=2)
        self.notes = Entry(frame3, font=(FONT1, 26), fg=BLACK, bg=GREY, bd=0)
        self.notes.grid(row=0, column=3, padx=5)

        Label(frame3, font=(FONT2, 26), text='       category ', fg=BLACK, bg=WHITE, bd=0).grid(row=1, column=0)
        self.drop = ttk.Combobox(frame3, state="readonly", values=self.category_types)
        self.option_add("*TCombobox*Listbox.selectBackground", ORANGE)
        self.option_add("*TCombobox*Listbox*Font", (FONT1, 24))
        self.drop.set(self.category_types[0])
        self.drop.configure(width=20, font=(FONT1, 24))
        self.drop.grid(row=1, column=1)

        Label(frame3, font=(FONT2, 26), text="     amount ", fg=BLACK, bg=WHITE, bd=0).grid(row=1, column=2)
        self.amount = Entry(frame3, font=(FONT1, 26), fg=BLACK, bg=GREY, bd=0)
        self.amount.grid(row=1, column=3)

        Button(frame3, font=(FONT2, 22, 'bold'), text="ADD" + " " + self.exp_inc.upper(), fg=WHITE, bg=GREEN,
            activeforeground=WHITE, activebackground=ORANGE, bd=0, width=18,
                command=lambda: self.add_data(self.date_entry.get_date().strftime("%Y-%m-%d"), self.notes.get(), 
                    self.drop.get(), self.amount.get())).grid(row=0, column=4, padx=60, sticky="w", pady=20)

        Button(frame3, font=(FONT2, 22, 'bold'), text="REMOVE" + " " + self.exp_inc.upper(), fg=WHITE, bg=ORANGE,
            activeforeground=WHITE, activebackground=ORANGE, bd=0, width=18, command=self.remove_data) \
                .grid(row=1, column=4, padx=60, sticky="w")
        frame3.pack()

        # 'MainPage' will not be updated if window's close/X is used instead of 'GO BACK'.
        Button(self, text="GO BACK", font=(FONT1, 22, "bold"), fg=WHITE, bg=BLUE, bd=0, activebackground=ORANGE, 
            activeforeground=WHITE, command=self.parent.refresh, width=12).pack(side="bottom", anchor="e", padx=15, pady=15)

    def add_data(self, input_date, notes, category, amount):
        if len(input_date) != 0 and len(amount) != 0:
            try:
                if float(amount) <= 0:
                    messagebox.showerror("Try again", "Amount must be more than 0", parent=self)
            except ValueError:
                messagebox.showerror("Try again", "Amount must be numerical", parent=self)
            else:
                try:
                    formatted_date = str(datetime.strptime(input_date, "%Y-%m-%d").date())
                except ValueError:
                    messagebox.showerror("Try again", "Not a valid date", parent=self)
                else:
                    con = sqlite3.connect(DATA)
                    cur = con.cursor()
                    cur.execute("SELECT MAX(id) FROM {}".format(self.user))
                    max_id = cur.fetchone()[0]
                    if max_id is None:  # handle when table is empty
                        max_id = 0
                    iid = max_id + 1
                    formatted_amount = "{:.2f}".format(float(amount))
                    # Add to tree_table. New log is inserted to top row of table.
                    self.tree_table.insert(parent='', index=0, iid=str(iid), text='',
                        values=(formatted_date, category, notes, formatted_amount))
                    # Add to database:
                    cur.execute("INSERT INTO {} (exp_inc, trn_date, category, notes, amount) VALUES (?, ?, ?, ?, ?)"
                        .format(self.user), (self.exp_inc, formatted_date, category, notes, formatted_amount))
                    con.commit()
                    cur.close()
                    con.close()
                    # Clear input fields for next input.
                    self.amount.delete(0, "end")
                    self.notes.delete(0, "end")
                    self.drop.set(self.category_types[0])
        else:
            messagebox.showerror("Try again", "Please enter the date and amount", parent=self)

    def remove_data(self):
        selected = self.tree_table.selection()
        if len(selected) != 0:
            con = sqlite3.connect(DATA)
            cur = con.cursor()
            for selection in selected:
                # Remove from database:
                cur.execute("DELETE FROM {} WHERE id = ?".format(self.user), (selection,))
                # Remove from tree_table:
                self.tree_table.delete(selection)
            con.commit()
            cur.close()
            con.close()
        else:
            messagebox.showerror("Try again", "Please select row(s) to remove from the table above\n"
                "For Windows: Ctrl + click row(s)\nFor Mac: Command + click row(s)", parent=self)

    def filter_date(self):
        start = self.start_date.get_date().strftime("%Y-%m-%d")
        end = self.end_date.get_date().strftime("%Y-%m-%d")
        if len(start) != 0 and len(end) != 0:
            try:
                start = str(datetime.strptime(start, "%Y-%m-%d").date())
                end = str(datetime.strptime(end, "%Y-%m-%d").date())
            except ValueError:
                messagebox.showerror("Try again", "Not a valid date", parent=self)
            else:
                for clear in self.tree_table.get_children():
                    self.tree_table.delete(clear)
                con = sqlite3.connect(DATA)
                cur = con.cursor()
                cur.execute("SELECT * FROM {} WHERE exp_inc = ? AND trn_date BETWEEN ? AND ? ORDER BY trn_date"\
                    .format(self.user), (self.exp_inc, start, end))
                rows = cur.fetchall()
                for row in rows:
                    index = row[0]
                    date = row[2]
                    category = row[3]
                    notes = row[4]
                    amount = "{:.2f}".format(float(row[5]))
                    self.tree_table.insert(parent='', index=0, text='', iid=str(index),
                        values=(date, category, notes, amount))
        else:
            messagebox.showerror("Try again", "Please enter a start and end date", parent=self)

    # revert_filter is used to show all data.
    def revert_filter(self):
        try:
            con = sqlite3.connect(DATA)
            cur = con.cursor()
            cur.execute("SELECT MIN(trn_date) FROM {} WHERE exp_inc = ?".format(self.user), (self.exp_inc,))
            min_date = cur.fetchone()[0]
            cur.execute("SELECT MAX(trn_date) FROM {} WHERE exp_inc = ?".format(self.user), (self.exp_inc,))
            max_date = cur.fetchone()[0]
            cur.close()
            con.close()
        except (TypeError, AttributeError):
            return
        else:
            self.start_date.delete(0, "end")
            self.end_date.delete(0, "end")
            try:
                max_date = datetime.strptime(max_date, '%Y-%m-%d')
                min_date = datetime.strptime(min_date, '%Y-%m-%d')
                # Sets date range input boxes to the oldest and newest log date in the user's db table.
                self.start_date.insert("end", str(min_date.strftime("%Y-%m-%d")))
                self.end_date.insert("end", str(max_date.strftime("%Y-%m-%d")))
                # Refreshes 'MainPage'.
                self.filter_date()
            except TypeError:
                pass


class Analytics(Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = 'u' + user
        self.title("slice- ANALYTICS")
        self.iconbitmap("assets/logo.ico")
        self.geometry("2200x1300+300+200")
        self.configure(bg=WHITE)
        self.chart_type = StringVar()
        self.chart_time = StringVar()

        self.bar_fig = plt.Figure(figsize=(17, 7))
        self.bar_ax = self.bar_fig.add_subplot()
        self.pie_fig = plt.Figure(figsize=(17, 7))
        self.pie_ax = self.pie_fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(figure=self.bar_fig, master=self)
        # self.canvas is used to display both bar and pie chart (one at a time).

        # Default chart selection.
        self.chart_type.set("OVERVIEW")
        self.chart_time.set("DAY")
        self.refresh_chart()

        # Radio button set 1 to control 'chart_type'.
        frame1 = Frame(self)
        frame1.configure(background=WHITE)
        Label(frame1, text="MODE", font=(FONT1, 33, "bold"), fg=DARK, bg=WHITE).grid(row=0, column=0)

        rb_overview = Radiobutton(frame1, text="OVERVIEW", indicatoron=0, width=17, value="OVERVIEW",
            variable=self.chart_type, command=self.refresh_chart)
        rb_overview.configure(foreground=WHITE, background=BLUE, activeforeground=WHITE, activebackground=ORANGE,
            selectcolor=ORANGE, borderwidth=0, font=(FONT2, 30, "bold"))
        rb_overview.grid(row=1, column=0, pady=20)

        rb_expenses = Radiobutton(frame1, text="EXPENSES", indicatoron=0, width=17, value="EXPENSES",
            variable=self.chart_type, command=self.refresh_chart)
        rb_expenses.configure(foreground=WHITE, background=BLUE, activeforeground=WHITE, activebackground=ORANGE,
            selectcolor=ORANGE, borderwidth=0, font=(FONT2, 30, "bold"))
        rb_expenses.grid(row=2, column=0)
        frame1.grid(row=0, column=1, rowspan=2, pady=200, stick="n")

        # Radio button set 2 to control 'chart_time'.
        frame2 = Frame(self)
        frame2.configure(bg=WHITE)
        Label(frame2, text="TIMESPAN", font=(FONT1, 33, "bold"), fg=DARK, bg=WHITE).grid(row=0, column=0)

        rb_day = Radiobutton(frame2, text="DAY", indicatoron=0, width=17, value="DAY", variable=self.chart_time,
            command=self.refresh_chart)
        rb_day.configure(foreground=WHITE, background=BLUE, activeforeground=WHITE, activebackground=ORANGE,
            selectcolor=ORANGE, borderwidth=0, font=(FONT2, 30, "bold"))
        rb_day.grid(row=1, column=0)

        rb_month = Radiobutton(frame2, text="MONTH", indicatoron=0, width=17, value="MONTH", variable=self.chart_time,
            command=self.refresh_chart)
        rb_month.configure(foreground=WHITE, background=BLUE, activeforeground=WHITE, activebackground=ORANGE,
            selectcolor=ORANGE, borderwidth=0, font=(FONT2, 30, "bold"))
        rb_month.grid(row=2, column=0, pady=20)

        rb_year = Radiobutton(frame2, text="YEAR", indicatoron=0, width=17, value="YEAR", variable=self.chart_time,
            command=self.refresh_chart)
        rb_year.configure(foreground=WHITE, background=BLUE, activeforeground=WHITE, activebackground=ORANGE,
            selectcolor=ORANGE, borderwidth=0, font=(FONT2, 30, "bold"))
        rb_year.grid(row=3, column=0)
        frame2.grid(row=2, column=1, sticky="n")

        frame3 = Frame(self)
        frame3.configure(bg="WHITE")
        Button(frame3, text="  GO BACK  ", font=(FONT1, 22, "bold"), bg=BLUE, fg=WHITE, bd=0, width=12,
            activebackground=ORANGE, activeforeground=WHITE, command=self.destroy).grid(row=1, column=0, padx=10, pady=10)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        frame3.grid(row=3, column=1, padx=5, pady=5, sticky="se")

    def refresh_chart(self):
        chart_type = self.chart_type.get()
        chart_time = self.chart_time.get()
        self.bar_ax.clear()
        self.pie_ax.clear()

        if chart_type == "OVERVIEW":
            self.draw_bar_chart(chart_time)
        elif chart_type == "EXPENSES":
            self.draw_pie_chart(chart_time)

        self.canvas.draw()

    # Calculates display data for bar chart.
    # Called separately for income and expense.
    def calculate_type_total(self, type_choice, fmt, prev):
        con = sqlite3.connect(DATA)
        cur = con.cursor()
        # Checks that row in 'DATA' is in desired range.
        cur.execute("SELECT * FROM {} WHERE exp_inc = ? AND strftime(?, trn_date) = strftime(?, ?)".format(self.user),
            (type_choice, fmt, fmt, prev))
        rows = cur.fetchall()
        amount = 0
        for row in rows:
            amount += float(row[5])
        cur.close()
        con.close()
        return amount

    # Calculates display data for pie chart.
    # Called separately for each expense category.
    def calculate_category_total(self, category, fmt):
        con = sqlite3.connect(DATA)
        cur = con.cursor()
        # Checks that row in 'DATA' is in desired timeframe and category.
        cur.execute("SELECT * FROM {} WHERE exp_inc = 'expenses' AND category = ? "
            "AND strftime(?, trn_date) = strftime(?, 'now')".format(self.user), (category, fmt, fmt))
        rows = cur.fetchall()
        amount = 0
        for row in rows:
            amount += float(row[5])
        cur.close()
        con.close()
        return amount

    def draw_bar_chart(self, chart_time):
        self.canvas = FigureCanvasTkAgg(figure=self.bar_fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, sticky="nsew")
        data = {"income": [], "expenses": []}
        data_labels = []

        # Shows data by day for last 7 days.
        if chart_time == "DAY":
            for prev in range(7):
                prev_day = datetime.now() - relativedelta(days=prev)
                data["income"].append(self.calculate_type_total("income", "%Y-%m-%d", prev_day))
                data["expenses"].append(self.calculate_type_total("expenses", "%Y-%m-%d", prev_day))
                data_labels.append(prev_day.strftime("%a\n%m-%d"))

        # Shows data by month for past 6 months.
        elif chart_time == "MONTH":
            for prev in range(6):
                prev_month = datetime.now() - relativedelta(months=prev)
                data["income"].append(self.calculate_type_total("income", "%Y-%m", prev_month))
                data["expenses"].append(self.calculate_type_total("expenses", "%Y-%m", prev_month))
                data_labels.append(prev_month.strftime("%B"))

        # Shows data by year for past 5 years.
        elif chart_time == "YEAR":
            for prev in range(5):
                prev_year = datetime.now() - relativedelta(years=prev)
                data["income"].append(self.calculate_type_total("income", "%Y", prev_year))
                data["expenses"].append(self.calculate_type_total("expenses", "%Y", prev_year))
                data_labels.append(prev_year.year)

        # Reverse because 'append' is used.
        data_labels.reverse()
        data["income"].reverse()
        data["expenses"].reverse()

        bar_width = 0.3
        x1 = range(len(data_labels))
        x2 = [x + bar_width for x in x1]

        self.bar_ax.bar(x1, data["income"], color=GREEN, width=bar_width, label='Total Income')
        self.bar_ax.bar(x2, data["expenses"], color=ORANGE, width=bar_width, label='Total Expenses')
        self.bar_ax.set_xticks([x + bar_width / 2 for x in x1])
        self.bar_ax.set_xticklabels(data_labels, fontsize=20)

        # Disables y-axis labels.
        self.bar_ax.set_yticks([])
        self.bar_ax.set_yticklabels([])

        self.bar_ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncols=2, fontsize=20)
        if data["income"] and data["expenses"]:
            offset = 0.02 * max(max(data["income"]), max(data["expenses"]))
        else:
            offset = 0
        for index, value in enumerate(data["income"]):
            if value != 0:
                self.bar_ax.text(x1[index], offset, "{:.2f}".format(value), ha="center", va="bottom",
                    rotation="vertical", fontsize=20)
        for index, value in enumerate(data["expenses"]):
            if value != 0:
                self.bar_ax.text(x2[index], offset, "{:.2f}".format(value), ha="center", va="bottom",
                    rotation="vertical", fontsize=20)

    def draw_pie_chart(self, chart_time):
        self.canvas = FigureCanvasTkAgg(figure=self.pie_fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, sticky="nsew")
        category_types = []
        data = []
        data_labels = []

        con = sqlite3.connect(DATA)
        cur = con.cursor()
        cur.execute("SELECT category FROM expense_types")
        for category in cur.fetchall():
            category_types.append(category[0])
        cur.close()
        con.close()

        # Shows data for current day.
        if chart_time == "DAY":
            for category in category_types:
                type_total = self.calculate_category_total(category, "%Y-%m-%d")
                if type_total != 0:
                    data.append(type_total)
                    data_labels.append(category)

        # Shows data for current month.
        elif chart_time == "MONTH":
            for category in category_types:
                type_total = self.calculate_category_total(category, "%Y-%m")
                if type_total != 0:
                    data.append(type_total)
                    data_labels.append(category)

        # Shows data for current year.
        elif chart_time == "YEAR":
            for category in category_types:
                type_total = self.calculate_category_total(category, "%Y")
                if type_total != 0:
                    data.append(type_total)
                    data_labels.append(category)

        self.pie_ax.pie(data, labels=data_labels, autopct="", textprops={"size": 20})
        legend_labels = []
        for i in range(len(data_labels)):
            legend_labels.append("{}: {:.2f}".format(data_labels[i], data[i]))
        self.pie_ax.legend(legend_labels, loc="upper right", bbox_to_anchor=(1.1, 1), prop={"size": 20})


if __name__ == "__main__":
    main()
