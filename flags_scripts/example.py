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
    _world.set_goal_state(tied=False)
