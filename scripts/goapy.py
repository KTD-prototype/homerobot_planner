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


class World:
    def __init__(self):
        self.planners = []
        self.plans = []

    # function to append a certain planner to the ARRAY:PLANNERS
    def add_planner(self, planner):
        self.planners.append(planner)
        # print(self.planners[0].start_state)

    # function to culculate an actual plans(chained sequence of actions) which are contained to the ARREY:PLANNERS
    def calculate(self):
        self.plans = []
        # print(self.planners)
        for planner in self.planners:
            # print(planner.start_state)

            # chain the action plans belongs to each individual planners.
            self.plans.append(planner.calculate())


            # PLANNERS : whole lists of available actions related to obtain goals (e.g. : actions for fighting, actions for curing, actions for eating)
            # PLANNER  : a single set of actions listed in PLANNERS
            # PLANS    : whole sets of chained actions for each PLANNER, calculated by planner.calculate()
            #            i.e.: PLANS contains whole chained actions to obtain goals listed in PLANNERS, but still they're ordered
            #                  regardless of which order should actions that have been chained be executed.
            #                  This would be calculated later at function : get_plan()
            
            print(self.plans) # in self.plans, chained actions for each planners are contained
            # print(self.plans[0][0]['g'])
            # print(planner.calculate())

    # when you have multiple PLANNERS, then you'll now have multiple PLANS(sets of chained actions), calculated by function : calculate()
    # Now, this function will order those plans from lighter, to heavier in terms of their costs
    def get_plan(self, debug=False):
        _plans = {}
        for plan in self.plans:
            # keep in mind that 'g' doesn't mean each cost of single action but
            # it seems to be means the accumulated cost from start node to current node in A* algorithm
            # TODO grasp accurate meanings of the value 'g'
            _plan_cost = sum([action['g'] for action in plan]) # sum up all 'g's in a plan
            print(_plan_cost)
            if _plan_cost in _plans:
                _plans[_plan_cost].append(plan)
            else:
                _plans[_plan_cost] = [plan]

        # now you can get an ordered list of summed 'g' values for each plan, from smaller to larger 
        _sorted_plans = sorted(_plans.keys())
        # print(_sorted_plans)

        if debug:
            _i = 1

            for plan_score in _sorted_plans:
                for plan in _plans[plan_score]:
                    print(_i)

                    for action in plan:
                        print(" %s" % action['name'])

                    _i += 1
                    print('\nTotal cost: %s\n' % plan_score)

        return [_plans[p][0] for p in _sorted_plans]


class Planner:
    # initialize an instance of the Planner
    def __init__(self, *keys):
        # get the possible states (e.g. has_food) as an arguments:*keys

        self.start_state = None
        self.goal_state = None

        # initialize all values as -1, correspondent to the keys
        self.values = {k: -1 for k in keys}
        self.action_list = None

        # print("keys : " + str(keys))
        # print("values : " + str(self.values))
        # print(self.start_state, self.goal_state, self.action_list)

    def state(self, **kwargs):
        _new_state = self.values.copy()
        _new_state.update(kwargs)
        return _new_state

    # set a start state with check exceptions
    def set_start_state(self, **kwargs):
        _invalid_states = set(kwargs.keys()) - set(self.values.keys())

        # print(set(kwargs.keys()))      # a list of start state which has been set as a start_state
        # print(set(self.values.keys())) # a list of possible states of this planner
        # print(_invalid_states)
        # if there're mismatches between possible states of this planner and start_state
        # all of the items in start_state should be included in the list of possible states of the planner
        if _invalid_states:
            raise Exception('Invalid states for world start state: %s' %
                            ', '.join(list(_invalid_states)))
        self.start_state = self.state(**kwargs)
        # print(self.start_state)

    # set a goal state with check exceptions
    def set_goal_state(self, **kwargs):
        _invalid_states = set(kwargs.keys()) - set(self.values.keys())

        # print(set(kwargs.keys()))      # a list of start state which has been set as a goal_state
        # print(set(self.values.keys())) # a list of possible states of this planner
        # print(_invalid_states)
        # if there're mismatches between possible states of this planner and start_state
        # all of the items in goal_state should be included in the list of possible states of the planner
        if _invalid_states:
            raise Exception('Invalid states for world goal state: %s' %
                            ', '.join(list(_invalid_states)))
        self.goal_state = self.state(**kwargs)
        # print(self.goal_state)

    # set an action list
    def set_action_list(self, action_list):
        self.action_list = action_list
        # print('all conditions : ')
        # print(self.action_list.conditions)
        # print('')
        # print('all reactions : ')
        # print(self.action_list.reactions)
        # print('')
        # print(self.action_list.reactions['go_to_kitchen'])

    # calculate the length-cost of chained action plans by A* algorithm
    def calculate(self):
        # latter 3 arguments are list of conditions, reactions, and weights
        # TODO why not set them directly? like : self.action_list.reactions ?
        value_return = astar(self.start_state,
                             self.goal_state,
                             {c: self.action_list.conditions[c].copy(
                             ) for c in self.action_list.conditions},
                             {r: self.action_list.reactions[r].copy(
                             ) for r in self.action_list.reactions},
                             self.action_list.weights.copy())
        # print({c: self.action_list.conditions[c].copy() for c in self.action_list.conditions})
        # print(self.action_list.weights.copy())
        # print(value_return)
        return value_return


