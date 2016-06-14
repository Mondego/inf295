﻿#!/usr/bin/python
'''
Created on Dec 17, 2015

@author: Arthur Valadares
'''

import logging
import logging.handlers
import os
import sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from applications.nodesim.nodesim import NodeSimulation
#from applications.nodesim.testsim import NodeTestSimulation
from spacetime_local.frame import frame

class Simulation(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        framenode = frame("http://ucigridb.nacs.uci.edu:12000/", time_step=200)
        framenode.attach_app(NodeSimulation(framenode))

        # frametest = frame(time_step=200)
        # frametest.attach_app(NodeTestSimulation(frametest))

        framenode.run_async()
        # frametest.run_async()

        frame.loop()

def setupLoggers():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    clog = logging.StreamHandler()
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == "__main__":
    setupLoggers()
    sim = Simulation()
