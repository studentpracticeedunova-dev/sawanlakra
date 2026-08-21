import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import hashlib
import mysql.connector
import smtplib
import random
import csv
import os
from email.message import EmailMessage

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    database="hrms",
    password="root@123",
    use_pure=True
)

cursor = db.cursor()

SENDER_EMAIL = "development.edunova@gmail.com"
APP_PASSWORD = "yfmq aamr widr zfzu"

BG = "#F4F7FB"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
SUCCESS = "#10B981"
INFO = "#06B6D4"
WARNING = "#F59E0B"
DANGER = "#EF4444"

TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"

SIDEBAR = "#0F172A"
SIDEBAR_HOVER = "#1E293B"

employee_file = "employees.csv"
department_count = 1

if not os.path.exists(employee_file):

    with open(employee_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Employee ID",
            "Name",
            "Age",
            "Department"
        ])

root = tk.Tk()

root.title("Employee Management System")
root.geometry("1250x850")
root.minsize(1100, 650)
root.configure(bg=BG)

root.withdraw()

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass


style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=38,
    fieldbackground=WHITE,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=PRIMARY,
    foreground=WHITE,
    font=("Segoe UI", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", TEXT)
    ]
)

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def get_employees():

    employees = []

    if not os.path.exists(employee_file):
        return employees

    with open(employee_file, "r", newline="") as file:

        reader = csv.reader(file)

        next(reader, None)

        for row in reader:

            if len(row) >= 4:
                employees.append(row)

    return employees


def get_next_employee_id():

    employees = get_employees()

    if not employees:
        return "EMP001"

    last_id = employees[-1][0]

    try:
        number = int(
            last_id.replace("EMP", "")
        )

        return f"EMP{number + 1:03d}"

    except:
        return "EMP001"

