from __future__ import absolute_import

import logging, sys, os
from pcc.subset import subset
#from pcc.parameterize import parameterize
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey
from pcc.join import join

#sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

#import carpedestrian
from datamodel.common.datamodel import Vector3, Vehicle
#Vehicle
import traceback
import numpy as np
import time

logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"


@pcc_set
class WPCar(Vehicle.Class()):
  #_ID = None
  #@primarykey(str)
  #def ID(self):
  #  return self._ID
  
  #@ID.setter
  #def ID(self, value):
  #  self._ID = value

  #_Position = Vector3(0, 0, 0)
  #@dimension(Vector3)
  #def Position(self):
  #  return self._Position

  #@Position.setter
  #def Position(self, value):
  #  self._Position = value

  #_Velocity = Vector3(0, 0, 0)
  #@dimension(Vector3)
  #def Velocity(self):
  #  return self._Velocity
  
  #@Velocity.setter
  #def Velocity(self, value):
  #  self._Velocity = value
  
  _IsAssigned = False
  @dimension(bool)
  def IsAssigned(self):
    return self._IsAssigned
  
  @IsAssigned.setter
  def IsAssigned(self, value):
    self._IsAssigned = value
  
  _Route = []
  @dimension(list)
  def Route(self):
    return self._Route
  
  @Route.setter
  def Route(self, value):
    self._Route = value
  
  _RouteSection = 0
  @dimension(int)
  def RouteSection(self):
    return self._RouteSection
  
  @RouteSection.setter
  def RouteSection(self, value):
    self._RouteSection = value
  
  _LastTickTime = time.time()
  @dimension(float)
  def LastTickTime(self):
    return self._LastTickTime
  
  @LastTickTime.setter
  def LastTickTime(self, value):
    self._LastTickTime = value
  
  _AccelMode = "Cruising"
  @dimension(float)
  def AccelMode(self):
    return self._AccelMode
  
  @AccelMode.setter
  def AccelMode(self, value):
    self._AccelMode = value
  
  def __init__(self, uid=None):
    #logger.debug("!!!!" )
    self.ID = uid
    self.LastTickTime = time.time()
    super(self.Class(), self).__init__()
    

def shorten_str( x, n=5 ):
    if isinstance( x, (list, tuple) ):
        return str( x[:n] )[:-1] + ( "]" if len(x)<=n else "...]" )
    x = str(x)
    return x[:n]  + ( "" if len(x)<=n else "..." )

@subset(WPCar)
class FreeWPCar(WPCar.Class()):
  @staticmethod
  def __query__(cars):
    return [c for c in cars if FreeWPCar.__predicate__(c)]

  @staticmethod
  def __predicate__(c):
    return c.IsAssigned == False

  def assign(self, route):
    logger.debug("[FreeWPCar]: {0} assign route {1}".format( self.ID, shorten_str(route) ) )
    self.Route = list(route)
    self.RouteSection = 0
    self.IsAssigned = True
    self.Position = Vector3( * route[0] )
    self.Velocity = Vector3( 0.0, 0.0, 0.0 )
    self.LastTickTime = time.time()
    self.AccelMode == "Cruising" 


def decode_v3(x):
    if isinstance( x, Vector3 ):
        return np.array( [ x.X, x.Y, x.Z ] ).astype(float)
    elif isinstance( x, (list, tuple) ):
        return np.array(x).astype(float)
    elif isinstance( x, np.ndarray):
        return x
    else:
        print type(x)
        assert 0

def diff( src, dst ):
    s, d = map( decode_v3, (src, dst) )
    return d-s

def scale_to_vector( scale, direction ):
    normalized = direction / np.sqrt( direction.dot( direction ) )
    return normalized * scale

def distance( src, dst ):
    src, dst = map( decode_v3, (src, dst) )
    v = diff( src, dst )
    return np.sqrt( v.dot( v ) )

