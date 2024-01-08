import sys
import tkinter as tk

from PIL import Image, ImageTk


def exit_application(e):
    root.quit()


root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

match sys.argv[1]:
    case "win":
        background = Image.open("pictures/bg/crimson_chronicles.png").resize((WIDTH, HEIGHT))
    case _:
        background = Image.open("pictures/bg/crimson_chronicles.png").resize((WIDTH, HEIGHT))

tk_background = ImageTk.PhotoImage(background)
canvas.create_image(0, 0, image = tk_background, anchor = 'nw')

root.bind("<Key>", exit_application)
root.mainloop()
