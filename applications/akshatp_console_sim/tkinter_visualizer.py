#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Apr 23, 2016
@author: Akshat Patel
"""

from __future__ import absolute_import
from datamodel.akshatp.datamodel import ActiveCar_akshatp, CarAndCarNearby_akshatp, Car_akshatp
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Getter
import Tkinter
import logging

@Getter(ActiveCar_akshatp, CarAndCarNearby_akshatp, Car_akshatp)

class TkinterVisualizer(IApplication):

    routesdrawn = False

    def __init__(self, frame, tkgui):
        """
        Constructor
        """
        self.logger = logging.getLogger(__name__)
        self.frame = frame
        self.sprites = []

        # Create the objDict
        self.objDict = {}

        # Set up the GUI part
        self.tkgui = tkgui

        self.canvas = Tkinter.Canvas(tkgui, width=800, height=1800)
        self.canvas.pack()

        self.gui = GuiPart(self.objDict)

        # Start the periodic call in the GUI to check if the objDict contains
        # anything
        self.periodicCall()

    def initialize(self):
        pass

    def update(self):
        if self.routesdrawn == False:
            cars = self.frame.get(ActiveCar_akshatp)
            if len(cars) == 2:
                for c in cars:
                    for i in xrange(1, len(c.Route)):
                        self.canvas.create_line(c.Route[i - 1]['X'],
                                                c.Route[i - 1]['Y'],
                                                c.Route[i]['X'],
                                                c.Route[i]['Y'],
                                                dash=(4, 2))
                self.routesdrawn = True

        for sprite in self.sprites:
            self.canvas.delete(sprite)

        for c in self.frame.get(ActiveCar_akshatp):
            self.objDict[c.ID] = c

        for c in self.frame.get(CarAndCarNearby_akshatp):
            self.objDict[str(c.ID) + " alert"] = c

        pass

    def periodicCall(self):
        self.gui.processIncoming(self)
        self.tkgui.after(1, self.periodicCall)

    def shutdown(self):
        pass


class GuiPart:
    def __init__(self, objDic):
        self.objDic = objDic

    def processIncoming(self, cs):
        """Handle all messages currently in the queue, if any."""
        l = []

        for sprite in cs.sprites:
            cs.canvas.delete(sprite)

        for key, msg in self.objDic.copy().iteritems():
            x1, y1, x2, y2, x3, y3, x4, y4 = msg.CarRotatedBox
            hx1, hy1, hx2, hy2, hx3, hy3, hx4, hy4 = msg.CarRotatedHitBox

            l.append(cs.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, x1, y1, fill="blue"))

            if key.endswith("alert"):
                l.append(cs.canvas.create_polygon(hx1, hy1, hx2, hy2, hx3, hy3, hx4, hy4, hx1, hy1, fill="red"))
            else:
                l.append(cs.canvas.create_polygon(hx1, hy1, hx2, hy2, hx3, hy3, hx4, hy4, hx1, hy1, fill="green"))

        cs.sprites = l
