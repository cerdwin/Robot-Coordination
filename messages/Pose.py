#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Vector3 import *
from .Quaternion import *

class Pose(Message):
    """
    Basic class for representing robot pose in free space in form of x,y,z position vector and orientation quaternion
    Data entries:
    Vector3 position
    Quaternion orientation
    """
    __attributes__ = ['position', 'orientation']
    __attribute_types = ['Vector3','Quaternion']
    
    def __init__(self, *args, **kwds):
        super(Pose, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.position == None:
            self.position = Vector3()
        if self.orientation == None:
            self.orientation = Quaternion()

    #transforms
    def to_T(self):
        T = np.identity(4)
        T[:3,:3] = self.orientation.to_R()
        T[:3,3] = [self.position.x, self.position.y, self.position.z]
        return T

    def dist(self, other):
        """method to calculate the euclidean distance between self and the given pose
        Args:
            other: Pose - the other pose to compute the distance to
        Returns:
            float64 euclidean distance to the other pose
        """
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        dz = self.position.z - other.position.z
        return np.linalg.norm(np.asarray([dx,dy,dz]))


    def plot(self, ax, style='frame', clr=[1,0,0], markersize=12):
        """plot of the pose 
        Args:
            ax: plt figure axes
            style: 'frame', 'point' - style of plotting the path
        """
        if style=='frame':
            dx = np.dot(self.orientation.to_R(),np.asarray([1,0,0]))
            dy = np.dot(self.orientation.to_R(),np.asarray([0,1,0]))
            dz = np.dot(self.orientation.to_R(),np.asarray([0,0,1]))
            if ax.name == "3d": #3D plot
                ax.quiver([self.position.x], [self.position.y], [self.position.z], [dx[0]], [dx[1]], [dx[2]], color='r')
                ax.quiver([self.position.x], [self.position.y], [self.position.z], [dy[0]], [dy[1]], [dy[2]], color='g')
                ax.quiver([self.position.x], [self.position.y], [self.position.z], [dz[0]], [dz[1]], [dz[2]], color='b')
            else: #2D plot
                ax.quiver([self.position.x], [self.position.y], [dx[0]], [dx[1]], color='r')
                ax.quiver([self.position.x], [self.position.y], [dy[0]], [dy[1]], color='g')

        elif style=='point':
            if ax.name == "3d": #3D plot
                ax.plot([self.position.x],[self.position.y],[self.position.z],'.',markersize=markersize, color=clr)
            else: #2D plot
                ax.plot([self.position.x],[self.position.y],'.',markersize=markersize, color=clr)
        else:
            print('unknown pose plot style', style)

#Examples of usage
if __name__=="__main__":
    pose = Pose()
    print(pose.position.x, 
          pose.position.y, 
          pose.position.z, 
          pose.orientation.x, 
          pose.orientation.y,
          pose.orientation.z,
          pose.orientation.w)

    pose = Pose(Vector3(1,2,3),Quaternion(1,0,0,0))
    print(pose.position.x, 
          pose.position.y, 
          pose.position.z, 
          pose.orientation.x, 
          pose.orientation.y,
          pose.orientation.z,
          pose.orientation.w)


