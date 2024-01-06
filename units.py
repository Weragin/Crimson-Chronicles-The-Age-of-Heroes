from random import choice
from typing import Tuple, List


# py.checkio Warriors
class Unit:
    """
    The blank unit type.

    :method __init__: class constructor
    :method hit: Called whenever the unit attacks. Takes an array of targets and handles targeting and effects that influence the attacker (e.g. vampirism)
    :method on_attacked: Called whenever the unit is beeing attacked. Handles effects related to the defender, e.g. defence.
    :method remove: Called when the unit dies. Should remove the unit and handle effects related but it might be redundant later.

    TBA: properties
    :property id: Used to identify the unit.
    :property health:
    :property attack:
    :property defence:
    """
    
    def __init__(self, id, health, attack, defence=0, vampirism=0, heal_power=0):
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

    def hit(self, targets: List["Unit"], allies: List["Unit"]) -> Tuple[dict[int, int], dict[int, int]]:
        """
        Handles the event of a unit beeing called as an attacker.

        Handles the effects of an attack on the attacker and calls the on_attacked() method of another Unit, returning its return values.
        
        :param targets: Iterable[Unit, ...]: An array of Units that might be targeted
        :param allies: Iterable[Unit, ...]: An array of allies that might be healed]
        
        :returns: Tuple[dict[int, int], dict[int, int]]: The ids and resulting hp for all targets and the ids and resulting hp for all allies
        """
        # attacking
        target = choice(targets)
        enemy_id, enemy_hp, damage_dealt = target.on_attacked(self.attack)
        attacks = {enemy_id: enemy_hp}

        # vampirism
        heals = {}
        if self.vampirism > 0:
            self.on_healed(damage_dealt * self.vampirism)
            heals[self.id] = self.health

        # healing
        if self.heal_power > 0:
            for unit in allies:
                id, health = unit.on_healed(self.heal_power)
                heals[id] = health
        
        return attacks, heals

    def on_attacked(self, damage) -> Tuple[int, int, int]:
        original_hp = self.health
        damage_dealt = max(damage + self.defence, 0)
        self.health = max(self.health - damage_dealt, 0)
        damage_dealt = original_hp - self.health
        
        return self.id, self.health, damage_dealt

    def on_healed(self, heal_power) -> Tuple[int, int]:
        original_hp = self.health
        self.health = min(self.health + heal_power, self.max_health)

        return self.id, self.health
        

class Warrior(Unit):
    """
    The most basic unit
    :property cost: int: =10
    :property health: int: =50
    :property attack: int: =5
    """


class Knight(Unit):
    """
    The better version of the most basic unit. Deals more damage
    :property cost: int: =13
    :property health: int: =50
    :property attack: int: =7
    """


class Defender(Unit):
    """
    The first special unit. Whenever it takes damage, it reduces the damage taken.
    :property cost: int: =30
    :property health: int: =50
    :property attack: int: =6
    """


class Vampire(Unit):
    """
    The second special unit. Whenever it deals damage, it heals
    """


class Lancer(Unit):
    """
    A special unit that modifies targeting to attack all units but has great cost.
    :property cost: int: =30
    :property health: int: =50
    :property attack: int: =6
    """
    def __init__(self, id):
        Unit.__init__(self, id, health=50, attack=6)

    def hit(self, targets: List[Unit]):
        """
        Attacks all oposing units.
        :param targets: Iterable[Unit, ...]: An array of Units that might be targeted
        """
        for target in targets:
            target.on_attacked(self.attack)


class Healer(Unit):
    """Heals unit"""
