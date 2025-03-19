
from tkinter import *

root = Tk()
# widthxheight
root.geometry("1200x1000")
# width,height
root.minsize(200, 100)
root.maxsize(1400, 1200)

# Label for heading
#Important label options
#text - adds text
#bd - background
#fg - foreground
#font - sets the font &size
#1.font= ("Ariel", 16, "bold")
#2.font= "Ariel 16 bold"
#padx - x padding
#pady - y padding
#relief - border styling - Sunken,Raised,Groove,Ridge
Label(
    text="Welcome to Token Trading System",
    bg="",  # Background color
    fg="white",  # Foreground text color
    padx=20,
    pady=10,
    font=("Ariel", 16, "bold"),
    borderwidth=5,
    relief=RIDGE
).pack()

# Load Image
try:
    photo = PhotoImage(file="RUET.png")  # Ensure the file exists
    img_label = Label(root, image=photo)
    img_label.image = photo  # Keep a reference to avoid garbage collection
    img_label.pack()
except Exception as e:
    print(f"Error loading image: {e}")

root.mainloop()
