from tkinter import *
from tkinter import messagebox
root=Tk()
root.title("TODO LIST")
root.geometry("400x300")
root.config(bg="white")

def addtask():
    addtask=addtask_entry.get()
    if addtask!="":
        add_listbox.insert(END,addtask)
        addtask_entry.delete(0,END)
    else:
        messagebox.showerror("failed")

def clear_all():
    add_listbox.delete(0,END)

def deletetask():
    try:
        selected_addtask_index=add_listbox.curselection()[0]
        add_listbox.delete(selected_addtask_index)
    except IndexError:
        messagebox.showwarning("Warning","you must select a task to delete.")

Label(root,text="TODO LIST",
       font=("Arial",20,"bold"),
       bg="white",
       fg="red").pack(pady=20)

Frame1=Frame(root,bg="white")
Frame1.pack(pady=20)

addtask_entry=Entry(Frame1,font=("Arial",12),width=25)
addtask_entry.grid(row=0,column=1,padx=10)

Button(Frame1,text="Add Task",
       font=("Arial",12),
       bg="yellow",
       fg="green",
       command=addtask).grid(row=0,column=0,padx=10)

add_listbox=Listbox(root,font=("Arial",12),width=28,height=10)
add_listbox.pack(pady=20)

Button(Frame1,text="Clear all",
       font=("Arial",12),
       bg="blue",
       fg="white",
       width=15,
       command=clear_all).grid(row=5,column=0,padx=10)

Button(Frame1,text="Delete Task",
       font=("Arial",12),
       bg="red",
       fg="white",
       width=15,
       command=deletetask).grid(row=5,column=1,padx=10)
root.mainloop()
