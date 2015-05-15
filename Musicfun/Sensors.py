#! /usr/bin/python
__author__ = 'guy'

import random

class Sensors():
    def __init__(self):
        self.Speed = 0
        self.Angle = 0
        self.MaxSpeed = 30

    def SetAngle(self, direction):
        self.Angle += direction
        self.Angle %= 360

    def SetSpeed(self, newSpeed):
        self.Speed = newSpeed
        self.Speed = min(self.Speed, self.MaxSpeed)
        self.Speed = max(self.Speed, 0)

    def reset(self):
        self.Speed = 0
        self.angle = random.uniform(0,360)
