from random import shuffle
from typing import Dict, List, Tuple

import battle
import units

"""gameloop functions"""
# 1 function main():
#  - while game_not_over: call_stack = attack_order(<living_units>)
#      - while call_stack != []: 
#          - attacker = call_stack.pop()
#          - if attacker[0] == 0:
#              - health_dict = player_turn(attacker[1], <armies>, call_stack)
#          - else:
#              - health_dict = enemy_turn(attacker[1], <armies>, call_stack)
#          - do the animatiooons
def game(call_stack: List[Tuple[bool, int]], 
         my_army_objects: Dict[int, units.Unit], 
         enemy_army_objects: Dict[int, units.Unit]
        ):
    if len(my_army_objects) == 0:
        print("YOU HAVE LOST!!!")
        return "YOU HAVE LOST!!!"
    if len(enemy_army_objects) == 0:
        print("YOU HAVE WON!!!")
        return "YOU HAVE WON!!!"

    if call_stack == []:
        # list_member[0] == True means player's turn, 
        # list_member[0] == False means enemy's turn:
        call_stack = [(id in my_army_objects.keys(), id) 
                      for id in 
                      list(my_army_objects.keys()) 
                      + list(enemy_army_objects.keys())]
        random.shuffle(call_stack)

    attacker = call_stack.pop()
    attacker_id = attacker[1]

    if attacker[0]:
        # create a dict of modified health and remove dead units from call stack and army objects dictionaries
        health_dict, defender = player_turn(
            attacker_id=attacker_id,
            targets_dict=enemy_army_objects,
            allies_dict=my_army_objects,
            call_stack=call_stack
            )
    else:
        health_dict, defender_id = enemy_turn(
            attacker_id=attacker_id, 
            targets_dict=my_army_objects, 
            allies_dict=enemy_army_objects, 
            call_stack=call_stack
            )

    # animations:


def player_turn(attacker_id: int, 
                targets_dict: Dict[int, units.Unit], 
                allies_dict: Dict[int, units.Unit], 
                call_stack: List[Tuple[bool, int]]
                ):
    unit = allies_dict[attacker_id]
    # attack part:
    if type(unit) == units.Lancer:
        health_dict, defender_id = unit.hit(
            targets=[i for i in targets_dict.values()], 
            allies=[i for i in allies_dict.values()]
            )
    else: 
        global enemy_unit
        canvas.tag_bind("enemy_army", "<ButtonPress-1>", defending_unit)
        root.wait_variable("Jozo")
        print(f"the defending unit (from p_t): {enemy_unit}, unbound defending_unit")
        canvas.tag_unbind("enemy_army", "<ButtonPress-1>")
    # do this in player_turn and enemy_turn:
    #          - for i in health_dict:
    #              - if health_dict[i] <= 0:
    #                  - if i in call_stack:
    #                      - call_stack.remove(i)
    #                  - if i in my_army_objects:
    #                      - my_army_objects.remove(i)
    #                  - if i in enemy_army_objects:
    #                      - enemy_army_objects.remove(i)

    return health_dict, defender_id


def enemy_turn(attacker_id: int, 
               targets_dict: Dict[int, units.Unit], 
               allies_dict: Dict[int, units.Unit], 
               call_stack: List[Tuple[bool, int]]
              ):
    unit = allies_dict[attacker_id]
    health_dict, defender_id = unit.hit(
        targets=[i for i in targets_dict.values()], 
        allies=[i for i in allies_dict.values()]
        )
    for i in health_dict:
        if health_dict[i] == 0:
            pass

    return health_dict, defender_id


# 3 player_turn(): 
#  - if the unit is lancer:
#      - call self.hit() with targets = [i for i in enemy_army_objects.values()]
#    else:
#      - bind defending_unit to canvas to the tag "enemy_army"
#      - call the attacker's self.hit() with 
#        targets = [enemy_army_object[defending_unit]]
#  - return health_dict

# 4 enemy_turn(): 
#  - call self.hit() with targets = [i for i in my_army_objects.values()]
#  - return health_dict
"""end of gameloop functions"""