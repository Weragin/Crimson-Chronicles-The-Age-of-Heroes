import json
import subprocess
import sys
import tkinter as tk

from PIL import Image, ImageTk

# canvas_dimensions = []


def close(e = 0):
    root.withdraw()
    sys.exit()


def next(e = 0):
    str_army = json.dumps(army)
    str_unit_stats = json.dumps(unit_stats)
    root.withdraw()
    subprocess.run(["python", "battle.py", str_army, str_unit_stats, str(WIDTH), str(HEIGHT)])
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
        army_add(knight, small_knight)


def Vampire(e):
    global money
    if money >= 140:
        money -= 140
        army.append(["vampire", []])
        canvas.itemconfig(money_text, text = money)
        army_add(vampire, small_vampire)


def Defender(e):
    global money
    if money >= 130:
        money -= 130
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(defender, small_defender)


def Healer(e):
    global money
    if money >= 135:
        money -= 135
        army.append(["healer", []])
        canvas.itemconfig(money_text, text = money)
        army_add(healer, small_healer)


def Lancer(e):
    global money
    if money >= 120:
        money -= 120
        army.append(["lancer", []])
        canvas.itemconfig(money_text, text = money)
        army_add(lancer)


def army_add(unit, img = None):
    global tag_height, temp
    object_tag = canvas.find_withtag(unit)
    place = len(army) * 50
    if img == None:
        color = canvas.itemcget(object_tag, "fill")
        temp.append(canvas.create_rectangle(place + 100, tag_height * 3 + 10, place + 120, tag_height * 3 + 30, fill=color, tags=("army")))
    else:
        temp.append(canvas.create_image(place + 100, tag_height * 3 + 10, image = img, anchor = tk.NW, tags=("army")))
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
    if selected_unit != "":
        x1, y1 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        if weapons[overlap[0]][-1] <= money:
            army[selected_unit][1].append(weapons[overlap[0]])
            nofweapons = len(army[selected_unit][1])
            img = canvas.itemcget(overlap[0], 'image')
            move = 5 * (nofweapons - 1)
            canvas.create_image(x1 + move, y1 + H + 10, image = small_weapon_tags[img], anchor = 'nw')
            money -= weapons[overlap[0]][-1]
            canvas.itemconfig(money_text, text = money)


def character_create(x1, y1, x2, y2, stats: list, img = None):
    global icon_tags
    num = 200//6
    if img == None:
        character = canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    else:
        character = canvas.create_image(x1, y1, image = img, anchor = tk.NW, tags="images")
    for i in range(len(stats)):
        canvas.create_image(x2, y1 + num * i, image = icon_tags[i], anchor = 'nw')
        canvas.create_text(x2 + 2 * num, y1 + num * i + num//2, text=stats[i], font=('Helvetica 20 bold'))
    return character


def weapon_create(x1, y1, x2 = None, y2 = None, stats = [0, 0, 0, 0, 0, 0], img = None):
    global HEIGHT, WIDTH, tag_width, small_icon_tags
    s = ["hp", "atk", "def", "vamp", "heal", "cost"]
    stats[3] = str(stats[3]*100)+'%'
    num = (y2 - y1)//2
    if img == None:
        weapon = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", tags="weapons")
    else:
        weapon = canvas.create_image(x1, y1, image = img, anchor = 'nw', tags = "weapons")
    for i in range(2):
        for j in range(3):
            # canvas.create_rectangle(x2 + num * i * 2.5, y1 + num * j, x2 + num * (i+1) + num * i * 1.5, y1 + num * (j+1), fill="red")
            canvas.create_image(x2 + num * i * 2.5, y1 + num * j, image = small_icon_tags[j+3*i], anchor = 'nw')
            canvas.create_text(x2 + num * (i + 1.7) + num * i * 2, (y1 + y2)//2 - (y2 - y1)//4 + num * j, text=stats[j+3*i], font=("Helvetica 16 bold"))
    stats[3] = float(stats[3][0:-1])/100
    return weapon


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

knight_img = Image.open("pictures/knight.png")
tk_knight_img = ImageTk.PhotoImage(knight_img)
small_knight = knight_img.resize((W, H))
small_knight = ImageTk.PhotoImage(small_knight)

vampire_img = Image.open("pictures/vampire.png")
tk_vampire_img = ImageTk.PhotoImage(vampire_img)
small_vampire = vampire_img.resize((W, H))
small_vampire = ImageTk.PhotoImage(small_vampire)

defender_img = Image.open("pictures/defender.png")
tk_defender_img = ImageTk.PhotoImage(defender_img)
small_defender = defender_img.resize((W, H))
small_defender = ImageTk.PhotoImage(small_defender)

healer_img = Image.open("pictures/healer.png")
tk_healer_img = ImageTk.PhotoImage(healer_img)
small_healer = healer_img.resize((W, H))
small_healer = ImageTk.PhotoImage(small_healer)

icon_names = ["pictures/icons/heart.png", "pictures/icons/attack.png", "pictures/icons/defense.png", "pictures/icons/vampirsm.png", "pictures/icons/heal.png", "pictures/icons/price.png"]
icon_tags = []
small_icon_tags = []
for i in icon_names:
    icon_img = Image.open(i)
    icon_tags.append(ImageTk.PhotoImage(icon_img))
    small_icon = icon_img.resize((25, 25))
    small_icon_tags.append(ImageTk.PhotoImage(small_icon))

weapon_file = ["pictures/weapons/sword.png", "pictures/weapons/shield.png", "pictures/weapons/axe.png", "pictures/weapons/katana.png", "pictures/weapons/magic_wand.png"]
weapon_tags = []
small_weapon_tags = {}
for i in weapon_file:
    weapon_img = Image.open(i)
    weapon_tags.append(ImageTk.PhotoImage(weapon_img))
    small_weapon = weapon_img.resize((25, 37))
    small_weapon_tags[str(weapon_tags[-1])] = ImageTk.PhotoImage(small_weapon)

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])

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
warrior = character_create(x, tag_height - y, 3 * x, tag_height + y, unit_stats["warrior"], tk_warrior_img)
canvas.tag_bind(warrior, "<ButtonPress-1>", Warrior)

