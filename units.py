from typing import Tuple, List, Iterable


# py.checkio Warriors
class Unit:
    """
    The blank unit type.

    :method __init__: class constructor
    :method hit: Called whenever the unit attacks. Takes an array of targets and handles targeting and effects that influence the attacker (e.g. vampirism)
    :method on_attacked: Called whenever the unit is beeing attacked. Handles effects related to the defender, e.g. defence.
    :method remove: Called when the unit dies. Should remove the unit and handle effects related but it might be redundant later.
    
    :property name: The name of the soldier
    :property cost: Self-explanatory
    :property health: Self-explanatory
    :property attack: Self-explanatory
    :property is_alive: True as long as health > 0
    """
    
    def __init__(self, name, cost, health, attack, **kwargs):
        self.name = name
        self.cost = cost
        self.health = health
        self.attack = attack
        self.is_alive = True
        for key, value in kwargs.items():
            setattr(self, key, value)

    def hit(self, targets: Iterable["Unit", ...]) -> Tuple[int, int, int]:
        """
        Handles the event of a unit beeing called as an attacker.

        Handles the effects of an attack on the attacker and calls the on_attacked() method of another Unit, returning its return values.
        
        :param targets: Iterable[Unit, ...]: An array of Units that might be targeted
        
        :returns: Tuple[int, int, int]: The health of the attacked unit before and after attack and the damage dealt.
        """
        original_hp, damage_dealt, final_hp = targets[0].on_attacked(self.attack)
        return original_hp, damage_dealt, final_hp

    def on_attacked(self, damage):
        original_hp = self.health
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.remove()

        return original_hp, damage, self.health

    def remove(self):
        """ 
        TODO: add functionality or remove
        Handles the event of a unit dying.
        """
        pass


class Warrior(Unit):
    """
    The most basic unit
    :property cost: int: =10
    :property health: int: =50
    :property attack: int: =5
    """
    def __init__(self, name):
        Unit.__init__(self, name, cost=10, health=50, attack=5)


class Knight(Unit):
    """
    The better version of the most basic unit. Deals more damage
    :property cost: int: =13
    :property health: int: =50
    :property attack: int: =7
    """
    def __init__(self, name):
        Unit.__init__(self, name, cost=13, health=50, attack=7)


class Defender(Unit):
    """
    The first special unit. Whenever it takes damage, it reduces the damage taken.
    :property cost: int: =30
    :property health: int: =50
    :property attack: int: =6
    """
    def __init__(self, name):
        Unit.__init__(self, name, cost=12, health=60, attack=3, defence=2)

    def on_attacked(self, damage):
        Unit.on_attacked(self, damage - self.defence)


class Lancer(Unit):
    """
    A special unit that modifies targeting to attack all units but has great cost.
    :property cost: int: =30
    :property health: int: =50
    :property attack: int: =6
    """
    def __init__(self, name):
        Unit.__init__(self, name, cost=30, health=50, attack=6)

    def hit(self, targets: List[Unit]):
        """
        
        """
        for target in targets:
            Unit.hit(self, target)
