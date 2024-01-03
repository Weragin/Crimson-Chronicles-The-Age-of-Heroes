import sys
import json
import tkinter as tk
from PIL import Image, ImageTk
import random


def close(e = 0):
    root.withdraw()
    sys.exit()


def create_army(my_army, x):
    global HEIGHT, unit_imgs
    army_units = []
    if len(my_army) > 3:
        spacing1 = (HEIGHT//150 - 1) * 150//3
        spacing2 = (HEIGHT//150 - 1) * 150//(len(my_army) - 3)
        enemy = size[0] + 25 if x > WIDTH//2 else -size[0] - 25
        for i in range(3):
            army_units.append(canvas.create_image(x, HEIGHT - spacing1 - size[-1] * (i + 0.5) - i * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = str(army_units[-1]) + 'e'
            canvas.itemconfig(army_units[-1], tags = temp_tag)
            hp_create(army_units[-1], unit_stats[my_army[i][0]][0], temp_tag)
        for i in range(3, len(my_army)):
            army_units.append(canvas.create_image(x + enemy * 2, HEIGHT - spacing2 - size[-1] * (i + 0.5 - 3) - (i-3) * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = str(army_units[-1]) + 'e'
            canvas.itemconfig(army_units[-1], tags = temp_tag)
            hp_create(army_units[-1], unit_stats[my_army[i][0]][0], temp_tag)
    else:
        spacing = (HEIGHT//150 - 1) * 150 // len(my_army)
        for i in range(len(my_army)):
            army_units.append(canvas.create_image(x, HEIGHT - spacing - size[-1] * (i+0.5) - i * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = str(army_units[-1]) + 'e'
            canvas.itemconfig(army_units[-1], tags = temp_tag)
            hp_create(army_units[-1], unit_stats[my_army[i][0]][0], temp_tag)
    return army_units


def hp_create(unit_id, hp, tag):
    unit_coords = canvas.coords(unit_id)
    hp_coords = (unit_coords[0], unit_coords[1] - 20)
    canvas.create_image(hp_coords[0], hp_coords[1], image = tk_hp_icon, anchor = 'nw', tags = tag)
    canvas.create_text(hp_coords[0] + 20 + 10, hp_coords[1] - 5, text=hp, anchor='nw', font=("Helvetica 16 bold"), tags= tag)


class Attack:
    def __init__(self, attacker, defender):
        global size
        self.attacker = attacker
        self.defender = defender
        self.atk_coords = canvas.coords(attacker)
        self.enemy = -1 if self.atk_coords[0] > WIDTH//2 else 1
        def_coords = canvas.coords(defender)
        self.end_coords = (def_coords[0] + (- size[0] - 20) * self.enemy, def_coords[1])
        self.dx = self.end_coords[0] - self.atk_coords[0]
        self.dy = self.end_coords[1] - self.atk_coords[1]
        self.steps = 20
        self.move_to()

    def move_to(self):
        tag = canvas.itemcget(self.attacker, 'tags')
        canvas.move(tag, self.dx/20, self.dy/20)
        self.steps -= 1
        if self.steps > 0:
            canvas.after(50, self.move_to)
        else:
            self.steps = 20
            print('returning')
            self.move_from()
    
    def attakcing(self):
        pass

    def move_from(self):
        tag = canvas.itemcget(self.attacker, 'tags')
        canvas.move(tag, self.dx/-20, self.dy/-20)
        self.steps -= 1
        if self.steps > 0:
            canvas.after(50, self.move_from)


root = tk.Tk()
root.attributes('-fullscreen', True)

hp_icon = Image.open("pictures/icons/heart.png").resize((20, 20))
tk_hp_icon = ImageTk.PhotoImage(hp_icon)
size = (80, 160)
warrior_img = Image.open("pictures/warrior.png").resize(size)
tk_warrior_img = ImageTk.PhotoImage(warrior_img)
knight_img = Image.open("pictures/knight.png").resize(size)
tk_knight_img = ImageTk.PhotoImage(knight_img)
vampire_img = Image.open("pictures/vampire.png").resize(size)
tk_vampire_img = ImageTk.PhotoImage(vampire_img)
defender_img = Image.open("pictures/defender.png").resize(size)
tk_defender_img = ImageTk.PhotoImage(defender_img)

unit_imgs = {"warrior": tk_warrior_img, "knight": tk_knight_img, "vampire": tk_vampire_img, "defender": tk_defender_img}

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = int(sys.argv[3])
HEIGHT = int(sys.argv[4])

exit_button = tk.Button(root, text='EXIT', command=close)
exit_button.place(x = WIDTH, y = 0)
root.bind('<Escape>', close)

army = sys.argv[1]
army = json.loads(army)
# print(army)

unit_stats = sys.argv[2]
unit_stats = json.loads(unit_stats)
# print(unit_stats)
# stats- hp, atk, def, vamp, heal, cost

my_army_tags = create_army(army, WIDTH//4)
enemy_army = [['vampire', [[-15, 5, -2, 0.1, 0, 70]]], ['vampire', [[-15, 5, -2, 0.1, 0, 70]]], ['vampire', []], ['knight', []]]
enemy_army_tags = create_army(enemy_army, WIDTH//4 * 3)

a = random.choice(my_army_tags)
b = random.choice(enemy_army_tags)
print(a, b)
if random.choice([True, False]):
    atk = Attack(a, b)
else:
    atk = Attack(b, a)
# atk = Attack(my_army_tags[0], enemy_army_tags[0])     # problem, obcas sa zasekne, nevrati sa kam ma
print("____________________________________________________________________________")

root.mainloop()