def signup():

    win = tk.Toplevel(root)

    win.title("Create Account")
    win.geometry("460x560")
    win.configure(bg=BG)
    win.resizable(False, False)

    # Header
    header = tk.Frame(
        win,
        bg=PRIMARY,
        height=110
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="CREATE ACCOUNT",
        font=("Segoe UI", 22, "bold"),
        bg=PRIMARY,
        fg=WHITE
    ).pack(pady=(25, 5))

    tk.Label(
        header,
        text="Register a new employee system account",
        font=("Segoe UI", 10),
        bg=PRIMARY,
        fg="#DBEAFE"
    ).pack()

    # Card
    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    # Username
    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(25, 5)
    )

    username = tk.Entry(
        card,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    username.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    # Email
    tk.Label(
        card,
        text="Email",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    email = tk.Entry(
        card,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    email.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    # Password
    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    password = tk.Entry(
        card,
        font=("Segoe UI", 11),
        show="*",
        bd=1,
        relief="solid"
    )

    password.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    # -------------------------------------------------
    # CREATE ACCOUNT -> SEND OTP
    # -------------------------------------------------

    def create_account():

        u = username.get().strip()
        e = email.get().strip().lower()
        p = password.get()

        # Validation
        if not u or not e or not p:

            messagebox.showerror(
                "Missing Information",
                "Please fill Username, Email and Password.",
                parent=win
            )

            return

        # Basic email validation
        if "@" not in e or "." not in e:

            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address.",
                parent=win
            )

            return

        # Check if username/email already exists
        try:

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username=%s OR LOWER(TRIM(email))=%s
                """,
                (u, e)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                messagebox.showerror(
                    "Already Exists",
                    "Username or Email already exists.",
                    parent=win
                )

                return

        except mysql.connector.Error as db_error:

            messagebox.showerror(
                "Database Error",
                str(db_error),
                parent=win
            )

            return

        # Generate OTP
        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        # Send OTP
        try:

            send_signup_otp_email(
                e,
                otp
            )

            messagebox.showinfo(
                "OTP Sent",
                "OTP has been sent to your email.",
                parent=win
            )

            # Hide create account window
            win.withdraw()

            # Open OTP verification
            verify_signup_otp_window(
                u,
                e,
                p,
                otp,
                win
            )

        except Exception as error:

            messagebox.showerror(
                "Email Error",
                f"OTP could not be sent.\n\n{error}",
                parent=win
            )

    # Create Account Button
    tk.Button(
        card,
        text="CREATE ACCOUNT",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        activebackground=PRIMARY_DARK,
        activeforeground=WHITE,
        bd=0,
        cursor="hand2",
        command=create_account
    ).pack(
        fill="x",
        padx=25,
        pady=30,
        ipady=10
    )


# ---------------------------------------------------------
# SEND SIGNUP OTP EMAIL
# ---------------------------------------------------------

def send_signup_otp_email(receiver_email, otp):

    msg = EmailMessage()

    msg["Subject"] = (
        "Employee Management System - Account Verification OTP"
    )

    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Hello,

Thank you for creating an account in Employee Management System.

Your account verification OTP is:

{otp}

Please do not share this OTP with anyone.

Regards,
Employee Management System
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)


# ---------------------------------------------------------
# VERIFY SIGNUP OTP
# ---------------------------------------------------------

def verify_signup_otp_window(
    username_value,
    email_value,
    password_value,
    correct_otp,
    signup_window
):

    win = tk.Toplevel(root)

    win.title("Verify Account")
    win.geometry("450x420")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="🔑",
        font=("Segoe UI Emoji", 40),
        bg=BG
    ).pack(
        pady=(35, 5)
    )

    tk.Label(
        win,
        text="Verify Your Email",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        win,
        text=f"OTP sent to\n{email_value}",
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED,
        justify="center"
    ).pack(
        pady=10
    )

    otp_entry = tk.Entry(
        win,
        font=("Segoe UI", 18),
        justify="center",
        bd=1,
        relief="solid"
    )

    otp_entry.pack(
        padx=60,
        fill="x",
        ipady=8
    )

    otp_entry.focus()

    # -----------------------------------------------------
    # VERIFY OTP AND CREATE ACCOUNT
    # -----------------------------------------------------

    def verify():

        entered_otp = otp_entry.get().strip()

        if not entered_otp:

            messagebox.showerror(
                "Error",
                "Please enter OTP.",
                parent=win
            )

            return

        if len(entered_otp) != 6 or not entered_otp.isdigit():

            messagebox.showerror(
                "Invalid OTP",
                "OTP must be 6 digits.",
                parent=win
            )

            return

        if entered_otp != correct_otp:

            messagebox.showerror(
                "Invalid OTP",
                "The OTP you entered is incorrect.",
                parent=win
            )

            return

        # OTP correct
        hashed_password = hash_password(
            password_value
        )

        try:

            # Create account ONLY after OTP verification
            cursor.execute(
                """
                INSERT INTO users
                (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (
                    username_value,
                    email_value,
                    hashed_password
                )
            )

            db.commit()

            messagebox.showinfo(
                "Account Created",
                "Email verified successfully!\n\n"
                "Your account has been created successfully.\n"
                "You can now login.",
                parent=win
            )

            win.destroy()

            # Close Create Account window
            signup_window.destroy()

            # Open login window again
            loginsystem()

        except mysql.connector.IntegrityError:

            db.rollback()

            messagebox.showerror(
                "Already Exists",
                "Username or Email already exists.",
                parent=win
            )

        except mysql.connector.Error as error:

            db.rollback()

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=win
            )

    # Verify button
    tk.Button(
        win,
        text="VERIFY OTP",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=verify
    ).pack(
        padx=60,
        fill="x",
        pady=30,
        ipady=10
    )

    # Cancel button
    tk.Button(
        win,
        text="CANCEL",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=DANGER,
        bd=0,
        cursor="hand2",
        command=lambda: cancel_signup_otp(
            win,
            signup_window
        )
    ).pack(
        pady=5
    )


def cancel_signup_otp(
    otp_window,
    signup_window
):

    otp_window.destroy()

    signup_window.deiconify()

def send_otp_email(receiver_email, otp):

    msg = EmailMessage()

    msg["Subject"] = (
        "Employee Management System - Password Reset OTP"
    )

    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Hello,

Your OTP for password reset is:

{otp}

Please do not share this OTP with anyone.

Regards,
Employee Management System
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

def forgot_password():

    win = tk.Toplevel(root)

    win.title("Forgot Password")
    win.geometry("450x390")
    win.configure(bg=BG)
    win.resizable(False, False)

    header = tk.Frame(
        win,
        bg=PRIMARY,
        height=100
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="🔐",
        font=("Segoe UI Emoji", 28),
        bg=PRIMARY,
        fg=WHITE
    ).pack(pady=(12, 0))

    tk.Label(
        header,
        text="Forgot Password?",
        font=("Segoe UI", 18, "bold"),
        bg=PRIMARY,
        fg=WHITE
    ).pack()

    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    tk.Label(
        card,
        text="Enter your registered email",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(pady=(20, 10))

    email = tk.Entry(
        card,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    email.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    def send_code():

        user_email = email.get().strip().lower()

        if not user_email:

            messagebox.showerror(
                "Error",
                "Please enter your email.",
                parent=win
            )

            return

        cursor.execute(
            """
            SELECT username
            FROM users
            WHERE LOWER(TRIM(email))=%s
            """,
            (user_email,)
        )

        user = cursor.fetchone()

        if not user:

            messagebox.showerror(
                "Error",
                "Email not registered.",
                parent=win
            )

            return

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        try:

            send_otp_email(
                user_email,
                otp
            )

            messagebox.showinfo(
                "OTP Sent",
                "OTP has been sent to your email.",
                parent=win
            )

            win.destroy()

            verify_otp_window(
                user_email,
                otp
            )

        except Exception as e:

            messagebox.showerror(
                "SMTP Error",
                f"Email could not be sent.\n\n{e}",
                parent=win
            )

    tk.Button(
        card,
        text="SEND OTP",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=send_code
    ).pack(
        fill="x",
        padx=25,
        pady=25,
        ipady=10
    )

def verify_otp_window(
    user_email,
    correct_otp
):

    win = tk.Toplevel(root)

    win.title("Verify OTP")
    win.geometry("450x390")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="🔑",
        font=("Segoe UI Emoji", 40),
        bg=BG
    ).pack(pady=(35, 5))

    tk.Label(
        win,
        text="Verify OTP",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        win,
        text="Enter the 6-digit OTP sent to your email",
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED
    ).pack(pady=10)

    otp_entry = tk.Entry(
        win,
        font=("Segoe UI", 18),
        justify="center",
        bd=1,
        relief="solid"
    )

    otp_entry.pack(
        padx=60,
        fill="x",
        ipady=8
    )

    def verify():

        entered = otp_entry.get().strip()

        if not entered:

            messagebox.showerror(
                "Error",
                "Please enter OTP.",
                parent=win
            )

            return

        if entered != correct_otp:

            messagebox.showerror(
                "Error",
                "Invalid OTP.",
                parent=win
            )

            return

        messagebox.showinfo(
            "Success",
            "OTP verified successfully!",
            parent=win
        )

        win.destroy()

        reset_password_window(
            user_email
        )

    tk.Button(
        win,
        text="VERIFY OTP",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=verify
    ).pack(
        padx=60,
        fill="x",
        pady=30,
        ipady=10
    )

def reset_password_window(user_email):

    win = tk.Toplevel(root)

    win.title("Reset Password")
    win.geometry("450x450")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="🔒",
        font=("Segoe UI Emoji", 35),
        bg=BG
    ).pack(pady=(25, 0))

    tk.Label(
        win,
        text="Create New Password",
        font=("Segoe UI", 21, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=10)

    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=15
    )

    tk.Label(
        card,
        text="New Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE
    ).pack(
        anchor="w",
        padx=25,
        pady=(20, 5)
    )

    new_password = tk.Entry(
        card,
        show="*",
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    new_password.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    tk.Label(
        card,
        text="Confirm Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    confirm_password = tk.Entry(
        card,
        show="*",
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    confirm_password.pack(
        fill="x",
        padx=25,
        ipady=8
    )

    def change_password():

        new_p = new_password.get()
        confirm_p = confirm_password.get()

        if not new_p or not confirm_p:

            messagebox.showerror(
                "Error",
                "Please fill all fields.",
                parent=win
            )

            return

        if new_p != confirm_p:

            messagebox.showerror(
                "Error",
                "Passwords do not match.",
                parent=win
            )

            return

        new_hashed = hash_password(new_p)

        try:

            cursor.execute(
                """
                UPDATE users
                SET password=%s
                """,
                (new_hashed,)
            )

            db.commit()

            messagebox.showinfo(
                "Success",
                "Password changed successfully!\n\n"
                "This password will work for all IDs.",
                parent=win
            )

            win.destroy()

        except mysql.connector.Error as e:

            db.rollback()

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    tk.Button(
        card,
        text="CHANGE PASSWORD",
        font=("Segoe UI", 11, "bold"),
        bg=SUCCESS,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=change_password
    ).pack(
        fill="x",
        padx=25,
        pady=25,
        ipady=10
    )

def add_employee():

    win = tk.Toplevel(root)

    win.title("Add Employee")
    win.geometry("500x500")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="Add New Employee",
        font=("Segoe UI", 24, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=25)

    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=10
    )

    def field(label):

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )

        entry.pack(
            fill="x",
            padx=30,
            ipady=7
        )

        return entry

    name_entry = field("Employee Name")
    age_entry = field("Age")
    dep_entry = field("Department")

    def add_user():

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        dep = dep_entry.get().strip()

        if not name or not age or not dep:

            messagebox.showerror(
                "Error",
                "Please fill all fields.",
                parent=win
            )

            return

        try:
            int(age)
        except:

            messagebox.showerror(
                "Error",
                "Age must be a number.",
                parent=win
            )

            return

        emp_id = get_next_employee_id()

        with open(
            employee_file,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                emp_id,
                name,
                age,
                dep
            ])

        load_data()

        messagebox.showinfo(
            "Success",
            f"Employee Added Successfully!\n\nEmployee ID: {emp_id}",
            parent=win
        )

        win.destroy()

        update_dashboard()

    tk.Button(
        card,
        text="＋  ADD EMPLOYEE",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=add_user
    ).pack(
        fill="x",
        padx=30,
        pady=25,
        ipady=10
    )

