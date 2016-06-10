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
from applications.archit_sim.trafficsim import TrafficSimulationArchit


logger = None

class Simulation(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        # framenode = frame(time_step=200)
        # framenode.attach_app(NodeSimulation(framenode))
        # http://127.0.0.1:12000 ,  http://ucigridb.nacs.uci.edu:12000
        frame_car = frame(time_step = 600, address='http://ucigridb.nacs.uci.edu:12000')
        frame_car.attach_app(TrafficSimulationArchit(frame_car))

        # frame_ped = frame(time_step = 1000)
        # frame_ped.attach_app(PedestrianSimulation(frame_ped))

        # gfx_frame = frame(time_step = 500)
        # gfx_frame.attach_app(GFXSimulation(gfx_frame))

        # framenode.run_async()
        frame_car.run_async()

        frame.loop()

def SetupLoggers():
    global logger
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)

    #logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
    #flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
    #flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
    #logger.addHandler(flog)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CADIS'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)

if __name__== "__main__":
    SetupLoggers()
    sim = Simulation()
