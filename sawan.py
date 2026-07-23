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