def update_employee():

    win = tk.Toplevel(root)

    win.title("Update Employee")
    win.geometry("500x560")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="Update Employee",
        font=("Segoe UI", 23, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=20)

    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=10
    )

    def create_field(label):

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(12, 4)
        )

        entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )

        entry.pack(
            fill="x",
            padx=25,
            ipady=7
        )

        return entry

    emp_id_entry = create_field(
        "Employee ID"
    )

    new_name_entry = create_field(
        "New Name"
    )

    age_entry = create_field(
        "Age"
    )

    dep_entry = create_field(
        "Department"
    )

    def search():

        emp_id = emp_id_entry.get().strip()

        for row in get_employees():

            if row[0].upper() == emp_id.upper():

                new_name_entry.delete(
                    0,
                    tk.END
                )

                age_entry.delete(
                    0,
                    tk.END
                )

                dep_entry.delete(
                    0,
                    tk.END
                )

                new_name_entry.insert(
                    0,
                    row[1]
                )

                age_entry.insert(
                    0,
                    row[2]
                )

                dep_entry.insert(
                    0,
                    row[3]
                )

                return

        messagebox.showerror(
            "Error",
            "Employee ID not found.",
            parent=win
        )

    def update_user():

        emp_id = emp_id_entry.get().strip()
        name = new_name_entry.get().strip()
        age = age_entry.get().strip()
        dep = dep_entry.get().strip()

        if not emp_id or not name or not age or not dep:

            messagebox.showerror(
                "Error",
                "Please fill all fields.",
                parent=win
            )

            return

        rows = []
        found = False

        with open(
            employee_file,
            "r",
            newline=""
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if row[0].upper() == emp_id.upper():

                    rows.append([
                        row[0],
                        name,
                        age,
                        dep
                    ])

                    found = True

                else:

                    rows.append(row)

        if not found:

            messagebox.showerror(
                "Error",
                "Employee ID not found.",
                parent=win
            )

            return

        with open(
            employee_file,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)
            writer.writerows(rows)

        load_data()
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Employee Updated Successfully!",
            parent=win
        )

        win.destroy()

    button_row = tk.Frame(
        card,
        bg=WHITE
    )

    button_row.pack(
        pady=20
    )

    tk.Button(
        button_row,
        text="SEARCH",
        width=15,
        font=("Segoe UI", 10, "bold"),
        bg=INFO,
        fg=WHITE,
        bd=0,
        command=search
    ).pack(
        side="left",
        padx=5,
        ipady=7
    )

    tk.Button(
        button_row,
        text="UPDATE",
        width=15,
        font=("Segoe UI", 10, "bold"),
        bg=SUCCESS,
        fg=WHITE,
        bd=0,
        command=update_user
    ).pack(
        side="left",
        padx=5,
        ipady=7
    )

