import tkinter as tk
import sys
from PIL import Image, ImageTk

root = tk.Tk()
root.attributes('-fullscreen', True)


def close(e = 0):
    root.withdraw()
    sys.exit()


def Warrior(e):
    global money
    if money > 100:
        money -= 100
        army.append(["warrior", []])
        canvas.itemconfig(money_text, text = money)
        army_add(warrior, small_warrior)



def Knight(e):
    global money
    if money > 120:
        money -= 120
        army.append(["knight", []])
        canvas.itemconfig(money_text, text = money)
        army_add(knight)


def Vampire(e):
    global money
    if money > 140:
        money -= 140
        army.append(["vampire", []])
        canvas.itemconfig(money_text, text = money)
        army_add(vampire)


def Defender(e):
    global money
    if money > 130:
        money -= 130
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(defender)


def Healer(e):
    global money
    if money > 135:
        money -= 135
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(healer)


def Lancer(e):
    global money
    if money > 120:
        money -= 120
        army.append(["defender", []])
        canvas.itemconfig(money_text, text = money)
        army_add(lancer)


def army_add(unit, img = None):
    global resized_tk
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
    # print(overlap)
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
    global selected_unit, temp
    try:
        x1, y1, x2, y2 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        army[selected_unit][1].append(overlap[0])
        nofweapons = len(army[selected_unit][1])
        color = canvas.itemcget(overlap[0], "fill")
        move = 5 * (nofweapons - 1)
        canvas.create_rectangle(x1 + move, y1 + 40, x2 - 10 + move, y2 + 30, fill=color)
    except:
        x1, y1 = canvas.coords(temp[selected_unit])
        overlap = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
        army[selected_unit][1].append(overlap[0])
        nofweapons = len(army[selected_unit][1])
        color = canvas.itemcget(overlap[0], 'fill')
        move = 5 * (nofweapons - 1)
        canvas.create_rectangle(x1 + move, y1 + H + 10, x1 + W - 10 + move, y1 + H + 40, fill=color)


def character_create(x1, y1, x2, y2, stats: list, img = None):
    num = 200//6
    if img == None:
        character = canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    else:
        character = canvas.create_image(x1, y1, image = img, anchor = tk.NW, tags="images")
        print(img, type(img))
    for i in range(len(stats)):
        canvas.create_rectangle(x2, y1 + num * i, x2 + num, y1 + num * (i + 1), fill="red")
        canvas.create_text(x2 + 2 * num, y1 + num * i + num//2, text=stats[i], font=('Helvetica 20 bold'))
    return character


def canvas_size(e):
    global WIDTH, HEIGHT
    WIDTH = e.width
    HEIGHT = e.height


W = 30
H = 60
warrior_img = Image.open("pictures/warrior.png")
small_warrior = warrior_img.resize((W, H))
small_warrior = ImageTk.PhotoImage(small_warrior)
tk_warrior_img = ImageTk.PhotoImage(warrior_img)

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = 1250
HEIGHT = 695
canvas.bind('<Configure>', canvas_size)

exit_button = tk.Button(root, text='EXIT', command=close)
exit_button.place(x = WIDTH, y = 0)
root.bind('<Escape>', close)

army = []
money = 600
money_text = canvas.create_text(WIDTH - 100, 50, text=money, fill="black", font=('Helvetica 30 bold'))

tag_width = (WIDTH - 300)//3
tag_height = HEIGHT//3 - 50

x = 50
y = 100
warrior = character_create(tag_width - x, tag_height - y, tag_width + x, tag_height + y, [100, 5, 2, 0, 0, 90], tk_warrior_img)
canvas.tag_bind(warrior, "<ButtonPress-1>", Warrior)

knight = character_create(tag_width*2 - x, tag_height - y, tag_width*2 + x, tag_height + y, [120, 7, 2, 0, 0, 100], None)
canvas.tag_bind(knight, "<ButtonPress-1>", Knight)

vampire = character_create(tag_width*3 - x, tag_height - y, tag_width*3 + x, tag_height + y, [140, 5, 2, 5, 0, 80], None)
canvas.tag_bind(vampire, "<ButtonPress-1>", Vampire)

defender = character_create(tag_width - x, tag_height * 2 - y + 50, tag_width + x, tag_height * 2 + y + 50, [130, 5, 5, 0, 0, 150], None)
canvas.tag_bind(defender, "<ButtonPress-1>", Defender)

healer = character_create(tag_width*2 - x, tag_height * 2 - y + 50, tag_width*2 + x, tag_height * 2 + y + 50, [135, 0, 2, 0, 5, 80], None)
canvas.tag_bind(healer, "<ButtonPress-1>", Healer)

lancer = character_create(tag_width*3 - x, tag_height * 2 - y + 50, tag_width*3 + x, tag_height * 2 + y + 50, [120, 7, 2, 0, 0, 90], None)
canvas.tag_bind(lancer, "<ButtonPress-1>", Lancer)

canvas.create_line(0, tag_height * 3, WIDTH, tag_height * 3)
canvas.create_text(60, tag_height*3 + 30, text="ARMY", fill="black", font=("Helvetica 30 bold"))

weapons = []
weapon1 = canvas.create_rectangle(WIDTH//2 + 30, tag_height*3 + 50, WIDTH//2 + 50, tag_height*3 + 70, fill="orange", tags="weapons")
weapon2 = canvas.create_rectangle(WIDTH//2 + 80, tag_height*3 + 50, WIDTH//2 + 100, tag_height*3 + 70, fill="brown", tags="weapons")
weapon3 = canvas.create_rectangle(WIDTH//2 + 130, tag_height*3 + 50, WIDTH//2 + 150, tag_height*3 + 70, fill="magenta", tags="weapons")
canvas.tag_bind("weapons", "<ButtonPress-1>", add_weapon)

temp = []
selected_unit = ""
canvas.tag_bind("army", "<ButtonPress-1>", find_unit)

root.mainloop()