'''
Created on Dec 17, 2015

@author: Arthur Valadares
'''

import logging
from datamodel.silverCar.datamodel import SilverCar, InactiveSilverCar, ActiveSilverCar
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Tracker, \
    Deleter
from datamodel.nodesim.datamodel import RouteRequest, Route, Waypoint, ResidentialNode, BusinessNode
from datamodel.common.datamodel import Vector3, Color, Vehicle

logger = logging.getLogger(__name__)
LOG_HEADER = "[SILVERCAR TRAFFIC SIMULATOR]"


@Producer(Vehicle, SilverCar, RouteRequest, host="http://ucigridb.nacs.uci.edu:12000")
@GetterSetter(SilverCar, InactiveSilverCar, ActiveSilverCar, Route, host="http://ucigridb.nacs.uci.edu:12000")
@Deleter(Route, host="http://ucigridb.nacs.uci.edu:12000")
class TrafficSimulation(IApplication):
    '''
    classdocs
    '''

    frame = None
    ticks = 0
    #TICKS_BETWEEN_CARS = 10
    #cars = []

    def __init__(self, frame):
        '''
        Constructor
        '''
        self.frame = frame

    def initialize(self):
        logger.debug("%s Initializing", LOG_HEADER)
        for i in xrange(1):
            self.frame.add(Vehicle())

        #self.cars = self.frame.get(silverCar)

    def createRoute(self, car):
        req = RouteRequest()
        req.Owner = car.ID
        req.Source = None # Picks a random source waypoint
        req.Destination = None # Picks a random destination waypoint
        req.Name = "Random"
        logger.debug("Car {0} Requested route".format(car.ID))
        self.frame.add(req)

    def update(self):
        self.ticks += 1
        '''
        for car in self.frame.get(ActiveSilverCar):
            #logger.debug("car {0} is active ".format(car.ID))
            #car.move()
            car = Vector3(441,139,40.5)

        routes = self.frame.get_new(Route)
        print "found {0} new routes".format(len(routes))
        if len(routes) > 0:
            for rt in routes:
                for car in self.frame.get(InactiveSilverCar):
                    logger.debug("checking {0} : {1}".format(rt.Owner, car.ID))
                    if(rt.Owner == car.ID):
                        logger.debug("assigning route for car {0}".format(car.ID))
                       # temp =
                        #print temp
                        car.Waypoints = rt.Waypoints[:]
                        self.frame.delete(Route, rt)
                        break

        for car in self.frame.get(InactiveSilverCar):
            self.createRoute(car)'''




    def shutdown(self):
        pass
