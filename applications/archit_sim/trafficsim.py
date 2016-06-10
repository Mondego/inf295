'''
Created on Dec 17, 2015

@author: Arthur Valadares
'''

import logging
from datamodel.architcars.datamodel import ArchitCar, InactiveArchitCar, ActiveArchitCar, CarAndCarNearby

from datamodel.nodesim.datamodel import RouteRequest, Route, Waypoint,\
    ResidentialNode, BusinessNode

from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Tracker, \
    Deleter

from random import choice
import random


# logger = logging.getLogger(__name__)
LOG_HEADER = "[TRAFFIC]"

#http://ucigridb.nacs.uci.edu:12000
# @Producer(ArchitCar, host = 'http://127.0.0.1:12000')
@Producer(ArchitCar, RouteRequest)
@GetterSetter(RouteRequest, Route, InactiveArchitCar, ActiveArchitCar, CarAndCarNearby)
@Tracker(Route, Waypoint, ResidentialNode, BusinessNode)
@Deleter(Route, ArchitCar)
class TrafficSimulationArchit(IApplication):
  '''
  classdocs
  '''

  frame = None
  ticks = 0
  TICKS_BETWEEN_CARS = 2
  cars = []
  # to store the route at class level
  route_req = []
  first = False;
  source = None
  destination = None

  def __init__(self, frame):
    '''
    Constructor
    '''
    self.frame = frame
    self.logger = logging.getLogger(__name__)

  def initialize(self):
    self.logger.debug("%s Initializing", LOG_HEADER)
    for i in xrange(2):
      self.frame.add(ArchitCar())
    
    # self.frame.add(Car("1d4883f3-b8f7-11e5-a78c-acbc327e1743")) # Valid uuid Example
    # self.frame.add(Car(10)) # Valid int Example
    # self.frame.add(Car("1d4883f3")) Invalid  Example - Crashes

    # self.cars = self.frame.get(Car)

  def update(self):
    # for c in self.frame.get(ArchitCar):
    #   self.logger.debug("%s Deleting", c.ID)
    #   self.frame.delete(ArchitCar, c)
    

    self.logger.info("%s Tick", LOG_HEADER)
    
    # create the route request only the first timev  
    if self.ticks == 0:
      req = RouteRequest()
      req.Owner = "Archit"
      # req.Source = None # Picks a random source waypoint
      req.Source = self.frame.get(Waypoint, '800')
      # req.Destination = None # Picks a random destination waypoint
      req.Destination = self.frame.get(Waypoint, '1000')
      req.Name = "Random"
      self.frame.add(req)

    # source = self.frame.get(Waypoint, '40')
    # destination = self.frame.get(Waypoint, '1000')
    # req.Source = source
    # req.Destination = destination

    self.route_req = self.frame.get(Route)
    # self.logger.debug("Route req--------------%s", self.route_req)
    
    if self.ticks % self.TICKS_BETWEEN_CARS == 0:
      try:
        inactives = self.frame.get(InactiveArchitCar)
        self.logger.debug("%s ************** InactiveCars: %s", LOG_HEADER, len(inactives))

        if len(inactives) > 0:
          if len(self.route_req) > 0:
            self.logger.debug("INSIDE-----------------")
            
            for rt in self.route_req:
                if rt.Owner == "Archit":
                    # self.logger.info("[%s]: %s", rt.Name, rt.Waypoints)
                    self.route = rt.Waypoints
                    # self.frame.delete(Route, rt)

                    self.logger.debug("%s ************** Starting car %s", LOG_HEADER, inactives[0].ID)
                    speed = random.randrange(5, 16, 5)
                    # self.logger.debug("ROUTE: %s", len(self.route))
                    inactives[0].start(self.route, 1);

      except Exception:
        self.logger.exception("Error: ")

    if self.ticks % 2 == 0:
      # pass
      for car in self.frame.get(ActiveArchitCar):
        try:
          car.move()
        except:
          self.logger.debug("Error, stopping car")
          car.stop()
    else:
      cars_going_to_hit = self.frame.get(CarAndCarNearby)
      for car in cars_going_to_hit:
        car.slow_down()
      # pass


    self.ticks += 1

  def shutdown(self):
    for rt in self.route_req:
      if rt.Owner == "Archit":
        self.frame.delete(Route, rt)

    for car in self.frame.get(ActiveArchitCar):
        car.stop()