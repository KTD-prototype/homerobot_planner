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

from goapy import Planner, Action_List

if __name__ == '__main__':
    import time

    # make an instance of the class:Planner with following arguments
    _world = Planner('hungry', 'has_food', 'in_kitchen', 'tired', 'in_bed')

    # set start state of the world
    _world.set_start_state(hungry=True, has_food=False,
                           in_kitchen=False, tired=True, in_bed=False)
    # set goal state to reach
    _world.set_goal_state(tired=False)

    # make an instance of the class:Action_List as an action list
    _actions = Action_List()

    # add an action 'eat' with corresponding conditions and reactions
    _actions.add_condition('eat', hungry=True, has_food=True, in_kitchen=False)
    _actions.add_reaction('eat', hungry=False)

    # add an action 'cook' with corresponding conditions and reactions
    _actions.add_condition('cook', hungry=True,
                           has_food=False, in_kitchen=True)
    _actions.add_reaction('cook', has_food=True)

    # add an action 'sleep' with correspondent conditions and reactions
    _actions.add_condition('sleep', tired=True, in_bed=True)
    _actions.add_reaction('sleep', tired=False)

    # add an action 'go_to_bed' with correspondent conditions and reactions
    _actions.add_condition('go_to_bed', in_bed=False, hungry=False)
    _actions.add_reaction('go_to_bed', in_bed=True)

    # add an action 'go_to_kitchen', with correspondent conditions and reactions
    _actions.add_condition('go_to_kitchen', in_kitchen=False)
    _actions.add_reaction('go_to_kitchen', in_kitchen=True)

    # add an action 'leave_kitchen' with correspondent conditions and reactions
    _actions.add_condition('leave_kitchen', in_kitchen=True)
    _actions.add_reaction('leave_kitchen', in_kitchen=False)

    # add and action 'order pizza' with correspondent conditions and reactions
    _actions.add_condition('order_pizza', has_food=False, hungry=True)
    _actions.add_reaction('order_pizza', has_food=True)

    # set weight
    _actions.set_weight('go_to_kitchen', 20)
    _actions.set_weight('order_pizza', 1)

    # set the all actions to the action list in the _world
    _world.set_action_list(_actions)
