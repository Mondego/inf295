#!/usr/bin/python


import logging
import logging.handlers
import os
import sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from spacetime_local.frame import frame
from applications.simUber.trafficsim import TrafficSimulation
from applications.simUber.request_gen import ReqSimulation
from applications.simUber.testCollision import ColSimulation
from applications.nodesim.nodesim import NodeSimulation

logger = None

class Simulation(object):
    def __init__(self):
        frame_car = frame(time_step=1000)
        frame_car.attach_app(TrafficSimulation(frame_car))

        frame_node = frame(time_step=1000)
        frame_node.attach_app(NodeSimulation(frame_node))

        frame_request = frame(time_step=1000)
        frame_request.attach_app(ReqSimulation(frame_request))

        frame_car.run_async()
        frame_node.run_async()
        frame_request.run_async()

        frame.loop()

def setupLoggers():
    global logger
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)

    # logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
    # flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
    # flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
    # logger.addHandler(flog)
    logging.getLogger("requests").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CADIS'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)


if __name__ == "__main__":
    setupLoggers()
    sim = Simulation()
