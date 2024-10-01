#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message

import math
import numbers
import numpy as np

class Quaternion(Message):
    """
    Basic class for representing and operation with quaternions that represent orientation in the free space
    Data entries:
    x,y,z,w component of the quaternion
    """
    __attributes__ = ['x', 'y','z','w']
    __attribute_types = ['float32','float32','float32','float32']
    
    def __init__(self, *args, **kwds):
        super(Quaternion, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.x == None or self.y == None or self.z == None or self.w == None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 1

    def __add__(self, other):
        q = Quaternion(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        q.normalize()
        return q

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            q = Quaternion()
            q.x = self.x * other
            q.y = self.y * other
            q.z = self.z * other
            q.w = self.w * other
            return q
        elif isinstance(other, Quaternion):
            x0, y0, z0, w0 = self.x, self.y, self.z, self.w
            x1, y1, z1, w1 = other.x, other.y, other.z, other.w

            x2 = w1*x0 + x1*w0 - y1*z0 + z1*y0
            y2 = w1*y0 + x1*z0 + y1*w0 - z1*x0
            z2 = w1*z0 - x1*y0 + y1*x0 + z1*w0
            w2 = w1*w0 - x1*x0 - y1*y0 - z1*z0

            return Quaternion(x2, y2, z2, w2)
        else:
            return None

    def negate(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def normalize(self):
        """Method to normalize the quaternion
        """
        x = self.x; y = self.y; z = self.z; w = self.w
        mult = 1/math.sqrt(x*x + y*y + z*z + w*w)
        mult = mult if w >= 0 else -mult
        self.x *= mult
        self.y *= mult
        self.z *= mult
        self.w *= mult

    def magnitude(self):
        """Method to normalize the quaternion
        """
        x = self.x; y = self.y; z = self.z; w = self.w
        return math.sqrt(x*x + y*y + z*z + w*w)

    def norm(self):
        """Method to calculate the norm of the rotation
        Returns minimal angle in angle-axis representation
        """
        return 2*math.acos(min(1.0, abs(self.w)))

    def dist(self, other):
        """Calculate the rotation distance between two quaternions
        Returns minimal angle in angle-axis representation
        """
        x0, y0, z0, w0 = self.x, self.y, self.z, self.w
        x1, y1, z1, w1 = -other.x, -other.y, -other.z, other.w

        # print("mag", self.magnitude(), other.magnitude())

        w2 = w1*w0 - x1*x0 - y1*y0 - z1*z0
        # print("w2", w2)
        return 2*math.acos(min(1.0, abs(w2)))
    
    def to_R(self):
        """Method to convert quaternion into rotation matrix
        Returns:
            rotation matrix
        """
        q = [self.w, self.x, self.y, self.z]
        R = [[q[0]**2+q[1]**2-q[2]**2-q[3]**2,     2*(q[1]*q[2]-q[0]*q[3]),      2*(q[1]*q[3]+q[0]*q[2])],
             [2*(q[1]*q[2]+q[0]*q[3]),     q[0]**2-q[1]**2+q[2]**2-q[3]**2,      2*(q[2]*q[3]-q[0]*q[1])],
             [2*(q[1]*q[3]-q[0]*q[2]),         2*(q[2]*q[3]+q[0]*q[1]),   q[0]**2-q[1]**2-q[2]**2+q[3]**2]]
        return np.asarray(R)

    def from_R(self, R):
        """Method to convert rotation matrix into quaternion
        Args:
            R: rotation matrix
        """
        q = np.array([R.trace() + 1, R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]])
        q = 1.0/(2.0*math.sqrt(R.trace() + 1.0000001))*q
        q = q/np.linalg.norm(q)
        self.x = q[1]
        self.y = q[2]
        self.z = q[3]
        self.w = q[0]

    def to_Euler(self):
        """Method to convert quaternion into euler angles  
        Returns:
            yaw, pitch, roll Euler angles
        """
        t0 = +2.0 * (self.w * self.x + self.y * self.z)
        t1 = +1.0 - 2.0 * (self.x * self.x + self.y * self.y)
        roll = math.atan2(t0, t1)
        t2 = +2.0 * (self.w * self.y - self.z * self.x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)
        t3 = +2.0 * (self.w * self.z + self.x * self.y)
        t4 = +1.0 - 2.0 * (self.y * self.y + self.z * self.z)
        yaw = math.atan2(t3, t4)
        return yaw, pitch, roll
    
    def from_Euler(self, yaw, pitch, roll):
        """Method to convert euler angles into quaternion
        Args:
            yaw, pitch, roll: Euler angles
        """
        q = np.zeros(4)
        q[0] = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        q[1] = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        q[2] = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        q[3] = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        # q = q/np.linalg.norm(q)
        self.x = q[1]
        self.y = q[2]
        self.z = q[3]
        self.w = q[0]
        self.normalize()

#Examples of usage
if __name__=="__main__":
    q = Quaternion()
    print("quaternion\n", q.x, q.y, q.z, q.w)
    print("rotation matrix\n", q.to_R())

    #given by euler angles
    yaw = math.pi 
    pitch = 0 
    roll = 0 
    q = Quaternion()
    q.from_Euler(yaw, pitch, roll)
    print("quaternion\n", q.x, q.y, q.z, q.w)
    #show as rotation matrix
    print("rotation matrix\n", q.to_R())
