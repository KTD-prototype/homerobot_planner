#!/usr/bin/env python
# -*- coding: utf-8 -*-


# scripts to define the basic characteristics of each agents
import rospy


class Agent:
    def __init__(self, myname, energy_rest, max_lin_vel, max_ang_vel):
        self.myname = myname
        self.energy_rest = energy_rest
        self.max_lin_vel = max_lin_vel
        self.max_ang_vel = max_ang_vel

    def show_base_spec(self):
        print('Name : ' + self.myname + " with " +
              str(self.energy_rest) + "% energy rest")
        print('My mobility : ' + str(self.max_lin_vel) +
              " [m/s] and " + str(self.max_ang_vel) + " [rad/s]")


class Family:
    def __init__(self, myname, age):
        self.myname = myname
        self.age = age

    def show_base_spec(self):
        print('My name is : ' + self.myname +
              ' and I am ' + str(self.age) + 'yeares old!')


class BaseStation:
    def __init__(self, myname):
        pass

    def charge(self, energy):
        energy += 1
        print('charged!')
        return energy


class RootGoal:
    def __init__(self):
        pass

    def clean(self):
        pass

    def bring(self):
        pass

    def manipulate(self):
        pass


if __name__ == '__main__':
    abc_rover = Agent('Alex', 90, 0.5, 1.1)
    abc_rover.show_base_spec()

    bob = Family('Bob', 6)
    bob.show_base_spec()

    base_station = BaseStation('charger')
    abc_rover.energy_rest = base_station.charge(abc_rover.energy_rest)
    abc_rover.show_base_spec()
