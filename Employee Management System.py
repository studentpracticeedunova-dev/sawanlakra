# import tkinter as tk
# from tkinter import messagebox
#
# root=tk.Tk()
# root.title("Employee Management System")
# root.geometry("500x500")
# root.config(bg="white")
#
# root.withdraw()
#
# tk.Label(root,text="Employee Management System",
#       font=("Arial",18,"bold"),
#       bg="white",
#       fg="black").pack(pady=20)
#
# def loginsystem():
#     login=tk.Toplevel(root)
#     login.title("Login System")
#     login.geometry("400x300")
#     login.config(bg="white")
#     login.resizable(False,False)
#     tk.Label(login,text="Login System",font=("Arial",20,"bold")).pack(pady=20)
#
#     tk.Label(login,text="Username").pack()
#     username=tk.Entry(login,width=30)
#     username.pack(pady=5)
#
#     tk.Label(login, text="Password").pack()
#     password = tk.Entry(login, show="*", width=30)
#     password.pack(pady=5)
#
#     def login_user():
#         user=username.get()
#         pwd=password.get()
#         if user=="admin" and pwd=="1234":
#             messagebox.showinfo("success","Login Successful")
#             login.destroy()
#             root.deiconify()
#         else:
#             messagebox.showerror("Error","Invalid Username or Password")
#
#     tk.Button(login,text="Login",
#            font=("Arial",18),
#            bg="blue",
#            fg="black",
#            command=login_user,
#            width=15).pack(pady=20)
#
#     def close_app():
#         root.destroy()
#
#     login.protocol("WM_DELETE_WINDOW",close_app)
#
#     def add_user():
#         name = name_entry.get()
#         age = age_entry.get()
#         dep = dep_entry.get()
#         if name == "" and age == "" and dep == "":
#             messagebox.showerror("success", "sucessful")
#             add.destroy()
#             root.deiconify()
#         else:
#             messagebox.showinfo("failed")
#
# def add_employee():
#     add = tk.Toplevel(root)
#     add.title("Add Employee")
#     add.geometry("400x300")
#     add.config(bg="white")
#     add.resizable(False, False)
#     tk.Label(add, text="Add Employee", width=20).pack(pady=20)
#
#     tk.Label(add,text="Name").pack()
#     name_entry=tk.Entry(add,width=30)
#     name_entry.grid(row=0,column=1,padx=5)
#
#     tk.Label(add, text="age").pack()
#     age_entry = tk.Entry(add, width=30)
#     age_entry.grid(row=0, column=1, padx=5)
#
#     tk.Label(add, text="dep").pack()
#     dep_entry = tk.Entry(add, width=30)
#     dep_entry.grid(row=0, column=1, padx=5)
#
#
#
#     tk.Button(add,text="Add Employee",
#                 font=("Arial",18),
#                 bg="white",
#                 fg="black",
#                 width=15,
#                 command=add_user).pack(pady=20)
#
#         # def close_app():
#         #    root.destroy()
#         # add.protocol("WM_DELETE_WINDOW",close_app)
#
# def update_employee():
#     update = tk.Toplevel(root)
#     update.title("Update Employee")
#     update.geometry("400x300")
#     tk.Label(update, text="Update Employee",font=("Arial",18)).pack(pady=20)
#
# def delete_employee():
#     delete = tk.Toplevel(root)
#     delete.title("Delete Employee")
#     delete.geometry("400x300")
#     tk.Label(delete,text="Delete Employee",font=("Arial",18)).pack(pady=20)
#
# def search_employee():
#     search = tk.Toplevel(root)
#     search.title("Search Employee")
#     search.geometry("400x300")
#     tk.Label(search,text="Search Employee",font=("Arial",18)).pack(pady=20)
#
# def upload_employee():
#     upload = tk.Toplevel(root)
#     upload.title("Upload Employee")
#     upload.geometry("400x300")
#     tk.Label(upload,text="Upload Employee",font=("Araial",18)).pack(pady=20)
#
# def salary_calculator():
#     salary = tk.Toplevel(root)
#     salary.title("Salary Calculator")
#     salary.geometry("400x300")
#     tk.Label(salary,text="Salary Calculator",font=("Arial",18)).pack(pady=20)
#
# def department_management():
#     department = tk.Toplevel(root)
#     department.title("Department Management")
#     department.geometry("400x300")
#     tk.Label(department,text="Department Management",font=("Arial",18)).pack(pady=20)
#
# # tk.Button(root,text="Add Employee",
# #           width=20,
# #           command=add_employee).pack(pady=50)
#
#
#
# title=tk.Label(root,text="Employee Management System",
#                font=("Arial",18,"bold"),
#                bg="navy",
#                fg="black",
#                pady=15)
#
# title.pack(fill="x")
#
# Frame1=tk.Frame(root,bg="white")
# Frame1.pack(pady=20)
#
# tk.Button(Frame1,text="Add Employee",width=20,command=add_employee).grid(row=0,column=0,pady=5)
# tk.Button(Frame1,text="Update Employee",width=20,command=update_employee).grid(row=0,column=1,pady=5)
# tk.Button(Frame1,text="Delete Employee",width=20,command=delete_employee).grid(row=0,column=2,pady=5)
# tk.Button(Frame1,text="Search Employee",width=20,command=search_employee).grid(row=0,column=3,pady=5)
# tk.Button(Frame1,text="Upload Employee Photo",width=20,command=upload_employee).grid(row=0,column=4,pady=5)
# tk.Button(Frame1,text="Salary Calculator",width=20,command=salary_calculator).grid(row=0,column=5,pady=5)
# tk.Button(Frame1,text="Department Management",width=20,command=department_management).grid(row=0,column=6,pady=5)
# tk.Button(Frame1,text="Logout",width=30,
#           command=lambda:[root.withdraw(),loginsystem()]).grid(row=0,column=7,pady=5)
#
# content=tk.Frame(root,bg="white")
# content.pack(fill="both", expand=True)
#
# tk.Label(content,text="Welcome to the Employee Management System",
#          font=("Arial",20,"bold"),
#          bg="white").pack(pady=20)
#
# loginsystem()
#
# root.mainloop()