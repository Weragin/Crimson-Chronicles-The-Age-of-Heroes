import tkinter as tk
import sys
from PIL import Image, ImageTk
import subprocess
import json

# canvas_dimensions = []


def close(e = 0):
    root.withdraw()
    sys.exit()


def next(e = 0):
    str_army = json.dumps(army)
    str_unit_stats = json.dumps(unit_stats)
    root.withdraw()
    subprocess.run(["python", "battle.py", str_army, str_unit_stats])
    sys.exit()


def Warrior(e):
    global money
    if money >= 100:
        money -= 100
        army.append(["warrior", []])
        canvas.itemconfig(money_text, text = money)
        army_add(warrior, small_warrior)



def Knight(e):
    global money
    if money >= 120:
        money -= 120
        army.append(["knight", []])
        canvas.itemconfig(money_text, text = money)
        army_add(knight)


def Vampire(e):
    global money
    if money >= 140:
        money -= 140
        army.append(["vampire", []])
        canvas.itemconfig(money_text, text = money)
        army_add(vampire)


def Defender(e):
    global money
    if money >= 130:
        money -= 130
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(defender)


def Healer(e):
    global money
    if money >= 135:
        money -= 135
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(healer)


def Lancer(e):
    global money
    if money >= 120:
        money -= 120
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(lancer)


def army_add(unit, img = None):
    global tag_height, temp
    object_tag = canvas.find_withtag(unit)
    place = len(army) * 50
    width = 25
    height = 50
    if img == None:
        color = canvas.itemcget(object_tag, "fill")
        temp.append(canvas.create_rectangle(place, tag_height * 3 + 60, place + 20, tag_height * 3 + 80, fill=color, tags=("army")))
    else:
        temp.append(canvas.create_image(place, tag_height * 3 + 60, image = img, anchor = tk.NW, tags=("army")))
    army[-1].append(temp[-1])


def find_unit(e):
    global selected_unit, select_rectangle, W, H
    overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
    size = 5
    temp = [i[-1] for i in army]
    try:
        if selected_unit != "":
            x1, y1, x2, y2 = canvas.coords(temp[selected_unit])
            canvas.coords(temp[selected_unit], x1 + size, y1 + size, x2 - size, y2 - size)
        x1, y1, x2, y2 = canvas.coords(overlap[0])
        selected_unit = temp.index(overlap[0])
        canvas.coords(overlap[0], x1 - size, y1 - size, x2 + size, y2 + size)
    except:
        if selected_unit != "":
            canvas.delete(select_rectangle)
        x1, y1 = canvas.coords(overlap[0])
        selected_unit = temp.index(overlap[0])
        select_rectangle = canvas.create_rectangle(x1 - size, y1 - size, x1 + W + size, y1 + H + size, fill=None, outline="green", width=2)
        
        

def add_weapon(e):
    global selected_unit, temp, money
    try:
        x1, y1, x2, y2 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        if weapons[overlap[0]][-1] <= money:
            army[selected_unit][1].append(weapons[overlap[0]])
            nofweapons = len(army[selected_unit][1])
            color = canvas.itemcget(overlap[0], "fill")
            move = 5 * (nofweapons - 1)
            canvas.create_rectangle(x1 + move, y1 + 40, x2 - 10 + move, y2 + 30, fill=color)
            money -= weapons[overlap[0]][-1]
            canvas.itemconfig(money_text, text = money)
    except:
        x1, y1 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        if weapons[overlap[0]][-1] <= money:
            army[selected_unit][1].append(weapons[overlap[0]])
            nofweapons = len(army[selected_unit][1])
            color = canvas.itemcget(overlap[0], 'fill')
            move = 5 * (nofweapons - 1)
            canvas.create_rectangle(x1 + move, y1 + H + 10, x1 + W - 10 + move, y1 + H + 40, fill=color)
            money -= weapons[overlap[0]][-1]
            canvas.itemconfig(money_text, text = money)


def character_create(x1, y1, x2, y2, stats: list, img = None):
    num = 200//6
    if img == None:
        character = canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    else:
        character = canvas.create_image(x1, y1, image = img, anchor = tk.NW, tags="images")
    for i in range(len(stats)):
        canvas.create_rectangle(x2, y1 + num * i, x2 + num, y1 + num * (i + 1), fill="red")
        canvas.create_text(x2 + 2 * num, y1 + num * i + num//2, text=stats[i], font=('Helvetica 20 bold'))
    return character


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height
    # canvas_dimensions.append(width)
    # canvas_dimensions.append(height)


root = tk.Tk()
root.attributes('-fullscreen', True)

W = 30
H = 60
warrior_img = Image.open("pictures/warrior.png")
small_warrior = warrior_img.resize((W, H))
small_warrior = ImageTk.PhotoImage(small_warrior)
tk_warrior_img = ImageTk.PhotoImage(warrior_img)

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])
# canvas.bind('<Configure>', canvas_size)