def delete_employee():

    win = tk.Toplevel(root)

    win.title("Delete Employee")
    win.geometry("450x350")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="🗑",
        font=("Segoe UI Emoji", 40),
        bg=BG
    ).pack(pady=(30, 5))

    tk.Label(
        win,
        text="Delete Employee",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    emp_id_entry = tk.Entry(
        win,
        font=("Segoe UI", 12),
        justify="center",
        bd=1,
        relief="solid"
    )

    emp_id_entry.pack(
        padx=70,
        fill="x",
        pady=25,
        ipady=8
    )

    def delete_user():

        emp_id = emp_id_entry.get().strip()

        if not emp_id:

            messagebox.showerror(
                "Error",
                "Enter Employee ID.",
                parent=win
            )

            return

        rows = []
        found = False

        with open(
            employee_file,
            "r",
            newline=""
        ) as file:

            reader = csv.reader(file)

            for row in reader:

                if row[0].upper() == emp_id.upper():

                    found = True

                else:

                    rows.append(row)

        if not found:

            messagebox.showerror(
                "Error",
                "Employee ID not found.",
                parent=win
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete employee {emp_id}?",
            parent=win
        )

        if not confirm:
            return

        with open(
            employee_file,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)
            writer.writerows(rows)

        load_data()
        update_dashboard()

        messagebox.showinfo(
            "Success",
            "Employee Deleted Successfully!",
            parent=win
        )

        win.destroy()

    tk.Button(
        win,
        text="DELETE EMPLOYEE",
        font=("Segoe UI", 11, "bold"),
        bg=DANGER,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=delete_user
    ).pack(
        padx=70,
        fill="x",
        ipady=10
    )

def search_employee():

    win = tk.Toplevel(root)

    win.title("Search Employee")
    win.geometry("500x430")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="🔎",
        font=("Segoe UI Emoji", 35),
        bg=BG
    ).pack(pady=(25, 0))

    tk.Label(
        win,
        text="Search Employee",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    emp_id_entry = tk.Entry(
        win,
        font=("Segoe UI", 12),
        justify="center",
        bd=1,
        relief="solid"
    )

    emp_id_entry.pack(
        padx=70,
        fill="x",
        pady=20,
        ipady=8
    )

    result = tk.Frame(
        win,
        bg=WHITE
    )

    result.pack(
        fill="both",
        expand=True,
        padx=50,
        pady=5
    )

    def search_user():

        emp_id = emp_id_entry.get().strip()

        for row in get_employees():

            if row[0].upper() == emp_id.upper():

                for widget in result.winfo_children():
                    widget.destroy()

                details = [
                    ("Employee ID", row[0]),
                    ("Name", row[1]),
                    ("Age", row[2]),
                    ("Department", row[3])
                ]

                for label, value in details:

                    frame = tk.Frame(
                        result,
                        bg=WHITE
                    )

                    frame.pack(
                        fill="x",
                        padx=20,
                        pady=7
                    )

                    tk.Label(
                        frame,
                        text=label,
                        font=("Segoe UI", 10, "bold"),
                        bg=WHITE,
                        fg=MUTED,
                        width=15,
                        anchor="w"
                    ).pack(side="left")

                    tk.Label(
                        frame,
                        text=value,
                        font=("Segoe UI", 10, "bold"),
                        bg=WHITE,
                        fg=TEXT,
                        anchor="w"
                    ).pack(side="left")

                return

        messagebox.showerror(
            "Error",
            "Employee ID not found.",
            parent=win
        )

    tk.Button(
        win,
        text="SEARCH EMPLOYEE",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        command=search_user
    ).pack(
        padx=70,
        fill="x",
        pady=15,
        ipady=9
    )

def upload_employee():

    win = tk.Toplevel(root)

    win.title("Employee Photo")
    win.geometry("500x520")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="Employee Photo",
        font=("Segoe UI", 23, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=25)

    photo_frame = tk.Frame(
        win,
        bg=WHITE,
        width=220,
        height=220
    )

    photo_frame.pack(
        pady=10
    )

    photo_frame.pack_propagate(False)

    photo_label = tk.Label(
        photo_frame,
        text="No Photo Selected",
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 11)
    )

    photo_label.pack(
        expand=True
    )

    def select_photo():

        path = filedialog.askopenfilename(
            parent=win,
            title="Select Employee Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                )
            ]
        )

        if not path:
            return

        try:

            img = Image.open(path)

            img.thumbnail(
                (210, 210)
            )

            photo = ImageTk.PhotoImage(
                img
            )

            photo_label.config(
                image=photo,
                text=""
            )

            photo_label.image = photo

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )

    tk.Button(
        win,
        text="📷  CHOOSE PHOTO",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=select_photo
    ).pack(
        padx=70,
        fill="x",
        pady=30,
        ipady=10
    )