# class to define the list of actions
class Action_List:
    def __init__(self):
        self.conditions = {}
        self.reactions = {}
        self.weights = {}
        # print(self.conditions, self.reactions, self.weights)

    # add condition to some kind of action library
    # 1st arg is a name of the action, and followings are conditions that the action can be executed
    def add_condition(self, key, **kwargs):
        # add the key to the key of the condition library:self.weights
        if not key in self.weights:
            self.weights[key] = 1

        # add to the condition library:self.conditions
        if not key in self.conditions:
            self.conditions[key] = kwargs

        # print(self.weights, self.conditions)
        # print(self.conditions[key].update(kwargs))
        return self.conditions[key].update(kwargs)

    # add reaction to some kind of action liberary
    # 1st arg is a name of the action, and followings are conditions that are changed as an reaction for the action
    def add_reaction(self, key, **kwargs):
        # if there're no correspondent condition, output an exception
        if not key in self.conditions:
            raise Exception(
                'Trying to add reaction \'%s\' without matching condition.' % key)

        # add to the reaction library:self.reactions
        if not key in self.reactions:
            self.reactions[key] = kwargs

        return self.reactions[key].update(kwargs)

    # set weights of each actions : the default are set as 1
    def set_weight(self, key, value):
        if not key in self.conditions:
            raise Exception(
                'Trying to set weight \'%s\' without matching condition.' % key)
        self.weights[key] = value
        # print(self.weights)


def distance_to_state(state_1, state_2):
    _scored_keys = set()
    _score = 0

    for key in state_2.keys():
        _value = state_2[key]
        if _value == -1:
            continue

        if not _value == state_1[key]:
            _score += 1

        _scored_keys.add(key)

    for key in state_1.keys():
        if key in _scored_keys:
            continue

        _value = state_1[key]

        if _value == -1:
            continue

        if not _value == state_2[key]:
            _score += 1

    return _score


def conditions_are_met(state_1, state_2):
    # print state_1, state_2
    # print(state_2.keys())
    for key in state_2.keys():
        _value = state_2[key]

        if _value == -1:
            continue

        if not state_1[key] == state_2[key]:
            return False

    return True


def node_in_list(node, node_list):
    for next_node in node_list.values():
        if node['state'] == next_node['state'] and node['name'] == next_node['name']:
            return True

    return False


def create_node(path, state, name=''):
    path['node_id'] += 1
    path['nodes'][path['node_id']] = {
        'state': state, 'f': 0, 'g': 0, 'h': 0, 'p_id': None, 'id': path['node_id'], 'name': name}
    return path['nodes'][path['node_id']]


