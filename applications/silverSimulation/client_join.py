#!/usr/bin/python
'''
Created on Dec 17, 2015

@author: Arthur Valadares
'''

import logging
import logging.handlers
import os
import sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from spacetime_local.frame import frame
from applications.silverSimulation.trafficsim2 import TrafficSimulation2

class Simulation(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        frame_car = frame(address="http://ucigridb.nacs.uci.edu:12000", time_step=1000)
        frame_car.attach_app(TrafficSimulation2(frame_car))

        frame_car.run_async()

        frame.loop()


def setupLoggers():
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CADIS'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)


if __name__ == "__main__":
    setupLoggers()
    sim = Simulation()
