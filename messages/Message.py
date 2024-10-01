#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Message:
    """ Base class of Message data classes"""

    #attributes are individual data parameters
    __attributes__ = ['entry']

    def __init__(self, *args, **kwds):
        """
        Message constructor. Initialize either empty, using 1-to-1 mapping between the arguments and message attributes, or using keyword arguments in which case the unitialized fields are left with the default values
        """
        #do not take both the args and keywords
        if args and kwds:
            raise TypeError("Message constructor may use only args or keywords, not both")
        #if there are args check for their propper number and fill in the message attributes
        if args:
            if len(args) != len(self.__attributes__):
                raise TypeError("Invalid number of arguments. Args should be: " + str(self.__attributes__))
            else:
                for i,k in enumerate(self.__attributes__):
                    setattr(self,k,args[i])
        #else iterate throught the keywords and assign the message attributes
        else:
            # validate kwds
            for k,v in kwds.items():
                if not k in self.__attributes__:
                    raise AttributeError(str(k) + " is not an attribute of " + self.__class__.__name__)

            # iterate through all attributes so all fields are initialized.
            for k in self.__attributes__:
                if k in kwds:
                    setattr(self, k, kwds[k])
                else:
                    setattr(self, k, None)
    
    def __str__(self):
        str_rep = ""
        #iterate through attributes and print them to string
        for k in self.__attributes__:
            str_rep += k + ":" 
            str_rest = str(getattr(self, k))
            if ':' in str_rest:
                str_rep += '\n'
            str_rep += str_rest
            if str_rep[-1] != '\n':
                str_rep += '\n'        

        return str_rep
