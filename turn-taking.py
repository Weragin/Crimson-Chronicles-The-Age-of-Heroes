from random import shuffle
from typing import Dict, List, Tuple

import battle
import units

# 1 function main():
#  - while game_not_over: call_stack = attack_order(<living_units>)
#      - while call_stack != []: 
#          - attacker = call_stack.pop()
#          - if attacker[0] == 0:
#              - health_dict = player_turn(attacker[1], <armies>, call_stack)
#          - else:
#              - health_dict = enemy_turn(attacker[1], <armies>, call_stack)
#            # do this in player_turn and enemy_turn:
#          - for i in health_dict:
#              - if health_dict[i] <= 0:
#                  - if i in call_stack:
#                      - call_stack.remove(i)
#                  - if i in my_army_objects:
#                      - my_army_objects.remove(i)
#                  - if i in enemy_army_objects:
#                      - enemy_army_objects.remove(i)
#          - do the animatiooons
def game(my_army_objects: Dict[int, units.Unit], enemy_army_objects: Dict[int, units.Unit]):
    while len(my_army_objects) > 0 and len(enemy_army_objects) > 0:
        # list_member[0] == 0 means player's turn, 
        # list_member[0] == 1 means enemy's turn:
        call_stack = [(0, id) for id in my_army_objects]\
                     + [(1, id) for id in enemy_army_objects]
        shuffle(call_stack)

        while len(call_stack) > 0:
            attacker = call_stack.pop()
            attacker_id = attacker[1]
            if attacker[0] == 0:
                # create a dict of modified health and remove dead units from call stack and army objects dictionaries
                health_dict, defender = player_turn(
                                        attacker_id=attacker_id,
                                        targets_dict=enemy_army_objects,
                                        allies_dict=my_army_objects,
                                        call_stack=call_stack
                                        )
            else:
                health_dict, defender_id = enemy_turn(
                                        unit_id=attacker_id, 
                                        targets_dict=my_army_objects, 
                                        allies_dict=enemy_army_objects, 
                                        call_stack=call_stack
                                        )

            # animations:


def player_turn(attacker_id, targets_dict, allies_dict, call_stack):
    unit = allies_dict[attacker_id]
    if type(unit) == units.Lancer:
        health_dict, defender_id = unit.hit(
            targets=[i for i in targets_dict.values()], 
            allies=[i for i in allies_dict.values()]
            )
    else: 
        pass

    return health_dict, defender_id


def enemy_turn(unit_id: int, 
               targets_dict: Dict[int, units.Unit], 
               allies_dict: Dict[int, units.Unit], 
               call_stack: List[Tuple[int, int]]):
    unit = allies_dict[unit_id]
    health_dict, defender_id = unit.hit(
        targets=[i for i in targets_dict.values()], 
        allies=[i for i in allies_dict.values()]
        )


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
