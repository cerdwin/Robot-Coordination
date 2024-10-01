#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Header import *

import math
import numpy as np

class LaserScan(Message):
    """
    Basic class for representing a single line scan from planar laser scanner
    Data entries:
    Header header # timestamp - laser scan acquisition time
                  # frame_id - coordinate frame of the obtained laser scan 
    float32 angle_min       # start angle of the scan [rad]
    float32 angle_max       # end angle of the scan [rad]
    float32 angle_increment # angular distance between measurements [rad]
    float32 range_min       # minimum measurable distance [m]
    float32 range_max       # maximum measurable distance [m]
    
    float32[] distances # distance data [m] (note: distance data out of range should be discarded) 
    """
    __attributes__ = ['header','angle_min','angle_max','angle_increment','range_min','range_max','distances']
    __attribute_types = ['Header','float32','float32','float32','float32','float32','float32[]']
    
    def __init__(self, *args, **kwds):
        super(LaserScan, self).__init__(*args)
        #message fields cannot be None 
        if self.header == None:
            self.header = Header()
        if self.angle_min == None:
            self.angle_min = 0
        if self.angle_max == None:
            self.angle_max = 0
        if self.angle_increment == None:
            self.angle_increment = 0
        if self.range_min == None:
            self.range_min = 0
        if self.range_max == None:
            self.range_max = 0
        if self.distances == None:
            self.distances = []

    def plot(self, ax):
        """ 2D plot of the LaserScan 
        Args:
            ax: plt figure axes
        """
        scan_x = []
        scan_y = []
        #get x,y coordinates of the laser scan points
        for idx, pt in enumerate(self.distances):
            scan_x.append(pt*np.cos((self.angle_min + idx*self.angle_increment))) 
            scan_y.append(pt*np.sin((self.angle_min + idx*self.angle_increment)))

        #plot the scan
        ax.scatter(scan_x, scan_y)


