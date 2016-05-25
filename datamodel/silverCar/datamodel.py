'''
Created on Dec 15, 2015

@author: arthurvaladares
'''
from __future__ import absolute_import
import logging
from pcc.join import join
from pcc.subset import subset
#from pcc.parameterize import parameterize
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey
import string, math

from spacetime_local.frame import frame

import traceback
from datamodel.common.datamodel import Vector3, Color, Vehicle
from datamodel.nodesim.datamodel import RouteRequest, Route, Waypoint, ResidentialNode, BusinessNode

logger = logging.getLogger(__name__)
LOG_HEADER = "[SilverCar]"
'''
def get_points(path):
    f = open(path, 'r')
    retorno = []
    line = f.readline().strip()
    while line:
        temp = line.split(',')
        retorno.append(Vector3(float(temp[0]),float(temp[1]),0))
        line = f.readline().strip()
    #print(retorno[0].X)
    f.close()
    return retorno'''


class Segment:
    p1 = Vector3(0,0,0)
    p2 = Vector3(0,0,0)

# Given three colinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if(q.X <= max(p.X, r.X) and q.X >= min(p.X, r.X) and
        q.Y <= max(p.Y, r.Y) and q.Y >= min(p.Y, r.Y)):
       return True
    return False

# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are colinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
    # See http:#www.geeksforgeeks.org/orientation-3-ordered-points/
    # for details of below formula.
    val = (q.Y - p.Y) * (r.X - q.X) - (q.X - p.X) * (r.Y - q.Y)

    if (val == 0): return 0  # colinear
    if (val > 0): return 1
    return 2 # clock or counterclock wise

# The main function that returns True if line segment 'p1q1'
# and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the four orientations needed for general and
    # special cases
    o1 = orientation(p1, q1, p2);
    o2 = orientation(p1, q1, q2);
    o3 = orientation(p2, q2, p1);
    o4 = orientation(p2, q2, q1);

    # General case
    if (o1 != o2 and o3 != o4):
        return True;

    # Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if (o1 == 0 and onSegment(p1, p2, q1)): return True;

    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if (o2 == 0 and onSegment(p1, q2, q1)): return True;

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if (o3 == 0 and onSegment(p2, p1, q2)): return True;

     # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if (o4 == 0 and onSegment(p2, q1, q2)): return True;

    return False # Doesn't fall in any of the above cases

