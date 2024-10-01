#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message
from .Header import *
from .Pose import *

class OccupancyGrid(Message):
    """
    Basic class for representing occupancy grid map
    Data entries:
    Header header # timestamp - gridmap timestamp
                  # frame_id - coordinate frame of the gridmap 
    float64 resolution # the map resolution [m/cell]
    int width     # width of the map [cells]
    int height    # height of the map [cells]
    Pose pose     # the origin of the map [m, m, rad].  This is the real-world pose of the cell (0,0) in the map.
    float64[] data # the map data in row-major order
    """
    __attributes__ = ['header','resolution','width','height','origin','data']
    __attribute_types = ['Header','float64','int','int','Pose','float64[]']
    
    def __init__(self, *args, **kwds):
        super(OccupancyGrid, self).__init__(*args)
        #message fields cannot be None 
        if self.header == None:
            self.header = Header()
        if self.origin == None:
            self.origin = Pose()

    def plot(self, ax):
        """ 2D plot of the pose 
        Args:
            ax: plt figure axes
        """
        if self.data is not None:
            extent = (self.origin.position.x, 
                      self.origin.position.x + self.resolution*self.width,
                      self.origin.position.y,
                      self.origin.position.y + self.resolution*self.height)
            gmap = self.data.reshape(self.height, self.width)
            ax.imshow(gmap, cmap="Greys", interpolation='nearest', extent=extent, vmin=0, vmax=1, origin='lower')


#Examples of usage
if __name__=="__main__":
    gridmap = OccupancyGrid()
    gridmap.width = 100
    gridmap.height = 100
    gridmap.resolution = 1
    gridmap.data = np.zeros((gridmap.height*gridmap.width))

    print(gridmap)

