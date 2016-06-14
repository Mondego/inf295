'''
Created on Dec 17, 2015

@author: Arthur Valadares
'''

import logging
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter
from datamodel.common.datamodel import Vehicle

logger = logging.getLogger(__name__)
LOG_HEADER = "[SILVERCAR TRAFFIC SIMULATOR]"


@Producer(Vehicle, host="http://ucigridb.nacs.uci.edu:12000")
@GetterSetter(Vehicle, host="http://ucigridb.nacs.uci.edu:12000")
class TrafficSimulation2(IApplication):
    '''
    classdocs
    '''

    frame = None
    ticks = 0

    def __init__(self, frame):
        '''
        Constructor
        '''
        self.frame = frame

    def initialize(self):
        logger.debug("%s Initializing", LOG_HEADER)
        self.frame.add(Vehicle())

    def update(self):
        self.ticks += 1

    def shutdown(self):
        pass
