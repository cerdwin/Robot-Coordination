#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .Message import Message

import time

class Header(Message):
    """
    Basic class for representing message header
    Data entries:
    float64 timestamp  # timestamp of the Message
    str frame_id       # coordinate frame of the Message
    """
    __attributes__ = ['timestamp', 'frame_id']
    __attribute_types = ['float64','str']
    
    def __init__(self, *args, **kwds):
        super(Header, self).__init__(*args, **kwds)
        #message fields cannot be None 
        if self.timestamp == None:
            self.timestamp = time.time()
        if self.frame_id == None:
            self.frame_id = 'base_frame'

#Examples of usage
if __name__=="__main__":
    hdr = Header()
    print(hdr.timestamp, hdr.frame_id)


