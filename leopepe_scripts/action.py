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


class ActionResponse:
    def __init__(self, name: str, action_type: str, return_code: str, stdout: str='', stderr: str=''):
        self.name = name
        self.action_type = action_type
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.__response_parser()

    # function to return the object with the format : string
    def __str__(self):
        return 'Name:{}, Response:{}, ReturnCode:{}'.format(self.name, self.response, self.return_code)

    # function to return the info for this object
    def __repr__(self):
        return self.__str__()

    # function to prepare the parameter:response
    def __response_parser(self):
        if not self.stdout == '':
            self.response = self.stdout
        elif not self.stderr == '':
            self.response = self.stderr


class ShellAction(Action):
    def __init__(self, name: str, pre_conditions: dict, effects: dict, shell: str, const: float=0.0):
        self.response = {}
        self.type = 'shell'
        self.shell = shell
        Action.__init__(
            self, name=name, pre_conditions=pre_conditions, effects=effects, cost=cost)

    def exec(self):
        cmd = self.shell
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        try:
            stdout, stderr = process.communicate(timeout=30)
            return_code = process.returncode
            self.response = ActionResponse(
                name=self.name, action_type='shell', stdout=stdout, stderr=stderr, return_code=return_code)

        except TimeoutError as e:
            process.kill()
            raise('{}'.format(e))
        finally:
            process.kill()

        return self.response


class Actions:
    def __init__(self):
        self.actions = list()

    # function to return the list of actions
    def __str__(self):
        return '{}'.format(self.actions)

    # function to return the list of actions
    def __repr__(self):
        return self.__str__()

    # convert the list of actions into iterrator
    def __iter__(self):
        return iter(self.actions)

    # return the number of actions in the list
    def __len__(self):
        return len(self.actions)

    # function to find a action named "key" from the list
    def __getitem__(self, key):
        for a in self.actions:
            if a.name == key:
                return a
            else:
                return None

    # todo:what is difference between this func and __getitem__ ?
    def get(self, name):
        result = None
        for action in self.actions:
            if action.name == name:
                result = action
        return result

    # search action that has a certain pre_condition
    def get_by_pre_condition(self, pre_conditions: dict):
        for action in self.actions:
            if action.pre_conditions == pre_conditions:
                return action

    # search action that has a certain effect
    def get_by_effect(self, effects: dict):
        for action in self.actions:
            if action.effects == effects:
                return action

    # todo:what is this function?
    # is it for adding new action to the que for actions that should be executed?
    def __add_shell_action(self, name, shell, pre_conditions, effects):
        if not ShellAction(name=name, shell=shell, pre_conditions=pre_conditions, effects=effects) in self.actions:
            self.actions.append(ShellAction(
                name=name, shell=shell, pre_conditions=pre_conditions, effects=effects))
        else:
            raise ActionAlreadyInCollectionError

    # todo:what is this?
    def __add_obj_action(self, name, obj, pre_conditions, effects):
        raise NotImplementedError

    # function to add an action to the list
    def add(self, **kwargs):
        if kwargs.get('shell') and kwargs.get('obj'):
            raise ActionMultipleTypeError

        name = kwargs.get('name')
        shell = kwargs.get('shell', None)
        obj = kwargs.get('obj', None)
        pre_conditions = kwargs.get('pre_conditions', None)
        effects = kwargs.get('effects', None)
        if shell:
            self.__add_shell_action(name, shell, pre_conditions, effects)
        elif obj:
            self.__add_obj_action(name, obj, pre_conditions, effects)

    # function to remove action
    def remove(self, name: str):
        result = False
        for action in self.actions:
            if action.name == name:
                self.actions.remove(action)
                result = True
        return result

    # execute actions(shell_actions) sequentially and
    def exec_all(self) -> list:
        responses = [s.exec() for s in self.actions()]
        return responses

    # method to compare two actions are same or not
    @staticmethod
    def compare_actions(action1: Action, action2: Action):
        result = None
        if action1.pre_conditions == action2.pre_conditions and action1.effects == action2.effects:
            result = 'Action {} and Action {} are equal'.format(
                action1.name, action2.name)

        return result