# calculate the length-cost of chained action plans by A* algorithm
# actual route seems to be calculated by the function : walk_path()
def astar(start_state, goal_state, actions, reactions, weight_table):
    # initialize the path
    _path = {'nodes': {},
             'node_id': 0,
             'goal': goal_state,
             'actions': actions,
             'reactions': reactions,
             'weight_table': weight_table,
             'action_nodes': {},
             'olist': {}, # TODO:what is olist?
             'clist': {}} # TODO:what is clist?

    # show contents of the path
    # print(_path)
    print
    # print('nodes : ' + str(_path['nodes']))
    # print('node_id : ' + str(_path['node_id']))
    # print('goal : ' + str(_path['goal']))
    # print('actions : ' + str(_path['actions']))
    # print('reactions : ' + str(_path['reactions']))
    # print('weight_table : ' + str(_path['weight_table']))
    # print('action_nodes : ' + str(_path['action_nodes']))
    # print('olist : ' + str(_path['olist']))
    # print('clist : ' + str(_path['clist']))
    # print

    _start_node = create_node(_path, start_state, name='start')
    _start_node['g'] = 0 # distance from start_node to current node(?)
    _start_node['h'] = distance_to_state(start_state, goal_state) # distance from 
    _start_node['f'] = _start_node['g'] + _start_node['h']
    _path['olist'][_start_node['id']] = _start_node
    # print('nodes : ' + str(_path['nodes']))
    # print(_start_node)
    # print(_path['olist'])

    # print(actions)
    for action in actions:
        _path['action_nodes'][action] = create_node(
            _path, actions[action], name=action)
        # print('nodes : ' + str(_path['nodes'][_path['node_id']]))
        # print(_path['action_nodes'][action])
    # print(_path)

    # print(walk_path(_path))
    return walk_path(_path)


# function to calculate the shortest path by A* algorithm
def walk_path(path):
    node = None

    # print(path['clist']) # clist seems to be empty for now....
    _clist = path['clist']

    # print(path['olist']) # olist seems to be a start condition....
    _olist = path['olist']
    # print(len(_olist)) # olist contains a single item : start_condition, so the length of it is 1 

    while len(_olist):
        # find lowest node
        _lowest = {'node': None, 'f': 9000000}
        # print(_olist.values())
        for next_node in _olist.values():
            if not _lowest['node'] or next_node['f'] < _lowest['f']:
                _lowest['node'] = next_node['id']
                _lowest['f'] = next_node['f']

        if _lowest['node']:
            node = path['nodes'][_lowest['node']]
            # print(_lowest['node'])
        else:
            print('else')
            return

        # remove node with lowest rank
        # print(_olist[node['id']])
        del _olist[node['id']]

        # if it matches the goal, we are done
        if conditions_are_met(node['state'], path['goal']):
            _path = []
            while node['p_id']:
                _path.append(node)
                node = path['nodes'][node['p_id']]

            _path.reverse()
            return _path

        # add it to closed
        _clist[node['id']] = node

        # find neighbors
        _neighbors = []
        for action_name in path['action_nodes']:
            if not conditions_are_met(node['state'], path['action_nodes'][action_name]['state']):
                continue

            path['node_id'] += 1

            _c_node = node.copy()
            _c_node['state'] = node['state'].copy()
            _c_node['id'] = path['node_id']
            _c_node['name'] = action_name

            for key in path['reactions'][action_name]:
                _value = path['reactions'][action_name][key]

                if _value == -1:
                    continue

                _c_node['state'][key] = _value

            path['nodes'][_c_node['id']] = _c_node
            _neighbors.append(_c_node)

        for next_node in _neighbors:
            _g_cost = node['g'] + path['weight_table'][next_node['name']]
            _in_olist, _in_clist = node_in_list(
                next_node, _olist), node_in_list(next_node, _clist)

            if _in_olist and _g_cost < next_node['g']:
                del _olist[next_node]

            if _in_clist and _g_cost < next_node['g']:
                del _clist[next_node['id']]

            if not _in_olist and not _in_clist:
                next_node['g'] = _g_cost
                next_node['h'] = distance_to_state(
                    next_node['state'], path['goal'])
                next_node['f'] = next_node['g']+next_node['h']
                next_node['p_id'] = node['id']

                _olist[next_node['id']] = next_node

    return []