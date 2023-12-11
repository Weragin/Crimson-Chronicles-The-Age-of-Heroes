from typing import Tuple, List


# py.checkio Warriors
class Unit:
    def __init__(self, name, cost, health, attack, **kwargs):
        self.name = name
        self.cost = cost
        self.is_alive = True
        self.health = health
        self.attack = attack
        for key, value in kwargs.items():
            setattr(self, key, value)

    def hit(self, target: "Unit") -> Tuple[int, int, int]:
        original_hp, damage_dealt, final_hp = target.on_attacked(self.attack)
        return original_hp, damage_dealt, final_hp

    def on_attacked(self, damage):
        original_hp = self.health
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.remove()

        return original_hp, damage, self.health

    def remove(self):
        pass


class Warrior(Unit):
    def __init__(self, name):
        Unit.__init__(self, name, cost=10, health=50, attack=5)


class Knight(Unit):
    def __init__(self, name):
        Unit.__init__(self, name, cost=13, health=50, attack=7)


class Lancer(Unit):
    def __init__(self, name):
        Unit.__init__(self, name, cost=30, health=50, attack=6)

    def hit(self, targets: List[Unit]):
        for target in targets:
            Unit.hit(self, target)
