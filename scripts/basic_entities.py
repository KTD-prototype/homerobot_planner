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
    def __init__(self):
        pass


class BaseStation:
    def __init__(self):
        pass


if __name__ == '__main__':
    abc_rover = Agent('Alex', 90, 0.5, 1.1)
    abc_rover.show_base_spec()
