import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
import hashlib
import mysql.connector
import smtplib
import random
from email.message import EmailMessage

SENDER_EMAIL = ""
SENDER_PASSWORD = ""

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    database="hrms",
    password="root@123",
    use_pure=True
)

cursor = db.cursor()

employee_count = 1
department_count = 1
import csv
import os

root = tk.Tk()
root.title("Employee Management System")
root.geometry("500x500")
root.config(bg="white")

root.withdraw()

header = tk.Frame(root, bg="#0B5ED7", height=80)
header.pack(fill="x")

def load_data():
    # Remove old data
    for row in tree.get_children():
        tree.delete(row)

    with open("employees.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)  # Skip header

        for row in reader:
            tree.insert("", "end", values=row)

tk.Label(header,text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Segoe UI", 24, "bold"),
    bg="#0B5ED7",
    fg="white").pack(pady=20)

card_frame = tk.Frame(root, bg="#F4F6F9")
card_frame.pack(fill="x", pady=15)

center_frame = tk.Frame(card_frame, bg="#F4F6F9")
center_frame.pack(anchor="center")

dep = set()
active = 0
inactive = 0
file = open("employees.csv", "r")
reader = csv.DictReader(file)
data = file.readlines()
r = len(data)
total = len(data)
for line in data[1:]:
    values = line.strip().split(",")
    dep.add(values[3])
d = len(dep)
file.close()

cards = [
    ("Total Employees", r-1, "#4E73DF"),
    ("Departments",d, "#1CC88A"),
    ("Active", total-1, "#36B9CC"),
    ("Inactive",0, "#F6C23E")
]

for title, value, color in cards:
    card = tk.Frame(center_frame, bg=color, width=250, height=90)
    card.pack(side="left", padx=20)
    card.pack_propagate(False)

    tk.Label(card,
             text=title,
             bg=color,
             fg="white",
             font=("Segoe UI", 12, "bold")).pack(pady=(10,0))

    tk.Label(card,
             text=value,
             bg=color,
             fg="white",
             font=("Segoe UI", 24, "bold")).pack()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

SENDER_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_16_character_app_password"

def signup():
    signup_win = tk.Toplevel(root)
    signup_win.title("Sign Up")
    signup_win.geometry("400x400")
    signup_win.config(bg="white")

    tk.Label(
        signup_win,
        text="Create Account",
        font=("Segoe UI", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    tk.Label(signup_win, text="Username", bg="white").pack()
    username = tk.Entry(signup_win, width=30)
    username.pack(pady=5)

    tk.Label(signup_win, text="Email", bg="white").pack()
    email = tk.Entry(signup_win, width=30)
    email.pack(pady=5)

    tk.Label(signup_win, text="Password", bg="white").pack()
    password = tk.Entry(signup_win, width=30, show="*")
    password.pack(pady=5)

    def create_account():
        u = username.get().strip()
        e = email.get().strip().lower()
        p = password.get()

        if not u or not e or not p:
            print("Please fill all fields")
            return

        hashed = hash_password(p)

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (u, e, hashed)
            )

            db.commit()
            print("Account Created Successfully!")
            signup_win.destroy()

        except mysql.connector.IntegrityError:
            print("Username or Email already exists")

    tk.Button(
        signup_win,
        text="Sign Up",
        command=create_account,
        width=20
    ).pack(pady=20)

SENDER_EMAIL = "kunallakra@gmail.com"
APP_PASSWORD = "kunallakra123456"

def send_otp_email(receiver_email, otp):
    print("SENDER EMAIL:", repr(SENDER_EMAIL))
    print("APP PASSWORD LENGTH:", len(APP_PASSWORD))
    print("RECEIVER EMAIL:", repr(receiver_email))
    msg = EmailMessage()

    msg["Subject"] = "Employee Management System - Password Reset OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(
        f"""Hello,

Your OTP for password reset is:

{otp}

Please do not share this OTP with anyone.

Regards,
Employee Management System
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print("SENDER:", SENDER_EMAIL)
    print("APP PASSWORD LENGTH:", len(APP_PASSWORD))
def forgot_password():

    forgot_win = tk.Toplevel(root)
    forgot_win.title("Forgot Password")
    forgot_win.geometry("400x250")
    forgot_win.config(bg="white")
    forgot_win.resizable(False, False)

    tk.Label(
        forgot_win,
        text="Forgot Password",
        font=("Segoe UI", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    tk.Label(
        forgot_win,
        text="Enter Registered Email",
        bg="white"
    ).pack()

    email = tk.Entry(
        forgot_win,
        width=30
    )
    email.pack(pady=8)

    def send_code():

        user_email = email.get().strip()
        print("Entered Email:", repr(user_email))

        cursor.execute(
            "SELECT username, email FROM users WHERE email=%s",
            (user_email,)
        )

        user = cursor.fetchone()
        cursor.execute("SELECT username, email FROM users")
        all_users = cursor.fetchall()

        print("ALL USERS FROM PYTHON:", all_users)

        cursor.execute(
            "SELECT username FROM users WHERE LOWER(TRIM(email)) = %s",
            (user_email,)
        )

        user = cursor.fetchone()

        print("Search Result:", user)

        if not user:
            messagebox.showerror(
                "Error",
                "Email not registered"
            )
            return


        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))

        try:

            send_otp_email(user_email, otp)

            messagebox.showinfo(
                "Success",
                "OTP sent successfully to your email"
            )

            forgot_win.destroy()

            verify_otp_window(
                user_email,
                otp
            )

        except Exception as e:

            print("SMTP ERROR:", repr(e))

            messagebox.showerror(

                "SMTP Error",

                f"Email could not be sent.\n\n{repr(e)}"

            )


    tk.Button(
        forgot_win,
        text="Send OTP",
        command=send_code,
        width=20
    ).pack(pady=15)

def verify_otp_window(user_email, correct_otp):

    otp_win = tk.Toplevel(root)
    otp_win.title("Verify OTP")
    otp_win.geometry("400x250")
    otp_win.config(bg="white")
    otp_win.resizable(False, False)

    tk.Label(
        otp_win,
        text="Verify OTP",
        font=("Segoe UI", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    tk.Label(
        otp_win,
        text="Enter OTP sent to your email",
        bg="white"
    ).pack()

    otp_entry = tk.Entry(
        otp_win,
        width=30
    )
    otp_entry.pack(pady=10)

    def verify():

        entered_otp = otp_entry.get().strip()

        if entered_otp == "":
            messagebox.showerror(
                "Error",
                "Please enter OTP"
            )
            return

        if entered_otp != correct_otp:
            messagebox.showerror(
                "Error",
                "Invalid OTP"
            )
            return

        messagebox.showinfo(
            "Success",
            "OTP Verified Successfully"
        )

        otp_win.destroy()

        reset_password_window(user_email)

    tk.Button(
        otp_win,
        text="Verify OTP",
        command=verify,
        width=20
    ).pack(pady=15)

def reset_password_window(user_email):

    reset_win = tk.Toplevel(root)
    reset_win.title("Reset Password")
    reset_win.geometry("400x320")
    reset_win.config(bg="white")
    reset_win.resizable(False, False)

    tk.Label(
        reset_win,
        text="Create New Password",
        font=("Segoe UI", 22, "bold"),
        bg="white"
    ).pack(pady=20)

    tk.Label(
        reset_win,
        text="New Password",
        bg="white"
    ).pack()

    new_password = tk.Entry(
        reset_win,
        width=30,
        show="*"
    )
    new_password.pack(pady=5)

    tk.Label(
        reset_win,
        text="Confirm Password",
        bg="white"
    ).pack()

    confirm_password = tk.Entry(
        reset_win,
        width=30,
        show="*"
    )
    confirm_password.pack(pady=5)

    def change_password():

        new_p = new_password.get()
        confirm_p = confirm_password.get()

        if new_p == "" or confirm_p == "":
            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )
            return

        if new_p != confirm_p:
            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )
            return

        # Hash new password
        new_hashed = hash_password(new_p)

        cursor.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (new_hashed, user_email)
        )

        db.commit()

        if cursor.rowcount > 0:

            messagebox.showinfo(
                "Success",
                "Password changed successfully!"
            )

            reset_win.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Password could not be changed"
            )

    tk.Button(
        reset_win,
        text="Change Password",
        command=change_password,
        width=20
    ).pack(pady=20)

def loginsystem():
    login = tk.Toplevel(root)
    login.title("Login System")
    login.geometry("400x500")
    login.config(bg="white")
    login.resizable(width=False, height=False)
    left_frame = tk.Frame(login, bg="#4A6CF7", width=380)
    left_frame.pack(side="left", fill="y")

    tk.Label(left_frame, text="WELCOME",
             font=("Segoe UI", 30, "bold"),
             bg="#4A6CF7",
             fg="white").pack(pady=(120, 10))

    tk.Label(left_frame, text="Employee Management\nSystem",
             font=("Segoe UI", 15),
             bg="#4A6CF7",
             fg="white",
             justify="center").pack()

    tk.Label(left_frame, text="🔒",
             font=("Segoe UI Emoji", 70),
             bg="#4A6CF7",
             fg="white").pack(pady=40)

    tk.Label(login, text="Login System", font=("Arial", 20, "bold")).pack(pady=20)

    tk.Label(login, text="Username").pack()
    username = tk.Entry(login, width=30)
    username.pack(pady=5)

    tk.Label(login, text="Password").pack()
    password = tk.Entry(login, show="*", width=30)
    password.pack(pady=5)

    def login_user():
        u = username.get().strip()
        p = password.get()

        if not u or not p:
            messagebox.showerror(
                "Error",
                "Please enter username and password"
            )
            return

        hashed = hash_password(p)

        try:
            cursor.execute(
                "SELECT username FROM users WHERE username=%s AND password=%s",
                (u, hashed)
            )

            user = cursor.fetchone()

            if user:
                messagebox.showinfo(
                    "Success",
                    "Login Successful"
                )

                login.destroy()
                root.deiconify()

            else:
                messagebox.showerror(
                    "Error",
                    "Invalid Username or Password"
                )

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )



    tk.Button(
        login,
        text="Sign Up",
        command=signup,
        width=20
    ).pack(pady=5)

    tk.Button(
        login,
        text="Forgot Password?",
        command=forgot_password,
        width=20
    ).pack(pady=5)

    tk.Button(login, text="Login",
              font=("Segoe UI", 15),
              bg="blue",
              fg="white",
              command=login_user,
              width=15).pack(pady=20)

def add_employee():
    add = tk.Toplevel(root)
    add.title("Add Employee")
    add.geometry("400x300")
    add.config(bg="pink")

    tk.Label(add, text="Add Employee", width=20).pack(pady=20)

    tk.Label(add, text="Name").pack()
    name_entry = tk.Entry(add, width=30)
    name_entry.pack(pady=5)

    tk.Label(add, text="age").pack()
    age_entry = tk.Entry(add, width=30)
    age_entry.pack(pady=5)

    tk.Label(add, text="dep").pack()
    dep_entry = tk.Entry(add, width=30)
    dep_entry.pack(pady=5)

    employee_count = 1
    file_name = "employees.csv"
    emp_id = 1
    global r

    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Employee ID", "Name", "Age", "Department"])
            writer.writerow([emp_id])
            emp_id += 1
            r+=1
            return "EMP001"

    def get_next_employee_id():
        if not os.path.exists(file_name):
            return "EMP001"

        with open(file_name, "r", newline="") as file:
            reader = list(csv.reader(file))

        if len(reader) <= 1:
            return "EMP001"

        last_id = reader[-1][0]
        number = int(last_id.replace("EMP", ""))
        return f"EMP{number + 1:03d}"



    def add_user():
        global employee_count
        employee_count = 1
        employee_count += 1
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        dep = dep_entry.get().strip()

        if name == "" or age == "" or dep == "":
            messagebox.showerror("Error", "Fill all fields")
            return
        emp_id = f"EMP{employee_count:03d}"
        tree.insert("", "end", values=(emp_id, name, age, dep))

        emp_id = get_next_employee_id()
        save_employee(emp_id, name, age, dep)

        load_data()

    def save_employee(emp_id, name, age, dep):
        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([emp_id, name, age, dep])

        employee_count += 1

    def save_employee(emp_id, name, age, dep):
        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([emp_id, name, age, dep])

        messagebox.showinfo(
            "Success",
            f"Employee Added Successfully\n\nEmployee ID: {emp_id}"
        )

        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        dep_entry.delete(0, tk.END)

    tk.Button(add, text="Add Employee",
              font=("Arial", 18),
              bg="blue",
              fg="white",
              width=15,
              command=add_user).pack(pady=20)


def update_employee():
    update = tk.Toplevel(root)
    update.title("Update Employee")
    update.geometry("400x300")
    update.config(bg="pink")
    tk.Label(update, text="Update Employee", font=("Arial", 18)).pack(pady=20)

    tk.Label(update, text="Employee ID").pack()
    emp_id_entry = tk.Entry(update, width=30)
    emp_id_entry.pack()

    tk.Label(update, text="New Name").pack()
    new_name_entry = tk.Entry(update, width=30)
    new_name_entry.pack(pady=5)

    tk.Label(update, text="Age").pack()
    age_entry = tk.Entry(update, width=30)
    age_entry.pack(pady=5)

    tk.Label(update, text="Dep").pack()
    dep_entry = tk.Entry(update, width=30)
    dep_entry.pack(pady=5)

    def search_employee():
        emp_id = emp_id_entry.get().strip()

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if row[0] == emp_id:
                    new_name_entry.delete(0, tk.END)
                    age_entry.delete(0, tk.END)
                    dep_entry.delete(0, tk.END)

                    new_name_entry.insert(0, row[1])
                    age_entry.insert(0, row[2])
                    dep_entry.insert(0, row[3])
                    return

        messagebox.showerror("Error", "Employee ID not found")

    import csv
    file_name = "employees.csv"
    emp_id=1
    def employee_exists(emp_id):
        emp_id = emp_id_entry.get().strip()
        found = False
        print("Searching:", emp_id)
        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if row[0] == emp_id:
                    new_name_entry.delete(0, tk.END)
                    age_entry.delete(0, tk.END)
                    dep_entry.delete(0, tk.END)

                    new_name_entry.insert(0, row[1])
                    age_entry.insert(0, row[2])
                    dep_entry.insert(0, row[3])

                    found = True
                    break

                print("Not Found")
                messagebox.showerror("Error", "Employee ID not found")


    tk.Button(update, text="Search", command=search_employee).pack()

    def update_user():
        emp_id = emp_id_entry.get().strip()
        new_name = new_name_entry.get().strip()
        new_age = age_entry.get().strip()
        new_dep = dep_entry.get().strip()

        rows = []

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                if row[0] == emp_id:
                    row = [emp_id, new_name, new_age, new_dep]

                rows.append(row)

        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        load_data()
        messagebox.showinfo("Success", "Employee Updated Successfully")

    tk.Button(update, text="Update Employee",
              font=("Arial", 18),
              bg="blue",
              fg="white",
              command=update_user).pack(pady=5)


def delete_employee():
    delete = tk.Toplevel(root)
    delete.title("Delete Employee")
    delete.geometry("400x300")
    delete.config(bg="pink")
    tk.Label(delete, text="Delete Employee", font=("Arial", 18)).pack(pady=20)

    tk.Label(delete, text="Employee ID").pack()
    emp_id_entry = tk.Entry(delete, width=30)
    emp_id_entry.pack(pady=5)

    import csv

    def delete_employee_by_id(id):
        rows = []
        found = False

        with open("employees.csv", "r", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                if row[0] == id:
                    found = True
                    continue  # Skip this employee

                rows.append(row)

        with open("employees.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return found

    def delete_user():
        emp_id = emp_id_entry.get().strip()

        if emp_id == "":
            messagebox.showerror("Error", "Enter Employee ID")
            return

        if delete_employee_by_id(emp_id):
            messagebox.showinfo("Success", "Employee Deleted Successfully")
            delete.destroy()
        else:
            messagebox.showerror("Error", "Employee ID not found!")

    tk.Button(delete, text="Delete Employee",
              font=("Arial", 18),
              bg="blue",
              fg="white",
              width=15,
              command=delete_user).pack(pady=20)


def search_employee():
    search = tk.Toplevel(root)
    search.title("Search Employee")
    search.geometry("400x300")
    search.config(bg="pink")
    tk.Label(search, text="Search Employee", font=("Arial", 18)).pack(pady=20)

    tk.Label(search, text="Employee ID").pack()
    emp_id_entry = tk.Entry(search, width=30)
    emp_id_entry.pack(pady=5)

    import csv

    def search_employee_by_id(emp_id):
        with open("employees.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header

            for row in reader:
                if row[0].strip().upper() == emp_id.strip().upper():
                    return row

        return None

    def search_user():
        emp_id = emp_id_entry.get().strip()

        if emp_id == "":
            messagebox.showerror("Error", "Enter Employee ID")
            return

        employee = search_employee_by_id(emp_id)

        if employee:
            messagebox.showinfo(
                "Employee Found",
                f"Employee ID : {employee[0]}\n"
                f"Name : {employee[1]}\n"
                f"Age : {employee[2]}\n"
                f"Department : {employee[3]}"
            )
        else:
            messagebox.showerror("Error", "Employee ID not found!")

    tk.Button(search, text="Search Employee",
              font=("Arial", 18),
              bg="blue",
              fg="white",
              width=15,
              command=search_user).pack(pady=20)


def upload_employee():
    upload = tk.Toplevel(root)
    upload.title("Upload Employee")
    upload.geometry("400x300")
    upload.config(bg="pink")
    tk.Label(upload, text="Upload Employee", font=("Arial", 18)).pack(pady=20)

    photo_label = tk.Label(upload)
    photo_label.pack(pady=10)

    def select_photo():
        global photo_path
        upload.lift()
        upload.focus_force()
        photo_path = filedialog.askopenfilename(
            parent=upload,
            title="Select Employee Photo",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if photo_path:
            img = Image.open(photo_path)
            img = img.resize((150, 150))

            photo = ImageTk.PhotoImage(img)

            photo_label.config(image=photo)
            photo_label.image = photo

    tk.Button(
        upload,
        text="Choose Photo",
        command=select_photo
    ).pack(pady=10)


def salary_calculator():
    salary = tk.Toplevel(root)
    salary.title("Salary Calculator")
    salary.geometry("400x300")
    salary.config(bg="pink")
    tk.Label(salary, text="Salary Calculator", font=("Arial", 18)).pack(pady=20)

    tk.Label(salary, text="Basic Salary").pack()
    basic_entry = tk.Entry(salary, width=30)
    basic_entry.pack()

    tk.Label(salary, text="HRA").pack()
    hra_entry = tk.Entry(salary, width=30)
    hra_entry.pack()

    tk.Label(salary, text="DA").pack()
    da_entry = tk.Entry(salary, width=30)
    da_entry.pack()

    tk.Label(salary, text="Deductions").pack()
    deduction_entry = tk.Entry(salary, width=30)
    deduction_entry.pack()

    result = tk.Label(salary, text="", font=("Arial", 12, "bold"))
    result.pack(pady=10)

    def salary_calculator():
        basic = float(basic_entry.get())
        hra = float(hra_entry.get())
        da = float(da_entry.get())
        deduction = float(deduction_entry.get())

        gross = basic + hra + da
        net = gross - deduction

        result.config(text=f"Net Salary: {net:.2f}")

    tk.Button(salary, text="Salary Calculator",
              font=("Arial", 18),
              bg="blue",
              fg="white",
              width=15,
              command=salary_calculator).pack(pady=20)


def department_management():
    dept = tk.Toplevel(root)
    dept.title("Department Management")
    dept.geometry("600x400")
    dept.config(bg="pink")
    tk.Label(dept, text="Department Name").pack(pady=5)

    dept_entry = tk.Entry(dept, width=30)
    dept_entry.pack()
    from tkinter import ttk

    tree = ttk.Treeview(
        dept,
        columns=("ID", "Department"),
        show="headings"
    )

    tree.heading("ID", text="Department ID")
    tree.heading("Department", text="Department")

    tree.column("ID", width=120)
    tree.column("Department", width=250)

    tree.pack(pady=20)

    def add_department():
        global department_count

        dept_name = dept_entry.get()

        if dept_name == "":
            return

        dept_id = f"DEP{department_count:03d}"
        department_count += 1

        tree.insert("", "end", values=(dept_id, dept_name))

        dept_entry.delete(0, tk.END)

    def update_department():
        selected = tree.focus()

        if selected:
            dept_id = tree.item(selected)["values"][0]
            tree.item(selected,
                      values=(dept_id, dept_entry.get()))

    def delete_department():
        selected = tree.focus()

        if selected:
            tree.delete(selected)

    def select_data(event):
        selected = tree.focus()

        values = tree.item(selected)["values"]

        dept_entry.delete(0, tk.END)
        dept_entry.insert(0, values[1])

        tree.bind("<<TreeviewSelect>>", select_data)

        dept_id = f"DEP{department_count:03d}"
        department_count += 1
        tree.insert("", "end", values=(dept_id, department_name))

    tk.Button(dept, text="Add", command=add_department).pack()
    tk.Button(dept, text="Update", command=update_department).pack()
    tk.Button(dept, text="Delete", command=delete_department).pack()

Frame1 = tk.Frame(root, bg="white")
Frame1.pack(pady=20)

scroll_y = tk.Scrollbar(Frame1, orient=tk.VERTICAL)
scroll_y.pack(side="right", fill=tk.Y)

tree = ttk.Treeview(Frame1,
                    columns=("ID", "Name", "Age", "Department"),
                    show="headings",
                    yscrollcommand=scroll_y.set)

scroll_y.config(command=tree.yview)

tree.heading("ID", text="Employee ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Department", text="Department")

tree.column("ID", width=150, anchor="center")
tree.column("Name", width=200, anchor="center")
tree.column("Age", width=100, anchor="center")
tree.column("Department", width=200, anchor="center")

tree.pack(fill="both", expand=True)

button_frame = tk.Frame(root, bg="#F4F6F9")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Add Employee", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=add_employee).grid(row=0,column=0,pady=5)
tk.Button(button_frame, text="Update Employee", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=update_employee).grid(row=0,column=1,pady=5)
tk.Button(button_frame, text="Delete Employee", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=delete_employee).grid(row=0,column=2,pady=5)
tk.Button(button_frame, text="Search Employee", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=search_employee).grid(row=0,column=3,pady=5)
tk.Button(button_frame, text="Upload Employee Photo", width=20,font=("Segoe UI", 12, "bold"), bg="sky blue",command=upload_employee).grid(row=1,column=0,pady=5)
tk.Button(button_frame, text="Salary Calculator", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=salary_calculator).grid(row=1,column=1,pady=5)
tk.Button(button_frame, text="Department Management", width=20, font=("Segoe UI", 12, "bold"),bg="sky blue",command=department_management).grid(row=1,column=2,pady=5)
tk.Button(button_frame, text="Logout", width=20,font=("Segoe UI", 12, "bold"),bg="sky blue",
          command=lambda: [root.withdraw()]).grid(row=1,column=3,pady=5)

content = tk.Frame(root, bg="white")
content.pack(fill="both", expand=True)

tk.Label(content, text="Welcome to the Employee Management System",
         font=("Arial", 20, "bold"),
         bg="white").pack(pady=20)

loginsystem()
load_data()
root.mainloop()