knight = character_create(tag_width, tag_height - y, tag_width + 2*x, tag_height + y, unit_stats["knight"], tk_knight_img)
canvas.tag_bind(knight, "<ButtonPress-1>", Knight)

vampire = character_create(tag_width*2 - x, tag_height - y, tag_width*2 + x, tag_height + y, unit_stats["vampire"], tk_vampire_img)
canvas.tag_bind(vampire, "<ButtonPress-1>", Vampire)

defender = character_create(x, tag_height * 2 - y + 50, 3 * x, tag_height * 2 + y + 50, unit_stats["defender"], tk_defender_img)
canvas.tag_bind(defender, "<ButtonPress-1>", Defender)

healer = character_create(tag_width, tag_height * 2 - y + 50, tag_width + 2*x, tag_height * 2 + y + 50, unit_stats["healer"], tk_healer_img)
canvas.tag_bind(healer, "<ButtonPress-1>", Healer)

lancer = character_create(tag_width*2 - x, tag_height * 2 - y + 50, tag_width*2 + x, tag_height * 2 + y + 50, unit_stats["lancer"], None)
canvas.tag_bind(lancer, "<ButtonPress-1>", Lancer)

canvas.create_line(0, tag_height * 3 - 25, WIDTH, tag_height * 3 - 25)
canvas.create_text(60, tag_height*3, text="ARMY", fill="black", font=('Helvetica 30 bold'))

weapons = {}
spacing = WIDTH//6
hspace = (HEIGHT - tag_height)//5
wx1 = tag_width * 3 - x//2
wx2 = tag_width * 3 + x//2
weapon_stats = [[5, 2, 0, 0, 0, 50], [20, -1, 2, 0, 0, 50], [-15, 5, -2, 0.1, 0, 70], [-20, 6, -5, 0.5, 0, 100], [30, 3, 0, 0, 3, 80]]
for i in range(5):
    temp = weapon_create(wx1, 25 + i*hspace, wx2, 75 + hspace*i, weapon_stats[i], weapon_tags[i])
    weapons[temp] = weapon_stats[i]

canvas.tag_bind("weapons", "<ButtonPress-1>", add_weapon)

temp = []
selected_unit = ""
canvas.tag_bind("army", "<ButtonPress-1>", find_unit)

root.bind("<Return>", next)
next_button = tk.Button(root, text="Next", command=next, width=5)
next_button.place(x = WIDTH - 50, y = HEIGHT//2)

root.mainloop()
