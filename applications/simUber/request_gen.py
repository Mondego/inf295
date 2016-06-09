import logging
from datamodel.uberCar_Xi.datamodel import InactiveUberCar, ActiveUberCar
from spacetime_local import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Tracker, Deleter
from applications.nodesim.pyroute.loadOsm import LoadOsm
from applications.nodesim.pyroute.route import Router
from applications.nodesim.nodesim import RouteRequest, Route
from datamodel.common.datamodel import Vector3
import random

logger = logging.getLogger(__name__)
LOG_HEADER = "[ReqUber]"


@Producer(RouteRequest, host = 'http://127.0.0.1:12000')
@GetterSetter(RouteRequest, Route)
@GetterSetter(InactiveUberCar, ActiveUberCar, host = 'http://ucigridb.nacs.uci.edu:12000')
@Tracker(Route)
@Deleter(Route)
class ReqSimulation(IApplication.IApplication):
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
        self.start_shutdown = False
        self.ticks = 0

    def initialize(self):
        logger.debug("%s Initializing", LOG_HEADER)

    def update(self):
        logger.info("request route")
        req = RouteRequest()
        req.Owner = "ReqSim"
        req.Source = None
        req.Destination = None
        self.frame.add(req)
        self.ticks += 1
        routes = self.frame.get_new(Route)
        route = None
        if len(routes) > 0:
            for rt in routes:
                if rt.Owner == "ReqSim":
                    self.frame.delete(Route, rt)
                    route = rt
                    break

        if route != None and len(route.Waypoints) > 1:
            cars = self.frame.get(InactiveUberCar)
            print "###########"
            print route.Waypoints
            if cars != None and len(cars) > 0:
                lat_lng_route = []
                for wp in route.Waypoints:
                    lat_lng_route.append([wp['X'], wp['Y']])
                cars[0].start(lat_lng_route)
            else:
                logger.info("Missed request")

    def shutdown(self):
        pass
