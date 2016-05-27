'''
Created on May 10, 2016

@author: Jilin Liu
'''

import logging
import math, sys, os

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from pcc.join import join
from pcc.subset import subset
from pcc.parameter import  parameter
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey
from datamodel.nodesim.datamodel import Waypoint
from datamodel.common.datamodel import Vehicle, Vector3, Color

import traceback


logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"

@pcc_set
class LockPart2TheRevenge(Vehicle.Class()):
  apple = "banana"

@pcc_set
class AmazonCar(Vehicle.Class()):
  '''
  classdocs
  '''

  _Aflag = True
  Bananas = "Awesome"
  Kale = "Not cool"
  @dimension(bool)
  def Aflag(self):
    return self._Aflag

  @Aflag.setter
  def Aflag(self, value):
    self._Aflag = value

  def becomeAmazonCar(self):
    self.Aflag = True

  def __init__(self, uid=None):
    self.ID = uid
    self.Position = Vector3(0, 0, 0)
    self.Velocity = Vector3(0, 0, 0)
    self.Length = 0
    self.Width = 0
    self.Name = ""
    self.Aflag = True
    self.Waypoints = []

  @dimension(list)
  def Waypoints(self):
    return self._Waypoints

  @Waypoints.setter
  def Waypoints(self, value):
    self._Waypoints = value

# Amazon Inactive
@subset(AmazonCar)
class AmazonInactiveCar(AmazonCar):
    @staticmethod
    def __query__(cars):
        return [c for c in cars if AmazonInactiveCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Aflag == True and c.Velocity == Vector3(0,0,0)

    def start(self):
      logger.debug("[AmazonInactiveCar]: {0} starting".format(self.ID))
      self.Velocity = Vector3(self.SPEED, 0, 0)

# Amazon InactiveCar
@subset(AmazonCar)
class AmazonActiveCar(AmazonCar):
  @staticmethod
  def __query__(cars):  # @DontTrace
    return [c for c in cars if AmazonActiveCar.__predicate__(c)]

  @staticmethod
  def __predicate__(c):
    return c.Velocity != Vector3(0, 0, 0) and c.Aflag

  def move(self, node1, node2):
        # by Jilin, based on road line from node1(x1, y1) to node2(x2, y2): y = ax + b,
        a = (node2[1] - node1[1])/(node2[0] - node1[0])
        b = 1
        alpha = 1.0/50  # type int and float
        if node2[0] > node1[0]:
          newPositionX = self.Position.X + alpha * self.SPEED / math.sqrt(pow(a, 2) + 1)
          if newPositionX > node2[0]:
            newPositionX = node2[0]
        elif node2[0] < node1[0]:
          newPositionX = self.Position.X - alpha * self.SPEED/ math.sqrt(pow(a, 2) + 1)
          if newPositionX < node2[0]:
            newPositionX = node2[0]
        else:
          newPositionX = self.Position.X

        if node2[1] > node1[1]:
          newPositionY = self.Position.Y + abs(a) * alpha * self.SPEED / math.sqrt(pow(a, 2) + 1)
          if newPositionY > node2[1]:
            newPositionY = node2[1]
        elif node2[1] < node1[1]:
          newPositionY = self.Position.Y - abs(a) * alpha * self.SPEED / math.sqrt(pow(a, 2) + 1)
          if newPositionY < node2[1]:
            newPositionY = node2[1]
        else:
            newPositionY = self.Position.Y

        self.Position = Vector3(newPositionX, newPositionY, 0)
        # logger.debug("[ActiveCar] {2}: Current velocity: {0}, New position {1}".format(self.Velocity, self.Position, self.ID))

        # End of ride
        if (self.Position.X >= self.FINAL_POSITION) or (self.Position.Y >= self.FINAL_POSITION):
            self.stop()


  def stop(self):
      logger.debug("[AmazonActiveCar]: {0} stopping".format(self.ID))
      self.Position.X = 0
      self.Position.Y = 0
      self.Position.Z = 0
      self.Velocity.X = 0
      self.Velocity.Y = 0
      self.Velocity.Z = 0
