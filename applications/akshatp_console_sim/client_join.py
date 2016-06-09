#!/usr/bin/python
"""
Created on Dec 17, 2015

@author: Arthur Valadares
"""

from __future__ import absolute_import
import os
import sys
from spacetime_local.frame import frame
from applications.akshatp_console_sim.trafficsim import TrafficSimulation_akshatp
# from tkinter_visualizer import TkinterVisualizer
from applications.nodesim.nodesim import NodeSimulation
import Tkinter
import logging

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

logger = None

class Simulation(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        # framenode = frame(time_step=200)
        # framenode.attach_app(NodeSimulation(framenode))

        frame_car = frame(time_step=200, address="http://ucigridb.nacs.uci.edu:12000")
        frame_car.attach_app(TrafficSimulation_akshatp(frame_car))

        # root = Tkinter.Tk()

        # con_frame = frame(time_step=200)
        # con_frame.attach_app(TkinterVisualizer(con_frame, root))

        # framenode.run_async()
        frame_car.run()
        # con_frame.run_async()
        # root.mainloop()

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