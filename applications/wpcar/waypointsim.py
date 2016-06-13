import logging
#from datamodel.carpedestrian.datamodel import Car, InactiveCar, ActiveCar, WPCar, FreeWPCar, AssignedWPCar
from datamodel.wpcar.datamodel import WPCar, FreeWPCar, AssignedWPCar #PotentialCollision
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter, Tracker, Deleter
from datamodel.nodesim.datamodel import RouteRequest, Route, Waypoint,\
    ResidentialNode, BusinessNode
import numpy, sys

logger = logging.getLogger(__name__)
LOG_HEADER = "[WaypointCarSimulation]"

#wplists = []
#for f in [ "car-4.rd", "bus-1.rd" ]:
#    wplists.append( [ map(float, line.strip().split(',') ) for line in open(f) if line.strip() ] )

#special_route = [(196.40276109834082, 465.4137457493732, 40.5), (231.40814589831396, 446.6660627096663, 40.5), 
#    (319.6804322263649, 567.9599691529883, 40.5), (332.7463866541471, 566.7175310440763, 40.5), (357.6218399826585, 555.2794908288894, 40.5), 
#    (516.9829544193801, 472.8642898994031, 40.5), (530.7053616249941, 465.020779695333, 40.5), (539.112519352173, 455.12242307587417, 40.5), 
#    (550.978694559537, 446.0007404014163, 40.5), (561.1610181137489, 444.68901845879697, 40.5), (600.5, 464.45355, 40.5), 
#    (612.5, 470.45295000000004, 40.5), (620.5, 477.45225, 40.5), (622.0, 486.45135, 40.5), (534.0, 700.4299500000001, 40.5), 
#    (519.0, 739.926, 40.5), (510.0, 766.42335, 40.5), (496.0, 811.9188, 40.5), (427.0, 1066.39335, 40.5), (429.0, 1077.39225, 40.5), 
#    (436.0, 1082.8917000000001, 40.5), (461.0, 1091.39085, 40.5), (468.5, 1096.3903500000001, 40.5), (471.5, 1103.8896, 40.5), 
#    (471.5, 1112.8887, 40.5), (468.5, 1132.3867500000001, 40.5), (456.0, 1195.38045, 40.5), (445.0, 1252.37475, 40.5), 
#    (438.0, 1285.37145, 40.5), (432.5, 1292.37075, 40.5), (424.0, 1295.3704500000001, 40.5)]
special_route = [(583.0, 544.0, 42.5), (560.0, 603.0, 42.5)]
#special_route = [ (364.0, 505.0, 42.5), (386.0, 401.0, 42.5) ]
import random

#@Producer(RouteRequest)
#@GetterSetter(RouteRequest, Route)
#@Tracker(Route, Waypoint, ResidentialNode, BusinessNode)
#@Deleter(Route)

