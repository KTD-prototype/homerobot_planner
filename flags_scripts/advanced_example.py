#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generic GOAP implementation.
# flags - https://github.com/flags
# The MIT License (MIT)
#
# Copyright (c) 2014 Luke Martin (flags)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from goapy import World, Planner, Action_List

if __name__ == '__main__':
    import time

    # initialize and instanciate the brain by the class:World
    _brain = World()

    # initialize combat_brain with the list of states
    _combat_brain = Planner('has_ammo',
                            'has_weapon',
                            'weapon_armed',
                            'weapon_loaded',
                            'in_engagement',
                            'in_cover',
                            'in_enemy_los',
                            'is_near')

    # initialize combat_brain with the start state
    _combat_brain.set_start_state(in_engagement=True,
                                  is_near=False,
                                  in_cover=False,
                                  in_enemy_los=True,
                                  has_ammo=False,
                                  has_weapon=True,
                                  weapon_armed=False,
                                  weapon_loaded=False)

    # set a goal
    _combat_brain.set_goal_state(in_engagement=False)

    # initialize and instanciate the action list
    _combat_actions = Action_List()

    # add an action:track
    _combat_actions.add_condition('track',
                                  is_near=False,
                                  weapon_armed=True)
    _combat_actions.add_reaction('track', is_near=True)

    # add an action:unpack_ammo
    _combat_actions.add_condition('unpack_ammo',
                                  has_ammo=False)
    _combat_actions.add_reaction('unpack_ammo',
                                 has_ammo=True)

    # add an action:search_for_ammo
    _combat_actions.add_condition('search_for_ammo',
                                  has_ammo=False)
    _combat_actions.add_reaction('search_for_ammo',
                                 has_ammo=True)

    # add an action:reload
    _combat_actions.add_condition('reload',
                                  has_ammo=True,
                                  weapon_loaded=False,
                                  in_cover=True)
    _combat_actions.add_reaction('reload', weapon_loaded=True)

    # add an action:arm
    _combat_actions.add_condition('arm',
                                  weapon_loaded=True,
                                  weapon_armed=False)
    _combat_actions.add_reaction('arm', weapon_armed=True)

    # add an action:shoot
    _combat_actions.add_condition('shoot',
                                  weapon_loaded=True,
                                  weapon_armed=True,
                                  is_near=True)
    _combat_actions.add_reaction('shoot', in_engagement=False)

    # add an action:get_cover
    _combat_actions.add_condition('get_cover', in_cover=False)
    _combat_actions.add_reaction('get_cover', in_cover=True)

    # set weights of each actions
    _combat_actions.set_weight('unpack_ammo', 3)
    _combat_actions.set_weight('search_for_ammo', 4)
    _combat_actions.set_weight('track', 20)

    # register the actions defined above to combat_brain
    _combat_brain.set_action_list(_combat_actions)

    # initialize food_brain with possible states
    _food_brain = Planner('is_hungry',
                          'has_food')
    # initialize actions by list
    _food_actions = Action_List()

    # register the actions to food_brain(still not defined?)
    _food_brain.set_action_list(_food_actions)

    # set start and goal state of the food_brain
    _food_brain.set_start_state(has_food=False,
                                is_hungry=True)
    _food_brain.set_goal_state(is_hungry=False)

    # add an action:find_food
    _food_actions.add_condition('find_food', has_food=False)
    _food_actions.add_reaction('find_food', has_food=True)

    # add an action:eat_food
    _food_actions.add_condition('eat_food', has_food=True)
    _food_actions.add_reaction('eat_food', is_hungry=False)

    # set weights of each actions
    _food_actions.set_weight('find_food', 20)
    _food_actions.set_weight('eat_food', 10)

    # initialize heal brain with possible states
    _heal_brain = Planner('is_hurt',
                          'has_bandage')
    # initialize actions by list
    _heal_actions = Action_List()

    # register the actions to heal brain(still not defined?)
    _heal_brain.set_action_list(_heal_actions)

    # set start and goal state of the heal_brain
    _heal_brain.set_start_state(has_bandage=False,
                                is_hurt=True)
    _heal_brain.set_goal_state(is_hurt=False)

    # add an action:
    _heal_actions.add_condition('find_bandage', has_bandage=False)
    _heal_actions.add_reaction('find_bandage', has_bandage=True)
    _heal_actions.add_condition('apply_bandage', has_bandage=True)
    _heal_actions.add_reaction('apply_bandage', is_hurt=False)

    # set weights of each actions
    _heal_actions.set_weight('find_bandage', 15)

    # register each planner to the _brain : instance of the class:World
    _brain.add_planner(_combat_brain)
    _brain.add_planner(_food_brain)
    _brain.add_planner(_heal_brain)

    # calculate the chain of actions with lowest cost
