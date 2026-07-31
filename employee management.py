import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog

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
    dep.add(values[2])
d = len(dep)
file.close()

cards = [
    ("Total Employees", r-1, "#4E73DF"),
    ("Departments",d+1, "#1CC88A"),
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

def loginsystem():
    login = tk.Toplevel(root)
    login.title("Login System")
    login.geometry("400x300")
    login.config(bg="white")

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
        user = username.get()
        pwd = password.get()
        if user == "admin" and pwd == "1234":
            messagebox.showinfo("success", "Login Successful")
            login.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

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






