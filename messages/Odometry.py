#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Header import *
from .Pose import *

class Odometry(Message):
    """
    Basic class for representing robot odometry as a pose in the free space given by the x,y,z coordinates and orientation in a form of quaternion
    Data entries:
    Header header # timestamp - odometry timestamp
                  # frame_id - coordinate frame of the odometry 
    Pose pose     # pose of the robot
    """
    __attributes__ = ['header','pose']
    __attribute_types = ['Header','Pose']
    
    def __init__(self, *args, **kwds):
        super(Odometry, self).__init__(*args)
        #message fields cannot be None 
        if self.header == None:
            self.header = Header()
        if self.pose == None:
            self.pose = Pose()

#Examples of usage
if __name__=="__main__":
    odom = Odometry()
    print(odom.header.timestamp)