@pcc_set
class SilverCar(Vehicle.Class()):
  '''
  classdocs
  '''
  #_Waypoints = get_points("/Users/Pedro/Dev/spacetime/python/datamodel/silverCar/car-4.rd")
  _Waypoints = []
  SPEED = 20
  route = None
  numRequestedRoutes = 0
  numRoutesFinished = 0
  ticks = 0
  _Name = ""
  #FINAL_POSITION = 7000

  def __init__(self, uid=None):
    self._ID = uid
    self._Length = 30
    self._Width = 10
    self._ticksToTarget = 0
    self._Velocity = Vector3(0,0,0)
    self._Position = Vector3(0, 0, 0)
    logger.debug("%s car created", LOG_HEADER)


  @dimension(list)
  def Waypoints(self):
    return self._Waypoints

  @Waypoints.setter
  def Waypoints(self, value):
    self._Waypoints = value
    #logger.debug("%s assigned route for car {0}".format(self._ID), LOG_HEADER)


  _Color = Color.White
  @dimension(Color)
  def Color(self):
    return self._Color

  @Color.setter
  def Color(self, value):
    self._Color = value


  def updateVelocity(self):
    '''if(self.route is None):
        routes = self.frame.get_new(Route)
        if len(routes) > 0:
            for rt in routes:
                if rt.Owner == self._ID:
                    self.route = rt
                    self.frame.delete(Route, rt)
                    logger.debug("Route Obtained FROM: {0} TO: {1}".format(self.route.Source, self.route.Destination))
                    _Waypoints = rt.Waypoints()
                    #self._ticksToTarget = self.TicksToNextTarget()
                    break
'''

    #if(self.route is not None):
    if(len(self._Waypoints) == 1):
        self.numRoutesFinished += 1
        logger.debug("Route Finished after {0} Ticks".format(self.ticks))
        self.ticks = 0
        self._Velocity = Vector3(0,0,0)
    else:
        d = 0.5
        m = (self._Waypoints[1].X - self._Waypoints[0].X)/(self._Waypoints[1].Y - self._Waypoints[0].Y)*-1
        x0 = math.sqrt(math.pow(d,2)/(1+math.pow(m,2))) + self._Waypoints[0].X
        x1 = math.sqrt(math.pow(d,2)/(1+math.pow(m,2))) + self._Waypoints[1].X
        y0 = m*(x0 - self._Waypoints[0].X) + self._Waypoints[0].Y
        y1 = m*(x1 - self._Waypoints[1].X) + self._Waypoints[1].Y
        temp = Vector3(x1 - x0, y1 - y0, self._Waypoints[1].Z - self._Waypoints[0].Z)
        #temp = Vector3(self._Waypoints[1].X - self._Waypoints[0].X, self._Waypoints[1].Y - self._Waypoints[0].Y, self._Waypoints[1].Z - self._Waypoints[0].Z)
        #print("Original: X = {0}, Y = {1}; Novo: X = {2}, Y = {3}".format(self._Waypoints[0].X, self._Waypoints[0].Y, x0, y0))
        #print("Original: X = {0}, Y = {1}; Novo: X = {2}, Y = {3}".format(self._Waypoints[1].X, self._Waypoints[1].Y, x1, y1))

        module = math.sqrt(math.pow(temp.X, 2) + math.pow(temp.Y, 2) + math.pow(temp.Z, 2))
        temp.X = (temp.X / module) * self.SPEED
        temp.Y = (temp.Y / module) * self.SPEED
        temp.Z = (temp.Z / module) * self.SPEED
        self._Velocity = temp
        self._Waypoints.pop(0)
        self._ticksToTarget = self.TicksToNextTarget()

  @staticmethod
  def __predicate__(c):
    return c.Velocity != Vector3(0,0,0)

  def move(self):
    self.ticks += 1

    #logger.debug("[SilverCar]: Current velocity: {0}, New position {1}, TicketsToTarget {2}".format(self.Velocity, self.Position, self._ticksToTarget));

    if(self._ticksToTarget <= 0):
        self.updateVelocity()

    if(self._ticksToTarget > 0):
        self.Position = Vector3(self.Position.X + self.Velocity.X, self.Position.Y + self.Velocity.Y, self.Position.Z + self.Velocity.Z)

    self._ticksToTarget -= 1
    # End of ride
    #if (self.Position.X >= self.FINAL_POSITION or self.Position.Y >= self.FINAL_POSITION):
    #if(len(self._Waypoints) == 0):
    #  self.stop();

  def stop(self):
    logger.debug("%s: {0} stopping".format(self.ID), LOG_HEADER);
    self.Position.X = 0;
    self.Position.Y = 0;
    self.Position.Z = 0;
    self.Velocity.X = 0;
    self.Velocity.Y = 0;
    self.Velocity.Z = 0;

  def start(self):
    logger.debug("[CAR]: {0} starting at position {1} {2}".format(self.ID,self.Position.X, self.Position.Y))
    #self.Velocity = Vector3(self.SPEED, 0, 0)
    self.updateVelocity()

  def collision(self, otherCar):
    collided = False
    for i in self.carToSegments():
        for j in otherCar.carToSegments():
            if(doIntersect(i.p1, i.p2, j.p1, j.p2)):
                collided = True
                print "Car {0} collided with car {1}".format(self.ID, otherCar.ID)
                return True
    if not collided:
        print "1: ",self.ID, self.Position.X, self.Position.Y, "2: ",otherCar.ID, otherCar.Position.X, otherCar.Position.Y
    #    print "No collision detected"

    return collided


  def carToSegments(self):
      px = self.Position.X
      py = self.Position.Y
      widthBy2 = self._Width / 2
      lengthBy2 = self._Length / 2

      seg1 = Segment()
      x1 = px - widthBy2
      x2 = px + widthBy2
      y1 = py + lengthBy2
      y2 = py + lengthBy2
      seg1.p1 = Vector3(x1,y1,0)
      seg1.p2 = Vector3(x2,y2,0)

      seg2 = Segment()
      x1 = px + widthBy2
      x2 = px + widthBy2
      y1 = py + lengthBy2
      y2 = py - lengthBy2
      seg2.p1 = Vector3(x1,y1,0)
      seg2.p2 = Vector3(x2,y2,0)

      seg3 = Segment()
      x1 = px + widthBy2
      x2 = px - widthBy2
      y1 = py - lengthBy2
      y2 = py - lengthBy2
      seg3.p1 = Vector3(x1,y1,0)
      seg3.p2 = Vector3(x2,y2,0)

      seg4 = Segment()
      x1 = px - widthBy2
      x2 = px - widthBy2
      y1 = py - lengthBy2
      y2 = py + lengthBy2
      seg4.p1 = Vector3(x1,y1,0)
      seg4.p2 = Vector3(x2,y2,0)

      return [seg1, seg2, seg3, seg4]



  _ticksToTarget = 0
  @dimension(int)
  def TicksToTarget(self):
    return self._ticksToTarget

  @TicksToTarget.setter
  def TicksToTarget(self, value):
    self._ticksToTarget = value

  def TicksToNextTarget(self):
      return math.ceil(math.sqrt(math.pow(self._Waypoints[0].X - self.Position.X, 2) + math.pow(self._Waypoints[0].Y - self.Position.Y, 2) + math.pow(self._Waypoints[0].Z - self.Position.Z, 2))/self.SPEED)

