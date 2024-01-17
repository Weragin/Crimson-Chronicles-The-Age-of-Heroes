import json
import subprocess
import sys
import tkinter as tk

from PIL import Image, ImageTk


def close(e = 0):
    root.withdraw()
    sys.exit()


def next(e = 0):
    str_army = json.dumps(army)
    str_unit_stats = json.dumps(unit_stats)
    root.withdraw()
    subprocess.run([sys.executable, "battle.py", str_army, str_unit_stats, str(WIDTH), str(HEIGHT)])
    sys.exit()


def Warrior(e):
    army.append(["warrior", []])
    army_add(warrior, small_warrior, "warrior")


def Knight(e):
    army.append(["knight", []])
    army_add(knight, small_knight, "knight")


def Vampire(e):
    army.append(["vampire", []])
    army_add(vampire, small_vampire, "vampire")


def Defender(e):
    army.append(["defender", []])
    army_add(defender, small_defender, "defender")


def Healer(e):
    army.append(["healer", []])
    army_add(healer, small_healer, 'healer')


def Lancer(e):
    army.append(["lancer", []])
    army_add(lancer, small_lancer, "lancer")


def army_add(unit, img = None, unit_str = "warrior"):
    img = img or small_warrior
    global tag_height, temp, money
    if len(army) <= 6:
        cost = unit_stats[unit_str][-1]
        money -= cost
        canvas.itemconfig(money_text, text = money)
        object_tag = canvas.find_withtag(unit)
        place = len(army) * 50
        temp.append(canvas.create_image(place + 100, tag_height * 3 + 10, image = img, anchor = tk.NW, tags=("army")))
        army[-1].append(temp[-1])



def find_unit(e):
    global selected_unit, select_rectangle, W, H
    overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
    size = 5
    temp = [i[-1] for i in army]
    if selected_unit != "":
        canvas.delete(select_rectangle)
    x1, y1 = canvas.coords(overlap[1])
    selected_unit = temp.index(overlap[1])
    select_rectangle = canvas.create_rectangle(x1 - size, y1 - size, x1 + W + size, y1 + H + size, fill=None, outline="green", width=2)
        

def add_weapon(e):
    global selected_unit, temp, money
    if selected_unit != "":
        x1, y1 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        if weapons[overlap[1]][-1] <= money:
            army[selected_unit][1].append(weapons[overlap[1]])
            nofweapons = len(army[selected_unit][1])
            img = canvas.itemcget(overlap[1], 'image')
            move = 5 * (nofweapons - 1)
            canvas.create_image(x1 + move, y1 + H + 10, image = small_weapon_tags[img], anchor = 'nw')
            money -= weapons[overlap[1]][-1]
            canvas.itemconfig(money_text, text = money)


def character_create(x1, y1, x2, y2, stats: list, img = None):
    img = img or tk_warrior_img
    global icon_tags
    num = 200//6
    stats[3] = str(stats[3]*100)+'%'
    character = canvas.create_image(x1, y1, image = img, anchor = tk.NW, tags="images")
    for i in range(len(stats)):
        canvas.create_image(x2, y1 + num * i, image = icon_tags[i], anchor = 'nw')
        canvas.create_text(x2 + 2 * num, y1 + num * i + num//2, text=stats[i], font=('Helvetica 20 bold'))
    stats[3] = float(stats[3][0:-1])/100
    return character


def weapon_create(x1, y1, x2 = None, y2 = None, stats = [0, 0, 0, 0, 0, 0], img = None):
    # img sets default img to sword img
    img = img or weapon_tags[0]
    global HEIGHT, WIDTH, tag_width, small_icon_tags
    s = ["hp", "atk", "def", "vamp", "heal", "cost"]
    stats[3] = str(stats[3]*100)+'%'
    num = (y2 - y1)//2
    weapon = canvas.create_image(x1, y1, image = img, anchor = 'nw', tags = "weapons")
    for i in range(2):
        for j in range(3):
            canvas.create_image(x2 + num * i * 2.5, y1 + num * j, image = small_icon_tags[j+3*i], anchor = 'nw')
            canvas.create_text(x2 + num * (i + 1.7) + num * i * 2, (y1 + y2)//2 - (y2 - y1)//4 + num * j, text=stats[j+3*i], font=("Helvetica 16 bold"))
    stats[3] = float(stats[3][0:-1])/100
    return weapon


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height


root = tk.Tk()
root.attributes('-fullscreen', True)

WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])

