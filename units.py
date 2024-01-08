from random import choice
from typing import List, Tuple


# py.checkio Warriors
class Unit:
    """
    The blank unit type.

    :method __init__: class constructor
    :method hit: Called whenever the unit attacks. Takes an array of targets and handles targeting and effects that influence the attacker (e.g. vampirism)
    :method on_attacked: Called whenever the unit is beeing attacked. Handles effects related to the defender, e.g. defence.

    TBA: properties
    :property id: Used to identify the unit.
    :property health:
    :property attack:
    :property defence:
    """
    
    def __init__(self, id: int, health: int, attack: int, defence=0, vampirism=0, heal_power=0):
        self.id = id
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defence = defence
        self.vampirism = vampirism
        self.heal_power = heal_power

    def equip_weapon(self, stats: list[int]):
        self.max_health += stats[0]
        self.health += stats[0]
        self.attack += stats[1]
        self.defence += stats[2]
        self.vampirism += stats[3]
        self.heal_power += stats[4]

    def check_stats(self):
        self.max_health = max(1, self.max_health)
        self.health = self.max_health
        self.attack = max(0, self.attack)
        self.heal_power = max(0, self.heal_power)

    def hit(self, targets: List["Unit"], allies: List["Unit"]) -> Tuple[dict[int, int], int]:
        """
        Handles the event of a unit beeing called as an attacker.

        Handles the effects of an attack on the attacker and calls the on_attacked() method of another Unit, returning its return values.
        
        :param targets: List[Unit]: An array of Units that might be targeted
        :param allies: List[Unit]: An array of allies that might be healed]
        
        :returns: Tuple[dict[int, int], int]: The ids and resulting hp for all targets and allies, and the id of the defender. Used for animations.
        """
        # attacking
        target = choice(targets)
        enemy_id, enemy_hp, damage_dealt = target.on_attacked(self.attack)
        health_points = {enemy_id: enemy_hp}

        # vampirism
        if self.vampirism > 0:
            self.on_healed(int(damage_dealt * self.vampirism))
            health_points[self.id] = self.health

        # healing
        if self.heal_power > 0:
            for unit in allies:
                id, health = unit.on_healed(self.heal_power)
                health_points[id] = health
        
        return health_points, enemy_id

    def on_attacked(self, damage) -> Tuple[int, int, int]:
        original_hp = self.health
        damage_dealt = max(damage - self.defence, 1)
        self.health = max(self.health - damage_dealt, 0)
        damage_dealt = original_hp - self.health
        
        return self.id, self.health, damage_dealt

    def on_healed(self, heal_power) -> Tuple[int, int]:
        original_hp = self.health
        self.health = min(self.health + heal_power, self.max_health)

        return self.id, self.health
        

class Warrior(Unit):
    """The most basic unit."""


class Knight(Unit):
    """The better version of the Warrior."""


class Defender(Unit):
    """The first special unit. Whenever it takes damage, it reduces the damage taken."""

class Vampire(Unit):
    """The second special unit. Whenever it deals damage, it heals."""


class Lancer(Unit):
    """A special unit that attacks all opposing units"""
    def hit(self, targets: List[Unit], allies: List[Unit]) -> Tuple[dict[int, int], int]:
        """
        Attacks all oposing units.
        :param targets: List[Unit, ...]: An array of Units to be attacked.
        :param allies: List[Unit, ...]: An array of allies that might be healed.
        :returns: Tuple[dict[int, int], int]: The ids and resulting hp for all targets and allies, and the id of an arbitrary defender. Used for animations.
        """
        # attacking
        total_damage = 0
        health_points = {}
        for target in targets:
            enemy_id, enemy_hp, damage_dealt = target.on_attacked(self.attack)
            health_points[enemy_id] = enemy_hp
            total_damage += damage_dealt

        # vampirism
        if self.vampirism > 0:
            self.on_healed(int(total_damage * self.vampirism))
            health_points[self.id] = self.health

        # healing
        if self.heal_power > 0:
            for unit in allies:
                id, health = unit.on_healed(self.heal_power)
                health_points[id] = health

        return health_points, enemy_id


class Healer(Unit):
    """A special unit that heals all allies."""