@join(SilverCar, SilverCar)
class CarNearCar(SilverCar):
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @dimension(SilverCar)
    def car1(self):
        return self._car1

    @car1.setter
    def car1(self, value):
        self._car1 = value

    @dimension(SilverCar)
    def silverCar(self):
        return self._silverCar

    @silverCar.setter
    def silverCar(self, value):
        self._silverCar = value

    def __init__(self, c1, c2):
        self._car1 = c1
        self._silverCar = c2

    @staticmethod
    def __query__(cars1, cars2):
        return [CarNearCar.Create(c1, c2) for c1 in cars1 for c2 in cars2 if CarNearCar.__predicate__(c1, c2)]

    @staticmethod
    def __predicate__(c1, c2):
        #collided = c1.collision(c2)
        return c1 != c2
    
    
@subset(SilverCar)
class InactiveSilverCar(SilverCar.Class()):
    _Name = ""
    @staticmethod
    def __query__(cars):
        return [c for c in cars if InactiveSilverCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return len(c._Waypoints) == 0

    #def start(self):
        # logger.debug("[InactiveCar]: {0} starting".format(self.ID))
        #self.Velocity = Vector3(self.SPEED, 0, 0)
        #self.Position = Vector3(self.Position.X - self.Velocity.X, self.Position.Y + self.Velocity.Y,
        #                        self.Position.Z + self.Velocity.Z)


@subset(SilverCar)
class ActiveSilverCar(SilverCar.Class()):
    _Name = ""

    @staticmethod
    def __query__(cars):  # @DontTrace
        return [c for c in cars if ActiveSilverCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return len(c._Waypoints) != 0

    def move(self):
        self.Position = Vector3(self.Position.X - self.Velocity.X, self.Position.Y + self.Velocity.Y,
                                self.Position.Z + self.Velocity.Z)
        # logger.debug("[ActiveCar] {2}: Current velocity: {0}, New position {1}".format(self.Velocity, self.Position, self.ID))

        # End of ride
        if (self.Position.X <= self.FINAL_POSITION):
            self.stop()

    def stop(self):
        # logger.debug("[ActiveCar]: {0} stopping".format(self.ID))

        self.Color = randrange(7)

        self.Position.X = self.INITIAL_POSITION
        self.Position.Y = randrange(self.MAX_Y)
        self.Position.Z = 0

        self.Velocity.X = 0
        self.Velocity.Y = 0
        self.Velocity.Z = 0