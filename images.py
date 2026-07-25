from tkinter import *
from PIL import Image,ImageTk
root=Tk()
root.title("My Project")
root.geometry("200x100")
root.config(bg="blue")

Label(root,text="My Project",
      font=("Arial",18,"bold"),
      bg="yellow",
      fg="red").pack(pady=10)

# 1. Open the original image using Pillow
original_img1 = Image.open("ChatGPT Image Jul 18, 2026, 04_35_26 PM.png")
original_img2 = Image.open("Gemini_Generated_Image_dhiwv8dhiwv8dhiw.png")
original_img3 = Image.open("ChatGPT Image Jul 3, 2026, 06_27_27 PM.png")

# 2. Resize the image to exact pixel dimensions (Width, Height)
resized_img1 = original_img1.resize((200, 150), Image.Resampling.LANCZOS)
resized_img2 = original_img2.resize((200, 150), Image.Resampling.LANCZOS)
resized_img3 = original_img3.resize((200, 150), Image.Resampling.LANCZOS)

# 3. Convert the resized Pillow image into a Tkinter-compatible photo image
tk_img1 = ImageTk.PhotoImage(resized_img1)
tk_img2 = ImageTk.PhotoImage(resized_img2)
tk_img3 = ImageTk.PhotoImage(resized_img3)

image_label=Label(root)
image_label.pack(pady=20)

def show_image1():
    image_label.config(width=500, height=250)
    image_label.config(image=tk_img1)

def show_image2():
    image_label.config(width=500, height=250)
    image_label.config(image=tk_img2)

def show_image3():
    image_label.config(width=500, height=250)
    image_label.config(image=tk_img3)

Button(root,text="Image 1",width=15,command=show_image1).pack(pady=5)
Button(root,text="Image 2",width=15,command=show_image2).pack(pady=5)
Button(root,text="Image 3",width=15,command=show_image3).pack(pady=5)
Button(root,text="Exit",width=15,command=root.destroy).pack(pady=5)
root.mainloop()