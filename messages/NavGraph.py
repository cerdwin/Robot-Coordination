#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Pose import *

class NavGraph(Message):
    """
    Basic class for representing navigation graph 
    Data entries:
    Pose[] poses
    list[(int, int)] edges
    """
    __attributes__ = ['poses','edges']
    __attribute_types = ['Pose[]', 'list()']
    
    def __init__(self, *args, **kwds):
        super(NavGraph, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.poses == None:
            self.poses = []
        if self.edges == None:
            self.edges = []

    def plot(self, ax, clr=[1,0,0], plot_edges = True):
        """ plot of the navigation graph
        Args:
            ax: plt figure axes
            clr: color
        """
        for pose in self.poses:
            pose.plot(ax, style='point', clr=clr, markersize=2)
        if plot_edges:
            for edge in self.edges:
                if edge[0] > len(self.poses) or edge[1] > len(self.poses):
                    print('non-existent edge in navigation graph')
                    return
                p1 = self.poses[edge[0]]
                p2 = self.poses[edge[1]]
                if  ax.name == "3d": #3D plot
                    ax.plot([p1.position.x, p2.position.x],
                            [p1.position.y, p2.position.y],
                            [p1.position.z, p2.position.z], color=clr, alpha = 0.3)
                else: # 2D plot
                    ax.plot([p1.position.x, p2.position.x],
                            [p1.position.y, p2.position.y], color=clr, alpha = 0.3)

