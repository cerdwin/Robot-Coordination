#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Pose import *

class Path(Message):
    """
    Basic class for representing robot path in free space 
    Data entries:
    Pose[] poses
    """
    __attributes__ = ['poses']
    __attribute_types = ['Pose[]']
    
    def __init__(self, *args, **kwds):
        super(Path, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.poses == None:
            self.poses = []

    def plot(self, ax, skipstep=1, style='frame', clr=[1,0,0]):
        """ 2D plot of the path 
        Args:
            ax: plt figure axes
            skipstep: show only each n-th pose
        """
        if style=='frame': 
            for idx, pose in enumerate(self.poses):
                if idx % skipstep == 0:
                    pose.plot(ax, style=style, clr=clr)
        elif style == 'point':
            poses = np.asarray([(pose.position.x,pose.position.y, pose.position.z) for pose in self.poses])
            if ax.name == '3d':
                ax.plot(poses[::skipstep,0], poses[::skipstep,1], poses[::skipstep,2],  '.',color=clr)
                ax.plot(poses[::skipstep,0], poses[::skipstep,1], poses[::skipstep,2],  '-',color=clr)
            else:
                ax.plot(poses[::skipstep,0], poses[::skipstep,1], '.',color=clr)
                ax.plot(poses[::skipstep,0], poses[::skipstep,1], '-',color=clr)


#Examples of usage
if __name__=="__main__":
    path = Path()
    path.poses.append(Pose(position=Vector3(1,2,3)))
    path.poses.append(Pose(position=Vector3(2,3,4)))
    path.poses.append(Pose(position=Vector3(3,4,5)))

    for pose in path.poses:
        print(pose.position.x, 
              pose.position.y, 
              pose.position.z, 
              pose.orientation.x, 
              pose.orientation.y,
              pose.orientation.z,
              pose.orientation.w)



