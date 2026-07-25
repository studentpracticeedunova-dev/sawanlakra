# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
#
#
# print("this is new line ")
#
#
# print("hello")

# import tkinter as tk
# from tkinter import messagebox
#
# root = tk.Tk()
# root.title("Employee Management System")
# root.geometry("800x500")
#
#
# def save_employee():
#     name = name_entry.get()
#     age = age_entry.get()
#     department = dept_entry.get()
#
#     if name == "" or age == "" or department == "":
#         messagebox.showerror("Error", "All fields are required")
#     else:
#         messagebox.showinfo("Success", "Employee Added Successfully")
#
#
# def open_add_employee():
#
#     add_win = tk.Toplevel(root)
#     add_win.title("Add Employee")
#     add_win.geometry("400x350")
#     add_win.resizable(False, False)
#
#     tk.Label(add_win, text="Add Employee",
#              font=("Arial", 16, "bold")).pack(pady=10)
#
#     tk.Label(add_win, text="Employee Name").pack()
#     global name_entry
#     name_entry = tk.Entry(add_win, width=30)
#     name_entry.pack(pady=5)
#
#     tk.Label(add_win, text="Age").pack()
#     global age_entry
#     age_entry = tk.Entry(add_win, width=30)
#     age_entry.pack(pady=5)
#
#     tk.Label(add_win, text="Department").pack()
#     global dept_entry
#     dept_entry = tk.Entry(add_win, width=30)
#     dept_entry.pack(pady=5)
#
#     tk.Button(add_win,
#               text="Save Employee",
#               command=save_employee,
#               bg="green",
#               fg="white",
#               width=20).pack(pady=20)
#
#
# tk.Button(root,
#           text="Add Employee",
#           command=open_add_employee,
#           width=20).pack(pady=50)
#
# root.mainloop()


#
# import tkinter as tk
#
# root = tk.Tk()
# root.title('Library Management System')
# root.geometry('500x400')
#
# # ---------- Functions ----------
# def open_add_book():
#     win = tk.Toplevel(root)
#     win.title('Add Book')
#     win.geometry('300x200')
#     tk.Label(win, text='Add Book Window', font=('Arial', 14)).pack(pady=20)
#
# def open_update_book():
#     win = tk.Toplevel(root)
#     win.title('Update Book')
#     win.geometry('300x200')
#     tk.Label(win, text='Update Book Window', font=('Arial', 14)).pack(pady=20)
#
# def open_delete_book():
#     win = tk.Toplevel(root)
#     win.title('Delete Book')
#     win.geometry('300x200')
#     tk.Label(win, text='Delete Book Window', font=('Arial', 14)).pack(pady=20)
#
# def open_view_books():
#     win = tk.Toplevel(root)
#     win.title('View Books')
#     win.geometry('300x200')
#     tk.Label(win, text='View Books Window', font=('Arial', 14)).pack(pady=20)
#
# def open_issue_book():
#     win = tk.Toplevel(root)
#     win.title('Issue Book')
#     win.geometry('300x200')
#     tk.Label(win, text='Issue Book Window', font=('Arial', 14)).pack(pady=20)
#
# def open_return_book():
#     win = tk.Toplevel(root)
#     win.title('Return Book')
#     win.geometry('300x200')
#     tk.Label(win, text='Return Book Window', font=('Arial', 14)).pack(pady=20)
#
# # ---------- Main Buttons ----------
# tk.Label(root, text='Library Dashboard', font=('Arial', 18, 'bold')).pack(pady=20)
#
# tk.Button(root, text='Add Book', width=20, command=open_add_book).pack(pady=5)
# tk.Button(root, text='Update Book', width=20, command=open_update_book).pack(pady=5)
# tk.Button(root, text='Delete Book', width=20, command=open_delete_book).pack(pady=5)
# tk.Button(root, text='View Books', width=20, command=open_view_books).pack(pady=5)
# tk.Button(root, text='Issue Book', width=20, command=open_issue_book).pack(pady=5)
# tk.Button(root, text='Return Book', width=20, command=open_return_book).pack(pady=5)
#
# root.mainloop()