def halfway( src, dst, progress ):
    #s = np.array( [ src.X, src.Y, src.Z ] ).astype(float)
    #d = np.array( [ dst.X, dst.Y, dst.Z ] ).astype(float)
    src, dst = map( decode_v3, (src, dst) )
    #assert( src != dst )
    print "         diff", diff(src, dst)
    print "         progress", progress
    print "         scale_to_vector", scale_to_vector( progress, diff(src, dst) )
    print "         prev", src
    print "         next", dst
    print "         pos", src + scale_to_vector( progress, diff(src, dst) )
    return src + scale_to_vector( progress, diff(src, dst) )

@subset(WPCar)
class AssignedWPCar(WPCar.Class()):
  @staticmethod
  def __query__(cars):
    return [c for c in cars if AssignedWPCar.__predicate__(c)]

  @staticmethod
  def __predicate__(c):
    return c.IsAssigned
  
  MAX_SPEED = 17.0      # 40 MPH = 17.88 meters/sec
  MAX_SPEEDUP = 1.3     # 3 MPH/sec = 2.68 meters/sec^2     
  MILD_SPEEDUP = 0.44    # 1 MPH/sec
  MAX_STOPPING = -2.6
  REG_STOPPING = -1.1
  MILD_STOPPING = -0.5
  FLOAT_MARGIN = 0.02
  
  def move(self):
    """
    """
    if self.RouteSection >= len(self.Route) - 1:
        logger.debug("[AssignedWPCar]: {0} arrive destination".format( self.ID ) )
        self.IsAssigned = False
        return
    print "="*40 + " move car({0}) ".format(self.ID) + "="*40
    route = self.Route
    now = self.RouteSection
    nxt = now + 1
    lastTick = self.LastTickTime
    thisTick = time.time()
    tdelta = thisTick - lastTick
    print "tdelta", tdelta
    
    # calculate velocity
    velocity = np.array( [ self.Velocity.X, self.Velocity.Y, self.Velocity.Z ] ).astype(float)
    velocity_scale = np.sqrt( velocity.dot( velocity ) )
    velocity_direction = diff( route[now], route[nxt] )
    print "Velocity", velocity, velocity_scale
    
    # decide acceleration
    if self.AccelMode == "Cruising": 
        ## based on speed limit
        if self.MAX_SPEED - velocity_scale >= 2.0 * self.MAX_SPEEDUP:   # if not within the range that can catchup to limit in 2 seconds, accel
            acceleration = self.MAX_SPEEDUP
        elif self.MAX_SPEED - velocity_scale >= self.FLOAT_MARGIN:  # approaching speed limit 
            acceleration = max( (self.MAX_SPEED - velocity_scale)*0.35, self.MILD_SPEEDUP )
        elif self.MAX_SPEED - velocity_scale >= -self.FLOAT_MARGIN:
            acceleration = 0
        else:
            acceleration = self.MILD_STOPPING
    elif self.AccelMode == "Slowdown": 
        acceleration = self.MILD_STOPPING
    elif self.AccelMode == "SuddenStop": 
        acceleration = self.MAX_STOPPING
    
    # calcuate new velocity and displacement
    displacement = 0
    new_velocity = max( velocity_scale + acceleration * tdelta, 0.0 )
    print "v old and new", velocity_scale, new_velocity
    displacement = (new_velocity + velocity_scale) * tdelta / 2.0
    print "displacement", displacement
    velocity_scale = new_velocity
    
    # exhaust displacement    
    _disp = 0.0
    _pos = self.Position #np.array( [ self.Position.X, self.Position.Y ] ).astype(float)
    print "Position", [ _pos.X, _pos.Y, _pos.Z ]
    for nxt in range( nxt, len(route) ):
        dist = distance ( _pos, route[ nxt ] )
        print "    now", now
        print "    dist", dist
        velocity_direction = diff( route[now], route[nxt] )
        if _disp + dist >= displacement + self.FLOAT_MARGIN:   # I am not moving that far
            lastpart = displacement - _disp
            print "    I am not moving that far, lastpart =", lastpart
            _pos = halfway( _pos, route[nxt], lastpart )
            break
        
        now = nxt
        _pos = route[now]
        if _disp + dist >= displacement - self.FLOAT_MARGIN:   # just there!!
            print "    just there!!"
            break
        
        print "    not even close!"
        _disp += dist                               # move on to next section
    else: # arrive destination
        assert( now == nxt )
        #_pos = route[now]
    
    # update 
    self.Position = _pos if isinstance(_pos, Vector3) else Vector3( *_pos )
    self.RouteSection = now
    self.Velocity = Vector3( *scale_to_vector( velocity_scale, velocity_direction ) )
    self.LastTickTime = thisTick    
    """
    v = np.array( [ self.Velocity.X, self.Velocity.Y ] ).astype(float)
    v0 = np.sqrt( v.dot( v ) )
    if v0 > 0.01:
        v /= v0
        if v0 <= 3.0:
            v0 = min( 3.0, v0 + 0.3 )
    else:
        #print self.Route[ nxt ]
        #print self.Route[ nxt ].X
        v = np.array( self.Route[ nxt ][:2] ).astype(float) - np.array( [ self.Position.X, self.Position.Y ] ).astype(float)
        v /= np.sqrt( v.dot( v ) )
        v0 = 1.0
    
    #self.Velocity.X, self.Velocity.Y = v * v0
    
    ori = np.array([0.1,0.1])
    disp = v0
    while disp >= 0.1:
        a = np.array( [ self.Position.X, self.Position.Y ] ).astype(float)
        b = np.array( self.Route[ nxt ][:2] ).astype(float)
        ori = b - a
        d = np.sqrt( ori.dot( ori ) )
        if d > disp + 0.1:
            a += (b-a)/d*disp
            self.Position.X, self.Position.Y = a
            break
        elif d > disp - 0.1:
            self.RouteSection += 1
            self.Position.X, self.Position.Y = self.Route[ nxt ][:2]
            break
        else:
            self.Position.X, self.Position.Y = self.Route[ nxt ][:2]
            self.RouteSection += 1
            nxt += 1
            if nxt == len(self.Route):
                break
    ori /= np.sqrt( ori.dot( ori ) )
    ori *= v0
    self.Position = Vector3( self.Position.X, self.Position.Y, self.Position.Z )
    self.Velocity = Vector3( ori[0], ori[1], 0.0 )
    logger.debug( "AssignedWPCar {0}".format( self.ID ) ) 
    logger.debug( "Position {0}".format( self.Position ) ) 
    logger.debug( "Velocity {0}".format( self.Velocity ) ) 
    logger.debug( "RouteSection {0}".format( self.RouteSection ) ) 
    """
    """
    self.RouteSection += 1
    if self.RouteSection == len(self.Route):
        logger.debug("[AssignedWPCar]: {0} arrive destination".format( self.ID ) )
        self.IsAssigned = False
    else:
        logger.debug("[AssignedWPCar]: {0} move to WP{1}: {2}".format( self.ID, self.RouteSection, shorten_str(self.Route[self.RouteSection]) ) )
        self.Position = Vector3( * self.Route[self.RouteSection] )
    """

##@join(WPCar)
##class PotentialCollision(object):
##
##  @primarykey(str)
##  def ID(self):
##    return self._ID
##
##  @ID.setter
##  def ID(self, value):
##    self._ID = value
##
##  @dimension(WPCar)
##  def car(self):
##    return self._car
##  
##  @car.setter
##  def car(self, value):
##    self._car = value
##  
##  def __init__(self, c):
##    self.car = c
##
##  @staticmethod
##  def __query__(cars):
##    #return [PotentialCollision.Create(c) for c1 in cars for c2 in cars if CarAndPedestrianNearby.__predicate__(c1, c2)]
##    carlist = []
##    for c1 in cars:
##        for c2 in cars:
##            pass
##        if CarAndPedestrianNearby.__predicate__(c1, c2):
##            carlist.append(c1)
##    return [ PotentialCollision.Create(c) for c in carlist ]
##    #return #[PotentialCollision.Create(c) for c1 in cars for c2 in cars if CarAndPedestrianNearby.__predicate__(c1, c2)]
##  
##  @staticmethod
##  def __predicate__(c1, c2):
##    #if abs(c.Position.X - p.X) < 130 and c.Position.Y == p.Y:
##    #  return True
##    #return False
##    return c1.AccelMode == "Cruising"

