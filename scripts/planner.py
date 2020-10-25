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

    # initialize the brain by the class:World
    _brain = World()

    # initialize carry_brain with the list of states
    _carry_brain = Planner('know_what_to_carry',
                           'know_place_of_object',
                           'in_front_of_object',
                           'picking_up_object'
                           'have_object',
                           'know_where_to_carry',
                           'reached_destination',
                           'delivered_object',
                           'said_to_start_carry',
                           'said_to_stop')

    # initialize carry brain with the start state
    _carry_brain.set_start_state(know_what_to_carry=False,
                                 know_place_of_obect=False,
                                 in_front_of_object=False,
                                 picking_up_object=False,
                                 have_object=False,
                                 know_where_to_carry=False,
                                 reached_destination=False,
                                 said_to_start_carry=False,
                                 said_to_stop=False,
                                 carry_complete=False)

    # set a goal
    _carry_brain.set_goal_state(carry_complete=True)

    # initialize the action list
    _carry_actions = Action_List()

    # add actions
    _carry_actions.add_condition('get_object_name',
                                 have_object=False,
                                 picking_up_object=False)
    _carry_actions.add_reaction('get_object_name',
                                know_what_to_carry=True)

    _carry_actions.add_condition('get_object_location',
                                 have_object=False,
                                 picking_up_object=False)
    _carry_actions.add_reaction('get_object_location',
                                know_place_of_object=True)

    _carry_actions.add_condition('get_destination')
    _carry_actions.add_reaction('get_destination',
                                know_where_to_carry=True)

    _carry_actions.add_condition('move_to_object_location',
                                 know_place_of_object=True,
                                 in_front_of_object=False,
                                 have_object=False,,
                                 picking_up_object=False,
                                 said_to_stop=False)
    _carry_actions.add_reaction('move_to_object_location',
                                in_front_of_object=True)

    _carry_actions.add_condition('start_pickup_object',
                                 in_front_of_object=True,
                                 have_object=False)
    _carry_actions.add_reaction('pickup_object',
                                have_object=True)

    _carry_actions.add_condition('carry',
                                 have_object=True)
    _carry_actions.add_reaction('get_object_location',
                                know_place_of_object=True)