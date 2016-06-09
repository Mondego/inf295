"""
Created on Dec 17, 2015

@author: Arthur Valadares
"""

from __future__ import absolute_import
from datamodel.akshatp.datamodel import Car_akshatp, InactiveCar_akshatp, ActiveCar_akshatp, CarAndCarNearby_akshatp
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import GetterSetter, Producer, Tracker, Deleter
from datamodel.nodesim.datamodel import RouteRequest, Route, Waypoint, ResidentialNode, BusinessNode
from random import randrange
from datamodel.common.datamodel import Vector3
import logging

@Producer(RouteRequest, Car_akshatp)
@GetterSetter(RouteRequest, Route, InactiveCar_akshatp, ActiveCar_akshatp, CarAndCarNearby_akshatp)
@Tracker(Route, Waypoint, ResidentialNode, BusinessNode)
@Deleter(Route)

class TrafficSimulation_akshatp(IApplication):
    ticks = 0
    frame = None
    routes = []
    carsproduced = False
    currentroute = 0

    def __init__(self, frame):
        self.frame = frame
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        pass

    def update(self):
        if self.ticks == 0:
            # Generating 5 random routes
            for _ in range(5):
                req = RouteRequest()
                req.Owner = "TrafficSimulation_akshatp"
                req.Source = None  # Picks a random source waypoint
                req.Destination = None  # Picks a random destination waypoint
                req.Name = "Random"
                self.frame.add(req)

        if len(self.routes) == 0:
            for r in self.frame.get_new(Route):
                if r.Owner == "TrafficSimulation_akshatp":
                    self.routes.append(r)

        # if len(self.routes) > 0:
        #     for rt in self.routes:
        #         if rt.Owner == "TrafficSimulation":
        #             self.frame.delete(Route, rt)

        if not self.carsproduced:
            for i in range(1):
                c = Car_akshatp()
                c.Name = "DummyCar"
                self.frame.add(c)
            self.carsproduced = True

        for inactive in self.frame.get(InactiveCar_akshatp):
            if len(self.routes) > self.currentroute:
                inactive.start(v=0.01, route=self.routes[self.currentroute].Waypoints)
                # print("car is at ",inactive.Position.X, inactive.Position.Y, inactive.Position.Z)
                self.currentroute += 1
                self.currentroute %= len(self.routes)
                # print("[TrafficSim] Starting car ID: " + str(inactives[0].ID))
        #
        # if self.ticks % 2 == 0:
        #     for car in self.frame.get(CarAndCarNearby_akshatp):
        #         # print("[TrafficSim] Slowing car ID: " + str(car.ID)+ " Velocity is: " + str(car.Velocity) + " TS: " + str(car.TopSpeed))
        #         car.slowDown()
        # else:
        
        activeCars = self.frame.get(ActiveCar_akshatp)
        print("Found ", len(activeCars), " active cars.")
        for car in activeCars:
            print("[TrafficSim] Moving car ID: " + str(car.ID) + " Pos: " + str(car.Position))
            car.move()

        self.ticks += 1

    def shutdown(self):
        pass
