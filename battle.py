import sys
import json
import tkinter as tk
from PIL import Image, ImageTk


def close(e = 0):
    root.withdraw()
    sys.exit()


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height


root = tk.Tk()
root.attributes('-fullscreen', True)

warrior_img = Image.open("pictures/warrior.png")
tk_warrior_img = ImageTk.PhotoImage(warrior_img)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = 1250
HEIGHT = 695
canvas.bind("<Configure>", canvas_size)

exit_button = tk.Button(root, text='EXIT', command=close)
exit_button.place(x = WIDTH, y = 0)
root.bind('<Escape>', close)

army = sys.argv[1]
army = json.loads(army)
print(army)

unit_stats = sys.argv[2]
unit_stats = json.loads(unit_stats)
print(unit_stats)
# stats- hp, atk, def, vamp, heal, cost



root.mainloop()