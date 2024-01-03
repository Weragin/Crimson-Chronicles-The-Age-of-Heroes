import tkinter as tk
import subprocess
import sys


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height


def exit_application():
    root.quit()


root = tk.Tk()
root.attributes('-fullscreen', True)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = 50
HEIGHT = 50
canvas.bind('<Configure>', canvas_size)

exit_button = tk.Button(root, text="START", command=exit_application)
exit_button.place(x= 1280//2, y=694//2)

root.mainloop()

root.withdraw()
subprocess.run(["python", "build_army.py", str(WIDTH), str(HEIGHT)])
sys.exit()