exit_button = tk.Button(root, text='EXIT', command=close, width=5)
exit_button.place(x = WIDTH - 50, y = 0)
root.bind('<Escape>', close)

army = []
money = 600
money_text = canvas.create_text(WIDTH - 100, 50, text=money, fill="black", font=('Helvetica 30 bold'))

tag_width = (WIDTH - 300)//3
tag_height = HEIGHT//3 - 50

x = 50
y = 100
unit_stats = {"warrior": [100, 5, 2, 0, 0, 90], "knight": [120, 7, 2, 0, 0, 100], "vampire": [140, 5, 2, 5, 0, 80], "defender": [130, 5, 5, 0, 0, 150], "healer": [135, 0, 2, 0, 5, 80], "lancer": [120, 7, 2, 0, 0, 90]}
warrior = character_create(tag_width - x, tag_height - y, tag_width + x, tag_height + y, unit_stats["warrior"], tk_warrior_img)
canvas.tag_bind(warrior, "<ButtonPress-1>", Warrior)

knight = character_create(tag_width*2 - x, tag_height - y, tag_width*2 + x, tag_height + y, unit_stats["knight"], None)
canvas.tag_bind(knight, "<ButtonPress-1>", Knight)

vampire = character_create(tag_width*3 - x, tag_height - y, tag_width*3 + x, tag_height + y, unit_stats["vampire"], None)
canvas.tag_bind(vampire, "<ButtonPress-1>", Vampire)

defender = character_create(tag_width - x, tag_height * 2 - y + 50, tag_width + x, tag_height * 2 + y + 50, unit_stats["defender"], None)
canvas.tag_bind(defender, "<ButtonPress-1>", Defender)

healer = character_create(tag_width*2 - x, tag_height * 2 - y + 50, tag_width*2 + x, tag_height * 2 + y + 50, unit_stats["healer"], None)
canvas.tag_bind(healer, "<ButtonPress-1>", Healer)

lancer = character_create(tag_width*3 - x, tag_height * 2 - y + 50, tag_width*3 + x, tag_height * 2 + y + 50, unit_stats["lancer"], None)
canvas.tag_bind(lancer, "<ButtonPress-1>", Lancer)

canvas.create_line(0, tag_height * 3, WIDTH, tag_height * 3)
canvas.create_text(60, tag_height*3 + 30, text="ARMY", fill="black", font=('Helvetica 30 bold'))

weapons = {}
spacing = WIDTH//6
sword = canvas.create_rectangle(WIDTH//2, tag_height*3 + 20, WIDTH//2 + 20, tag_height*3 + 40, fill="orange", tags="weapons")
weapons[sword] = [5, 2, 0, 0, 0, 50]
shield = canvas.create_rectangle(WIDTH//2 + spacing, tag_height*3 + 20, WIDTH//2 + spacing + 20, tag_height*3 + 40, fill="brown", tags="weapons")
weapons[shield] = [20, -1, 2, 0, 0, 50]
greatAxe = canvas.create_rectangle(WIDTH//2 + 2*spacing, tag_height*3 + 20, WIDTH//2 + 2*spacing + 20, tag_height*3 + 40, fill="magenta", tags="weapons")
weapons[greatAxe] = [-15, 5, -2, 0.1, 0, 70]
katana = canvas.create_rectangle(WIDTH//2, tag_height*3 + 100, WIDTH//2 + 20, tag_height*3 + 120, fill="grey", tags="weapons")
weapons[katana] = [-20, 6, -5, 0.5, 0, 100]
magicWand = canvas.create_rectangle(WIDTH//2 + spacing, tag_height * 3 + 100, WIDTH//2 + spacing + 20, tag_height*3 + 120, fill="purple", tags="weapons")
weapons[magicWand] = [30, 3, 0, 0, 3, 80]

canvas.tag_bind("weapons", "<ButtonPress-1>", add_weapon)

temp = []
selected_unit = ""
canvas.tag_bind("army", "<ButtonPress-1>", find_unit)

root.bind("<Return>", next)
next_button = tk.Button(root, text="Next", command=next, width=5)
next_button.place(x = WIDTH - 50, y = HEIGHT//2)

root.mainloop()