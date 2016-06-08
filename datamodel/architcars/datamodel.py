'''
@author: Archit dey (architd1@uci.edu)
'''

from __future__ import absolute_import
import logging
from pcc.join import join
from pcc.subset import subset
from pcc.parameter import parameter
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey

import traceback
from datamodel.common.datamodel import Vector3, Color, Vehicle

from math import *
from sympy.geometry import *


logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"

@pcc_set
class ArchitCar(Vehicle.Class()):
    '''
    classdocs
    '''

    _Color = Color.Red
    @dimension(Color)
    def Color(self):
        return self._Color

    @Color.setter
    def Color(self, value):
        self._Color = value

    _TopSpeed = 0
    @dimension(int)
    def TopSpeed(self):
        return self._TopSpeed

    @TopSpeed.setter
    def TopSpeed(self, value):
        self._TopSpeed = value

    _Speed = 0
    @dimension(int)
    def Speed(self):
        return self._Speed

    @Speed.setter
    def Speed(self, value):
        self._Speed = value

    _Route = []
    @dimension(list)
    def Route(self):
        return self._Route

    @Route.setter
    def Route(self, value):
        self._Route = value

    _CurrentSegment = 0
    @dimension(int)
    def CurrentSegment(self):
        return self._CurrentSegment

    @CurrentSegment.setter
    def CurrentSegment(self, value):
        self._CurrentSegment = value

    def get_next_point(self, x1, y1, x2, y2, speed):
        """
          x1, y1, x2, y2 - start and end coordinates
          speed - distances at which the points will be returned
          step - current step in the line segment
        """
        l = sqrt((x2-x1)**2 + (y2-y1)**2)
        slope = (y2-y1)/(x2-x1)
        angle = atan(slope)
        
        velx = speed * sin(angle)
        vely = speed * cos(angle)

        next_x = x1 + ((speed)/l)*(x2-x1)
        next_y = y1 + ((speed)/l)*(y2-y1)
        return round(next_x, 2), round(next_y, 2), velx, vely

    def __init__(self, uid=None):
        self.Position = Vector3(0,0,40.5)
        self.Velocity = Vector3(0,0,0)
        self.Speed = 0
        # self.Length = 0
        # self.Width = 0
        self.Name = "ArchitCars"


@subset(ArchitCar)
class InactiveArchitCar(ArchitCar.Class()):
    @staticmethod
    def __query__(cars):
        return [c for c in cars if InactiveArchitCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Position == Vector3(0,0,40.5)

    def start(self, route, top_speed):
        logger.debug("[InactiveCar]: {0} starting".format(self.ID))

        self.TopSpeed = top_speed   # top speed will be constant, speed will keep changing
        self.Speed = top_speed
        self.Velocity = Vector3(0, 0, 0)
        # self.Position = Vector3(start_x, start_y, 0)
        self.Route = route
        # print "OUTPUT", type(self.Route)
        # print "Contents", self.Route
        self.Position = Vector3(self.Route[0]['X'], self.Route[0]['Y'], 40.5)
        logger.debug("[InactiveCar][{0}]: Starting, New position {2}, Current velocity: {1}".format(self.ID, self.Velocity.X, self.Position));
        self.CurrentSegment = 1

@subset(ArchitCar)
class ActiveArchitCar(ArchitCar.Class()):
    @staticmethod
    def __query__(cars):  # @DontTrace
        return [c for c in cars if ActiveArchitCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Position != Vector3(0,0,40.5)

    def move(self):
    
        '''code with individual steps calculation'''
        
        # end coordinates of the line segment
        end = self.Route[self.CurrentSegment]
        x2, y2 = end['X'], end['Y']

        x, y , velx, vely = self.get_next_point(self.Position.X, self.Position.Y, x2, y2, self.Speed)
        # logger.debug("velx:{0}  vely:{1}".format(velx, vely))

        if (x > x2 or y > y2):
          ''' We have exceeded the endpoint of this line segment
              setting the position of the car as the end of line segment
              increment the count so that we get  endpoints for the next line segment
          '''
          x, y = x2, y2
          self.CurrentSegment += 1 
        
        
        self.Position = Vector3(x, y, self.Position.Z)
        self.Velocity = Vector3(velx, vely, 0)

        logger.debug("[ActiveCar][{0}]: Speed: {1}, New position {3}, Current velocity: {2}".format(self.ID, self.Speed,self.Velocity, self.Position));
        
        if self.Speed < self.TopSpeed:
          self.Speed += round(0.34 * self.TopSpeed, 2);
          # self.Speed = Vector3(self.Velocity.X, 0, 0)
          if self.Speed > self.TopSpeed:
            self.Speed = self.TopSpeed

        lastx = self.Route[-1]['X']
        lasty = self.Route[-1]['Y']

        if (x ==  lastx and y == lasty):
          ''' reached the end of the route, stop car'''
          logger.debug("X: {0}, LastX: {1}".format(x, self.Route[-1]['X']))
          logger.debug("Y: {0}, LastY: {1}".format(y, self.Route[-1]['Y']))
          self.stop();

    def stop(self):
        logger.debug("[ActiveCar]: {0} stopping".format(self.ID));
        self.Position = Vector3(0, 0, 40.5)
        self.Velocity = Vector3(0, 0, 0)
        self.Speed = 0

@parameter(Vehicle)
@subset(ArchitCar)
class CarAndCarNearby(ArchitCar.Class()):
    @staticmethod
    def __query__(cars, cars_in_danger):
        c = []
        for c1 in cars:
          for c2 in cars_in_danger: 
            if CarAndCarNearby.__predicate__(c1, c2):
              c.append(c1)
        return c

    @staticmethod
    def __predicate__(c1, c2):
        # pass
        if c2.Position != Vector3(0, 0, 40.5) and c1.Position != Vector3(0,0,40.5) and c1.ID != c2.ID:
          if ((c2.Position.X < c1.Position.X + (2 * c1.Speed))  and (c2.Position.X > c1.Position.X)) and ((c2.Position.Y < c1.Position.Y + (2* c1.Speed))  and (c2.Position.Y > c1.Position.Y)):
            return True
          return False

    def slow_down(self):
        self.Speed -= round(0.34 * self.TopSpeed, 2);
        if self.Speed < 0:
          self.Speed = 0
        logger.debug("[ActiveCar]: {0} avoiding collision! New Velocity {1}, Current pos {2}".format(self.ID, self.Speed, self.Position));