def salary_calculator():

    win = tk.Toplevel(root)

    win.title("Salary Calculator")
    win.geometry("700x700")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="💰",
        font=("Segoe UI Emoji", 35),
        bg=BG
    ).pack(pady=(20, 0))

    tk.Label(
        win,
        text="Salary Calculator",
        font=("Segoe UI", 23, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    card = tk.Frame(
        win,
        bg=WHITE
    )

    card.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=20
    )

    entries = {}

    for label in [
        "Basic Salary",
        "HRA",
        "DA",
        "Deductions"
    ]:

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(10, 4)
        )

        entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid"
        )

        entry.pack(
            fill="x",
            padx=25,
            ipady=7
        )

        entries[label] = entry

    result = tk.Label(
        card,
        text="Net Salary: ₹0.00",
        font=("Segoe UI", 16, "bold"),
        bg=WHITE,
        fg=SUCCESS
    )

    result.pack(
        pady=20
    )

    def calculate():

        try:

            basic = float(
                entries["Basic Salary"].get()
            )

            hra = float(
                entries["HRA"].get()
            )

            da = float(
                entries["DA"].get()
            )

            deduction = float(
                entries["Deductions"].get()
            )

            gross = basic + hra + da

            net = gross - deduction

            result.config(
                text=f"Net Salary: ₹{net:,.2f}"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid numbers.",
                parent=win
            )

    tk.Button(
        card,
        text="CALCULATE SALARY",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=calculate
    ).pack(
        fill="x",
        padx=25,
        pady=10,
        ipady=10
    )

