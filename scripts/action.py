#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Action:
    def __init__(self, name: str, pre_conditions: dict, effects: dict, cost: float):
        self.name = name
        self.pre_conditions = pre_conditions
        self.effects = effects
        self.cost = cost

    # function to return the object with the format : string
    def __str__(self):
        return self.name

    # function to return the info for this object
    def __repr__(self):
        return self.__str__()

    # function to identify whether this instance is same as the instance : other
    def __cmp__(self, other):
        return cmp(self, other)

    # todo : figure out what function is this?
    def __hash__(self):
        return hash(self)

    # this function will called when you call your instance after generating it
    def __call__(self, **kwargs):
        self.__init__(kwargs.get('name'), kwargs.get(
            'pre_conditions'), kwargs.get('effects'))
        self.exec()

    # todo ; figure out what function is this? (->tuple means that it is annotated that the return value is in format : tuple)
    def.exec(self) -> tuple:
        pass

    
