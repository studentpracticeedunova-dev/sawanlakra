# from tkinter import *
# from tkinter import messagebox
#
# root=Tk()
# root.title("Signupform")
# root.geometry("400x300")
# root.config(bg="white")
#
# def sign():
#     name=name_entry.get()
#     email=email_entry.get()
#     password=password_entry.get()
#     confirmpassword=confirmpassword_entry.get()
#
#     if name=="sawan" and email=="sawanlakra987" and password=="1234" and confirmpassword=="1234":
#         messagebox.showinfo("sign","sign in successfully")
#     else:
#         messagebox.showerror("failed")
#
# def clear():
#     name_entry.delete(0,END)
#     email_entry.delete(0,END)
#     password_entry.delete(0,END)
#     confirmpassword_entry.delete(0,END)
#
# Label(root,text="signupform",
#       font=("Arial",20,"bold"),
#       bg="white",
#       fg="blue").pack(pady=20)
#
# Frame1=Frame(root,bg="white")
# Frame1.pack(pady=20)
#
# Label(Frame1,text="Name",
#       font=("Arial",18),
#       bg="yellow",
#       fg="black").grid(row=0,column=0,padx=5)
# name_entry=Entry(Frame1,text="Name",font=("Arial",18))
# name_entry.grid(row=0,column=1,padx=5)
#
# Label(Frame1,text="Email",
#       font=("Arial",18),
#       bg="yellow",
#       fg="black").grid(row=1,column=0,padx=5)
# email_entry=Entry(Frame1,text="Email",font=("Arial",18))
# email_entry.grid(row=1,column=1,padx=5)
#
# Label(Frame1,text="Password",
#       font=("Arial",18),
#       bg="yellow",
#       fg="black").grid(row=2,column=0,padx=5)
# password_entry=Entry(Frame1,text="Password",font=("Arial",18))
# password_entry.grid(row=2,column=1,padx=5)
#
# Label(Frame1,text="Confirm Password",
#       font=("Arial",18),
#       bg="yellow",
#       fg="black").grid(row=3,column=0,padx=5)
# confirmpassword_entry=Entry(Frame1,text="Confirm Password",font=("Arial",18))
# confirmpassword_entry.grid(row=3,column=1,padx=5)
#
# Button(Frame1,text="Sign",
#        font=("Arial",18),
#        bg="blue",
#        fg="white",
#        command=sign).grid(row=4,column=0,padx=5)
#
# Button(Frame1,text="Clear",
#        font=("Arial",18),
#        bg="red",
#        fg="white",
#        command=clear).grid(row=4,column=1,padx=5)
#
# root.mainloop()


import tkinter as tk
from tkinter import messagebox

# ---------------- MAIN ROOT ----------------
root = tk.Tk()
root.title("Employee Management System")
root.geometry("900x600")
root.configure(bg="white")

# Hide main window first
root.withdraw()


# ---------------- LOGIN WINDOW ----------------
def open_login():

    login = tk.Toplevel(root)
    login.title("Employee Login")
    login.geometry("400x300")
    login.resizable(False, False)

    tk.Label(login,
             text="Employee Login",
             font=("Arial", 18, "bold")).pack(pady=20)

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
            messagebox.showinfo("Success", "Login Successful")
            login.destroy()
            root.deiconify()      # Show Main Window

        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    tk.Button(login,
              text="Login",
              command=login_user,
              bg="green",
              fg="white",
              width=15).pack(pady=20)

    def close_app():
        root.destroy()

    login.protocol("WM_DELETE_WINDOW", close_app)


# ---------------- MAIN WINDOW ----------------

title = tk.Label(root,
                 text="EMPLOYEE MANAGEMENT SYSTEM",
                 font=("Arial", 22, "bold"),
                 bg="navy",
                 fg="white",
                 pady=15)

title.pack(fill="x")

menu_frame = tk.Frame(root, bg="#f0f0f0", width=200)
menu_frame.pack(side="left", fill="y")

tk.Button(menu_frame, text="Add Employee", width=20).pack(pady=15)

tk.Button(menu_frame, text="View Employee", width=20).pack(pady=15)

tk.Button(menu_frame, text="Update Employee", width=20).pack(pady=15)

tk.Button(menu_frame, text="Delete Employee", width=20).pack(pady=15)

tk.Button(menu_frame, text="Logout", width=20,
          command=lambda: [root.withdraw(), open_login()]).pack(pady=30)

content = tk.Frame(root, bg="white")
content.pack(fill="both", expand=True)

tk.Label(content,
         text="Welcome to Employee Management System",
         font=("Arial", 20),
         bg="white").pack(pady=100)


# Start Login
open_login()

root.mainloop()