def department_management():

    global department_count

    win = tk.Toplevel(root)

    win.title("Department Management")
    win.geometry("650x500")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="Department Management",
        font=("Segoe UI", 23, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=20)

    top = tk.Frame(
        win,
        bg=BG
    )

    top.pack(
        fill="x",
        padx=30
    )

    dept_entry = tk.Entry(
        top,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    dept_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=8
    )

    tree_dept = ttk.Treeview(
        win,
        columns=("ID", "Department"),
        show="headings"
    )

    tree_dept.heading(
        "ID",
        text="Department ID"
    )

    tree_dept.heading(
        "Department",
        text="Department Name"
    )

    tree_dept.column(
        "ID",
        width=180,
        anchor="center"
    )

    tree_dept.column(
        "Department",
        width=350,
        anchor="center"
    )

    tree_dept.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    def add_department():

        global department_count

        name = dept_entry.get().strip()

        if not name:

            messagebox.showerror(
                "Error",
                "Enter department name.",
                parent=win
            )

            return

        dept_id = f"DEP{department_count:03d}"

        department_count += 1

        tree_dept.insert(
            "",
            "end",
            values=(
                dept_id,
                name
            )
        )

        dept_entry.delete(
            0,
            tk.END
        )

    def update_department():

        selected = tree_dept.focus()

        if not selected:
            return

        name = dept_entry.get().strip()

        if not name:
            return

        values = tree_dept.item(
            selected
        )["values"]

        tree_dept.item(
            selected,
            values=(
                values[0],
                name
            )
        )

        dept_entry.delete(
            0,
            tk.END
        )

    def delete_department():

        selected = tree_dept.focus()

        if not selected:
            return

        tree_dept.delete(
            selected
        )

        dept_entry.delete(
            0,
            tk.END
        )

    def select_data(event):

        selected = tree_dept.focus()

        if not selected:
            return

        values = tree_dept.item(
            selected
        )["values"]

        dept_entry.delete(
            0,
            tk.END
        )

        dept_entry.insert(
            0,
            values[1]
        )

    tree_dept.bind(
        "<<TreeviewSelect>>",
        select_data
    )

    tk.Button(
        top,
        text="ADD",
        width=10,
        font=("Segoe UI", 10, "bold"),
        bg=SUCCESS,
        fg=WHITE,
        bd=0,
        command=add_department
    ).pack(
        side="left",
        padx=5,
        ipady=6
    )

    tk.Button(
        top,
        text="UPDATE",
        width=10,
        font=("Segoe UI", 10, "bold"),
        bg=INFO,
        fg=WHITE,
        bd=0,
        command=update_department
    ).pack(
        side="left",
        padx=5,
        ipady=6
    )

    tk.Button(
        top,
        text="DELETE",
        width=10,
        font=("Segoe UI", 10, "bold"),
        bg=DANGER,
        fg=WHITE,
        bd=0,
        command=delete_department
    ).pack(
        side="left",
        padx=5,
        ipady=6
    )

cards = {}


def create_card(parent, title, color):

    card = tk.Frame(
        parent,
        bg=color,
        width=230,
        height=110
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 11, "bold"),
        bg=color,
        fg=WHITE
    ).pack(
        pady=(15, 5)
    )

    value = tk.Label(
        card,
        text="0",
        font=("Segoe UI", 26, "bold"),
        bg=color,
        fg=WHITE
    )

    value.pack()

    cards[title] = value


