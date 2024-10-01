#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message

import numpy as np
import numbers 

class Vector3(Message):
    """
    Basic class for representing 3D vector
    Data entries:
    float64 x
    float64 y
    float64 z
    """
    __attributes__ = ['x','y','z']
    __attribute_types = ['float64','float64','float64']
    
    def __init__(self, *args, **kwds):
        super(Vector3, self).__init__(*args, **kwds)
        #message fields cannot be None - fill in zeros instead
        if self.x == None:
            self.x = 0.0
        if self.y == None:
            self.y = 0.0
        if self.z == None:
            self.z = 0.0

    def __add__(self, other):
        v = Vector3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)
        return v
    
    def __IADD__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __sub__(self, other):
        v = Vector3(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z)
        return v
    
    def __ISUB__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def __mul__(self, other):
        if isinstance(other,numbers.Number):
            v = Vector3()
            v.x = self.x * other
            v.y = self.y * other
            v.z = self.z * other
            return v
        else:
            return None
    
    def __IMUL__(self, other):
        if isinstance(other,numbers.Number):
            self.x *= other
            self.y *= other
            self.z *= other

    def norm(self):
        return np.linalg.norm(np.asarray([self.x, self.y, self.z]))


#Examples of usage
if __name__=="__main__":
    x = Vector3()
    print(x.x, x.y, x.z)

    y = Vector3(1, 2, 3)
    print(x.x, x.y, x.z)

    z = Vector3(x=2,z=1)
    print(x.x, x.y, x.z)

    print(x+y)
