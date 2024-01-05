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
    enemy1 = "enemy_army" if x > WIDTH//2 else "my_army"
    if len(my_army) > 3:
        spacing1 = (HEIGHT//150 - 1) * 150//3
        spacing2 = (HEIGHT//150 - 1) * 150//(len(my_army) - 3)
        enemy = size[0] + 25 if x > WIDTH//2 else -size[0] - 25
        for i in range(3):
            army_units.append(canvas.create_image(x, HEIGHT - spacing1 - size[-1] * (i + 0.5) - i * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = (enemy1, str(army_units[-1]) + 'e')
            canvas.itemconfig(army_units[-1], tags = temp_tag)
            hp_create(army_units[-1], unit_stats[my_army[i][0]][0], temp_tag)
        for i in range(3, len(my_army)):
            army_units.append(canvas.create_image(x + enemy * 2, HEIGHT - spacing2 - size[-1] * (i + 0.5 - 3) - (i-3) * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = (enemy1, str(army_units[-1]) + 'e')
            canvas.itemconfig(army_units[-1], tags = temp_tag)
            hp_create(army_units[-1], unit_stats[my_army[i][0]][0], temp_tag)
    else:
        spacing = (HEIGHT//150 - 1) * 150 // len(my_army)
        for i in range(len(my_army)):
            army_units.append(canvas.create_image(x, HEIGHT - spacing - size[-1] * (i+0.5) - i * size[-1]//3, image = unit_imgs[my_army[i][0]], anchor = 'nw'))
            temp_tag = (enemy1, str(army_units[-1]) + 'e')
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
    
    def animate(self):
        is_lancer = canvas.itemcget(self.attacker, 'image')
        if is_lancer != tk_lancer_img:
            self.move_to()
        else:
            self.lancer_animate()

    def move_to(self):
        tag = canvas.itemcget(self.attacker, 'tags').split(' ')
        print(tag)
        tag = tag[1]
        canvas.move(tag, self.dx/20, self.dy/20)
        self.steps -= 1
        if self.steps > 0:
            canvas.after(50, self.move_to)
        else:
            self.steps = 20
            self.attakcing()
            self.turn_around()
            print('returning')
            self.move_from()
    
    def attakcing(self):
        tags = canvas.itemcget(self.defender, 'tags').split(' ')
        items = canvas.find_withtag(tags[1])
        dmg = random.randint(5, 10)
        hp = canvas.itemcget(items[-1], 'text')
        canvas.itemconfig(items[-1], text = int(hp) - dmg)

    def turn_around(self):
        id = str(canvas.itemcget(self.attacker, 'image'))
        print(id)
        canvas.itemconfig(self.attacker, image = opposite_img[id])
        print(canvas.itemcget(self.attacker, 'image'))

    def turn_back(self):
        id = canvas.itemcget(self.attacker, 'image')
        img_id = [i for i in opposite_img if str(opposite_img[i]) == id]
        canvas.itemconfig(self.attacker, image = img_id)

    def move_from(self):
        tag = canvas.itemcget(self.attacker, 'tags').split(' ')
        tag = tag[1]
        canvas.move(tag, self.dx/-20, self.dy/-20)
        self.steps -= 1
        if self.steps > 0:
            canvas.after(50, self.move_from)
        else:
            self.turn_back()

    def lancer_animate(self):
        # zmen obrazok na motorku
        # dojdi dole
        # zmen obrazok na utok motorku
        # ide hore
        # zmen obrazok na vracia sa s motorkou
        # vrati sa na miesto
        # zmen obrazok na idle lancer
        # WIDTH//4 * 3 - size[0] * 2
        pass


def attacking_unit(e):
    global my_turn, my_unit
    print("attacking unit selected")
    my_unit = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)[1]


def defending_unit(e):
    global enemy_unit, my_turn
    print("defending unit selected")
    enemy_unit = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)[1]


def attack(e):
    global my_turn, my_unit, enemy_unit
    if my_turn:
        print("commencing attack")
        my_turn = False
        atk = Attack(my_unit, enemy_unit)
        atk.animate()
        canvas.after(3000, enemy_attack)



def enemy_attack():
    global my_turn, running_animation
    attacker = random.choice(enemy_army_tags)
    defender = random.choice(my_army_tags)
    atk = Attack(attacker, defender)
    atk.animate()
    my_turn = True


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
healer_img = Image.open("pictures/healer.png").resize(size)
tk_healer_img = ImageTk.PhotoImage(healer_img)

tk_lancer_img = None

unit_imgs = {"warrior": tk_warrior_img, "knight": tk_knight_img, "vampire": tk_vampire_img, "defender": tk_defender_img, 'healer': tk_healer_img, "lancer": tk_lancer_img}
opposite_healer = healer_img.transpose(Image.FLIP_LEFT_RIGHT)
opposite_healer = ImageTk.PhotoImage(opposite_healer)
opposite_lancer = None
opposite_img = {str(tk_warrior_img): tk_warrior_img, str(tk_knight_img): tk_knight_img, str(tk_vampire_img): tk_vampire_img, str(tk_defender_img): tk_defender_img, str(tk_healer_img): opposite_healer, str(tk_lancer_img): opposite_lancer}

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
WIDTH = int(sys.argv[3])
HEIGHT = int(sys.argv[4])

background = Image.open("pictures/bg/battle_background.png").resize((WIDTH, HEIGHT))
tk_background = ImageTk.PhotoImage(background)
canvas.create_image(0, 0, image = tk_background, anchor = 'nw')

exit_button = tk.Button(root, text='EXIT', command=close)
exit_button.place(x = WIDTH, y = 0, anchor='ne')
root.bind('<Escape>', close)

army = sys.argv[1]
army = json.loads(army)
# print(army)


unit_stats = sys.argv[2]
unit_stats = json.loads(unit_stats)
print(unit_stats)
# stats- hp, atk, def, vamp, heal, cost

my_army_tags = create_army(army, WIDTH//4)
enemy_army = [['vampire', [[-15, 5, -2, 0.1, 0, 70]]], ['vampire', [[-15, 5, -2, 0.1, 0, 70]]], ['vampire', []], ['knight', []]]
enemy_army_tags = create_army(enemy_army, WIDTH//4 * 3 - size[0])

my_turn = True
my_unit = None
enemy_unit = None

# for i in range(5):
#     a = random.choice(my_army_tags)
#     b = random.choice(enemy_army_tags)
#     print(a, b)
#     if random.choice([True, False]):
#         ani(a, b)
#     else:
#         ani(b, a)
#     # enemy 2 utoci na my 0 tak sa zasekne
# print("____________________________________________________________________________")
running_animation = False
canvas.tag_bind("my_army", "<ButtonPress-1>", attacking_unit)
canvas.tag_bind("enemy_army", "<ButtonPress-1>", defending_unit)
root.bind("<Return>", attack)

root.mainloop()