def update_dashboard():

    employees = get_employees()

    total = len(employees)

    departments = set()

    for employee in employees:

        if len(employee) >= 4:

            departments.add(
                employee[3]
            )

    cards["Total Employees"].config(
        text=str(total)
    )

    cards["Departments"].config(
        text=str(len(departments))
    )

    cards["Active"].config(
        text=str(total)
    )

    cards["Inactive"].config(
        text="0"
    )

def create_dashboard():

    # Header
    header = tk.Frame(
        root,
        bg=SIDEBAR,
        height=75
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="EMPLOYEE MANAGEMENT SYSTEM",
        font=("Segoe UI", 21, "bold"),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(
        side="left",
        padx=30,
        pady=20
    )

    tk.Label(
        header,
        text="HRMS Dashboard",
        font=("Segoe UI", 10),
        bg=SIDEBAR,
        fg="#94A3B8"
    ).pack(
        side="right",
        padx=30
    )

    # Main content
    content = tk.Frame(
        root,
        bg=BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # Welcome
    tk.Label(
        content,
        text="Dashboard",
        font=("Segoe UI", 25, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        content,
        text="Manage your employees efficiently",
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        pady=(0, 20)
    )

    # Cards
    card_frame = tk.Frame(
        content,
        bg=BG
    )

    card_frame.pack(
        fill="x",
        pady=(0, 20)
    )

    create_card(
        card_frame,
        "Total Employees",
        "#4F46E5"
    )

    create_card(
        card_frame,
        "Departments",
        SUCCESS
    )

    create_card(
        card_frame,
        "Active",
        INFO
    )

    create_card(
        card_frame,
        "Inactive",
        WARNING
    )

    action_frame = tk.Frame(
        content,
        bg=BG,
        height=60
    )

    action_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    action_frame.pack_propagate(False)

    tk.Button(
        action_frame,
        text="＋ Add Employee",
        font=("Segoe UI", 10, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=add_employee
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="✎ Update Employee",
        font=("Segoe UI", 10, "bold"),
        bg=INFO,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=update_employee
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="✕ Delete Employee",
        font=("Segoe UI", 10, "bold"),
        bg=DANGER,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=delete_employee
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="⌕ Search",
        font=("Segoe UI", 10, "bold"),
        bg="#7C3AED",
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=search_employee
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="▣ Photo",
        font=("Segoe UI", 10, "bold"),
        bg="#0891B2",
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=upload_employee
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="₹ Salary",
        font=("Segoe UI", 10, "bold"),
        bg=SUCCESS,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=salary_calculator
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )

    tk.Button(
        action_frame,
        text="▦ Departments",
        font=("Segoe UI", 10, "bold"),
        bg="#8B5CF6",
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=department_management
    ).pack(
        side="left",
        padx=5,
        ipadx=10,
        ipady=10
    )
    # Table container
    table_card = tk.Frame(
        content,
        bg=WHITE
    )

    table_card.pack(
        fill="both",
        expand=True,
        pady=(0, 5)
    )

    tk.Label(
        table_card,
        text="Employee Records",
        font=("Segoe UI", 16, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=20,
        pady=15
    )

    table_frame = tk.Frame(
        table_card,
        bg=WHITE
    )

    table_frame.pack(
        fill="both",
        expand=False,
        padx=20,
        pady=(0, 10)
    )

    table_frame.configure(height=280)
    table_frame.pack_propagate(False)

    scroll_y = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    scroll_y.pack(
        side="right",
        fill="y"
    )

    global tree

    tree = ttk.Treeview(
        table_frame,
        columns=(
            "ID",
            "Name",
            "Age",
            "Department"
        ),
        show="headings",
        yscrollcommand=scroll_y.set
    )

    scroll_y.config(
        command=tree.yview
    )

    tree.heading(
        "ID",
        text="EMPLOYEE ID"
    )

    tree.heading(
        "Name",
        text="NAME"
    )

    tree.heading(
        "Age",
        text="AGE"
    )

    tree.heading(
        "Department",
        text="DEPARTMENT"
    )

    tree.column(
        "ID",
        width=150,
        anchor="center"
    )

    tree.column(
        "Name",
        width=250,
        anchor="center"
    )

    tree.column(
        "Age",
        width=100,
        anchor="center"
    )

    tree.column(
        "Department",
        width=250,
        anchor="center"
    )

    tree.pack(
        fill="both",
        expand=True
    )

    # Buttons
    button_frame = tk.Frame(
        content,
        bg=BG
    )

    button_frame.pack(
        fill="x",
        pady=15
    )

    buttons = [
        (
            "＋  Add Employee",
            PRIMARY,
            add_employee
        ),
        (
            "✎  Update",
            INFO,
            update_employee
        ),
        (
            "✕  Delete",
            DANGER,
            delete_employee
        ),
        (
            "⌕  Search",
            "#7C3AED",
            search_employee
        ),
        (
            "▣  Photo",
            "#0891B2",
            upload_employee
        ),
        (
            "₹  Salary",
            SUCCESS,
            salary_calculator
        ),
        (
            "▦  Departments",
            "#8B5CF6",
            department_management
        ),
    ]

    for text, color, command in buttons:

        tk.Button(
            button_frame,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg=WHITE,
            bd=0,
            cursor="hand2",
            command=command
        ).pack(
            side="left",
            padx=4,
            ipadx=8,
            ipady=8
        )

    def logout():

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if result:

            root.withdraw()
            loginsystem()

    tk.Button(
        button_frame,
        text="⇥  Logout",
        font=("Segoe UI", 10, "bold"),
        bg=SIDEBAR,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=logout
    ).pack(
        side="right",
        padx=4,
        ipadx=15,
        ipady=8
    )

def load_data():

    if "tree" not in globals():
        return

    for row in tree.get_children():

        tree.delete(row)

    for employee in get_employees():

        tree.insert(
            "",
            "end",
            values=employee
        )

    update_dashboard()

def loginsystem():

    login = tk.Toplevel(root)

    login.title(
        "Employee Management System - Login"
    )

    login.geometry(
        "900x550"
    )

    login.configure(
        bg=WHITE
    )

    login.resizable(
        False,
        False
    )

    # Left panel
    left = tk.Frame(
        login,
        bg=SIDEBAR,
        width=400
    )

    left.pack(
        side="left",
        fill="y"
    )

    left.pack_propagate(False)

    tk.Label(
        left,
        text="WELCOME",
        font=("Segoe UI", 30, "bold"),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(
        pady=(130, 5)
    )

    tk.Label(
        left,
        text="Employee Management\nSystem",
        font=("Segoe UI", 18),
        bg=SIDEBAR,
        fg="#CBD5E1",
        justify="center"
    ).pack()

    tk.Label(
        left,
        text="👨‍💼",
        font=("Segoe UI Emoji", 70),
        bg=SIDEBAR,
        fg=WHITE
    ).pack(
        pady=35
    )

    tk.Label(
        left,
        text="Manage • Track • Grow",
        font=("Segoe UI", 10),
        bg=SIDEBAR,
        fg="#94A3B8"
    ).pack()

    # Right panel
    right = tk.Frame(
        login,
        bg=WHITE
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    tk.Label(
        right,
        text="Login",
        font=("Segoe UI", 28, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        pady=(80, 5)
    )

    tk.Label(
        right,
        text="Sign in to continue",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        pady=(0, 25)
    )

    tk.Label(
        right,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=65
    )

    username = tk.Entry(
        right,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )

    username.pack(
        padx=65,
        fill="x",
        ipady=8
    )

    tk.Label(
        right,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=65,
        pady=(15, 0)
    )

    password = tk.Entry(
        right,
        font=("Segoe UI", 11),
        show="*",
        bd=1,
        relief="solid"
    )

    password.pack(
        padx=65,
        fill="x",
        ipady=8
    )

    def login_user():

        u = username.get().strip()
        p = password.get()

        if not u or not p:

            messagebox.showerror(
                "Error",
                "Please enter username/email and password.",
                parent=login
            )

            return

        hashed = hash_password(p)

        try:

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE (username=%s or email=%s)
                AND password=%s
                """,
                (u,u.lower(), hashed)
            )

            user = cursor.fetchone()

            if user:

                messagebox.showinfo(
                    "Welcome",
                    "Login Successful!",
                    parent=login
                )

                login.destroy()

                root.deiconify()

                load_data()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid Username/email or Password.",
                    parent=login
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=login
            )

    tk.Button(
        right,
        text="LOGIN",
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg=WHITE,
        bd=0,
        cursor="hand2",
        command=login_user
    ).pack(
        padx=65,
        fill="x",
        pady=25,
        ipady=10
    )

    bottom = tk.Frame(
        right,
        bg=WHITE
    )

    bottom.pack()

    tk.Button(
        bottom,
        text="Create Account",
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=PRIMARY,
        bd=0,
        cursor="hand2",
        command=signup
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        bottom,
        text="Forgot Password?",
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=PRIMARY,
        bd=0,
        cursor="hand2",
        command=forgot_password
    ).pack(
        side="left",
        padx=10
    )

create_dashboard()

load_data()

loginsystem()

root.mainloop()