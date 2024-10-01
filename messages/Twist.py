#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Vector3 import *

class Twist(Message):
    """
    Basic class for representing velocity in free space broken into the linear and angular components
    Data entries:
    Vector3 linear
    Vector3 angular
    """
    __attributes__ = ['linear', 'angular']
    __attribute_types = ['Vector3','Vector3']
    
    def __init__(self, *args, **kwds):
        super(Twist, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.linear == None:
            self.linear = Vector3()
        if self.angular == None:
            self.angular = Vector3()

#Examples of usage
if __name__=="__main__":
    cmd = Twist()
    print(cmd)

    cmd = Twist(Vector3(1.0,-0.5,0.0), Vector3(0.0, 0.0, 1.0))
    print(cmd)