x = int(WIDTH//25)          # 50
y = int(HEIGHT//7.2)        # 100
print(x, y)

pic_x = int(WIDTH//12.8)    # 100
pic_y = int(HEIGHT//3.6)    # 200
W = int(WIDTH//42.6)
H = int(HEIGHT//12)
warrior_img = Image.open("pictures/warrior.png").resize((pic_x, pic_y))
small_warrior = warrior_img.resize((W, H))
small_warrior = ImageTk.PhotoImage(small_warrior)
tk_warrior_img = ImageTk.PhotoImage(warrior_img)

knight_img = Image.open("pictures/knight.png").resize((pic_x, pic_y))
tk_knight_img = ImageTk.PhotoImage(knight_img)
small_knight = knight_img.resize((W, H))
small_knight = ImageTk.PhotoImage(small_knight)

vampire_img = Image.open("pictures/vampire.png").resize((pic_x, pic_y))
tk_vampire_img = ImageTk.PhotoImage(vampire_img)
small_vampire = vampire_img.resize((W, H))
small_vampire = ImageTk.PhotoImage(small_vampire)

defender_img = Image.open("pictures/defender.png").resize((pic_x, pic_y))
tk_defender_img = ImageTk.PhotoImage(defender_img)
small_defender = defender_img.resize((W, H))
small_defender = ImageTk.PhotoImage(small_defender)

healer_img = Image.open("pictures/healer.png").resize((pic_x, pic_y))
tk_healer_img = ImageTk.PhotoImage(healer_img)
small_healer = healer_img.resize((W, H))
small_healer = ImageTk.PhotoImage(small_healer)

lancer_img = Image.open("pictures/lancer.png").resize((pic_x, pic_y))
tk_lancer_img = ImageTk.PhotoImage(lancer_img)
small_lancer = lancer_img.resize((W, H))
small_lancer = ImageTk.PhotoImage(small_lancer)

icon_size = int(WIDTH//51.2)        # 25
icon_names = ["pictures/icons/heart.png", "pictures/icons/attack.png", "pictures/icons/defense.png", "pictures/icons/vampirsm.png", "pictures/icons/heal.png", "pictures/icons/price.png"]
icon_tags = []
small_icon_tags = []
for i in icon_names:
    icon_img = Image.open(i)
    icon_tags.append(ImageTk.PhotoImage(icon_img))
    small_icon = icon_img.resize((icon_size, icon_size))
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

background = Image.open("pictures/bg/build_army_bg.png").resize((WIDTH, HEIGHT))
tk_background = ImageTk.PhotoImage(background)
canvas.create_image(0, 0, image = tk_background, anchor = 'nw')

exit_button = tk.Button(root, text='EXIT', command=close, width=5)
exit_button.place(x = WIDTH - 50, y = 0)
root.bind('<Escape>', close)

army = []
money = 600
money_text = canvas.create_text(WIDTH - 100, 50, text=money, fill="black", font=('Helvetica 30 bold'))

tag_width = (WIDTH - 300)//3
tag_height = HEIGHT//3 - 50

# hp, atk, def, vamp, heal, cost
unit_stats = {"warrior": [100, 10, 2, 0, 0, 80], "knight": [120, 12, 3, 0, 0, 100], "vampire": [100, 12, 1, 0.5, 0, 130], "defender": [130, 5, 5, 0, 0, 150], "healer": [100, 1, 2, 0, 4, 100], "lancer": [90, 8, 1, 0, 0, 200]}
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

lancer = character_create(tag_width*2 - x, tag_height * 2 - y + 50, tag_width*2 + x, tag_height * 2 + y + 50, unit_stats["lancer"], tk_lancer_img)
canvas.tag_bind(lancer, "<ButtonPress-1>", Lancer)

canvas.create_line(0, tag_height * 3 - 25, WIDTH, tag_height * 3 - 25)
canvas.create_text(60, tag_height*3, text="ARMY", fill="black", font=('Helvetica 30 bold'))

weapons = {}
spacing = WIDTH//6
hspace = (HEIGHT - tag_height)//5
wx1 = tag_width * 3 - x//2
wx2 = tag_width * 3 + x//2
weapon_stats = [[5, 5, 0, 0, 0, 50], [20, -1, 2, 0, 0, 70], [-15, 7, -2, 0.1, 0, 70], [-40, 10, -5, 0.5, 0, 100], [30, 3, 0, 0, 2, 80]]
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
