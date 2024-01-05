import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height


def exit_application(e):
    root.quit()


root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
canvas.bind('<Configure>', canvas_size)

background = Image.open("pictures/bg/crimson_chronicles.png").resize((WIDTH, HEIGHT))
tk_background = ImageTk.PhotoImage(background)
canvas.create_image(0, 0, image = tk_background, anchor = 'nw')

root.bind("<Key>", exit_application)
root.mainloop()

root.withdraw()
subprocess.run(["python", "build_army.py", str(WIDTH), str(HEIGHT)])
sys.exit()