@Producer(WPCar, RouteRequest, host="http://ucigridb.nacs.uci.edu:12000/")
#@Producer(RouteRequest)#, WPCar)
#@GetterSetter(FreeWPCar, AssignedWPCar, host="http://ucigridb.nacs.uci.edu:12000/")
@GetterSetter(RouteRequest, Route, FreeWPCar, AssignedWPCar, host="http://ucigridb.nacs.uci.edu:12000/")
@Tracker(Route, Waypoint, ResidentialNode, BusinessNode, host="http://ucigridb.nacs.uci.edu:12000/")
#@Deleter(WPCar, host="http://ucigridb.nacs.uci.edu:12000/")
@Deleter(Route, WPCar, host="http://ucigridb.nacs.uci.edu:12000/")
class WaypointCarSimulation(IApplication):
  frame = None
  cars = []
  ticks = 0
  INTERVAL_START_FREE_CAR = 2
  INTERVAL_ADD_CAR = 3
  MAX_CAR = 300
  def __init__(self, frame):
    self.frame = frame
  
  def initialize(self):
    logger.debug("%s Initializing", LOG_HEADER)
    #print len(self.frame.get(WPCar))
    #print len(self.frame.get(FreeWPCar))
    #print len(self.frame.get(AssignedWPCar))
    for car in self.frame.get(WPCar):
        self.frame.delete(WPCar, car)
    for i in xrange(1):
        car = WPCar()
        self.frame.add(car)   # init WPCar??
    self.cars = self.frame.get(WPCar)
    print len(self.cars)
    self.num_car = 0
    #for car in self.cars:
    #    car.IsAssigned = False
    #print "!!!"
  
  def update(self):
    logger.info("{0} update: tick #{1}".format( LOG_HEADER, self.ticks ) )
    
    '''if self.ticks % self.INTERVAL_ADD_CAR == 0:
        if self.num_car < self.MAX_CAR:
            self.num_car += 1
            n = len(self.frame.get(FreeWPCar)) + len(self.frame.get(AssignedWPCar))
            logger.info("    add {0} more car(s) ".format( self.num_car - n ) )
            for i in xrange( self.num_car - n ):
                car = WPCar( str(n + i + 31415000) )
                self.frame.add(car)   # init WPCar??'''
    
    if self.ticks % self.INTERVAL_START_FREE_CAR == 0:
      try:
        free = self.frame.get(FreeWPCar)
        logger.debug("%s ************** FreeWPCar: %s", LOG_HEADER, len(free))
        if free != None and len(free) > 0:
          #logger.debug("%s ************** Starting car %s", LOG_HEADER, inactives[0].ID)
          #inactives[0].start();
          
          # assign startpoint, destination, wplist for free[0]
          #wp = random.sample( wplists, 1 )[0]
          #req = RouteRequest()
          #req.Owner = "WaypointCarSimulation"
          #req.Source = None # Picks a random source waypoint
          #req.Destination = None # Picks a random destination waypoint
          #req.Name = "Random"
          #self.frame.add(req)
          #wp = wplists[ int( random.random()*2 ) ]
          #free[0].assign( [ (x,y,40.0) for x,y in wp ] )
          #logger.debug("Assign car with route: {0}".format(wp) )
          # free[0].start()
          pass

      except Exception:
        logger.exception("Error: ")
    
    routes = self.frame.get_new(Route)
    logger.debug( "len(routes) {0}".format(len(routes)) )
    if len(routes) < 0:
        free = self.frame.get(FreeWPCar)
        #logger.debug("%s ************** FreeWPCar: %s", LOG_HEADER, len(free))
        if free != None and len(free) > 0:
            #wp = special_route
            #free[0].Name = "WPCar"
            #free[0].assign( wp ) #[ (w['X'], w['Y'],40.5) for w in rt.Waypoints ] )
            for rt in routes:
                if rt.Owner == "WaypointCarSimulation":
                    logger.info("[%s]: %s", rt.Name, rt.Waypoints)
                    #wp = wplists[ int( random.random()*2 ) ]
                    #print len( rt.Waypoints )
                    wp = [ (w['X'], w['Y'],40.5) for w in rt.Waypoints ]
                    #wp = special_route
                    #wp = wplists[ int( random.random()*2 ) ]
                    #wp = [ (w['X'], w['Y'],45.0) for w in wp ]
                    logger.debug("Assign car with route: {0}".format(wp) )
                    if len(wp)==0:
                        continue
                    free[0].assign( wp ) #[ (w['X'], w['Y'],40.5) for w in rt.Waypoints ] )
                    #free[0].assign( [ (430.0, 310.0, 44.0), (440.0, 310.0, 44.0) ] )
                    print "old name", free[0].Name
                    free[0].Name = "WPCar"
                    self.frame.delete(Route, rt)
    
    free = self.frame.get(FreeWPCar)
    logger.debug("%s ************** FreeWPCar: %s", LOG_HEADER, len(free))
    if free != None and len(free) > 0:
        wp = special_route
        #free[0].Name = "WPCar"
        free[0].assign( wp ) #[ (w['X'], w['Y'],40.5) for w in rt.Waypoints ] )
    for car in self.frame.get(AssignedWPCar):
      #car.IsAssigned = False
      #break
      _pos = car.Position #np.array( [ self.Position.X, self.Position.Y ] ).astype(float)
      print >> sys.stderr, car.Name
      print >> sys.stderr, "Position", [ _pos.X, _pos.Y, _pos.Z ]
      car.move()
      logger.debug("Car.move: ")
    #for car in self.frame.get(PotentialCollision):
    #    logger.debug( "PotentialCollision: {0}".format( car.car.ID ) )
    self.ticks += 1
  
  def shutdown(self):
    pass

