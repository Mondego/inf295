import logging
from datamodel.uberCar_Xi.datamodel import *
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter
from datamodel.common.datamodel import Vehicle
logger = logging.getLogger(__name__)
LOG_HEADER = "[TRAFFIC]"


@Producer(UberCar, host = 'http://ucigridb.nacs.uci.edu:12000')
@GetterSetter(InactiveUberCar, ActiveUberCar, CarAndCarInfront, Vehicle,
            host = 'http://ucigridb.nacs.uci.edu:12000')
class TrafficSimulation(IApplication):
    '''
  classdocs
  '''

    frame = None
    ticks = 0
    cars = []

    def __init__(self, frame):
        '''
    Constructor
    '''
        self.frame = frame

    def initialize(self):
        logger.debug("%s Initializing", LOG_HEADER)
        for i in xrange(2):
            self.frame.add(UberCar())
        # self.frame.add(Car("1d4883f3-b8f7-11e5-a78c-acbc327e1743")) # Valid uuid Example
        # self.frame.add(Car(10)) # Valid int Example
        # self.frame.add(Car("1d4883f3")) Invalid  Example - Crashes
        self.cars = self.frame.get(UberCar)

    def update(self):
        logger.info("%s %d Tick", LOG_HEADER, self.ticks)
        cars = self.frame.get(UberCar)
        activeCars = self.frame.get(ActiveUberCar)
        inActiveCars = self.frame.get(InactiveUberCar)
        #carInDanger = self.frame.get(CarInDanger)
        logger.info("total cars: %d", len(cars))
        logger.info("active cars: %d, inactive cars: %d", len(activeCars), len(inActiveCars))
        #logger.info("cars in danger: %d", len(carInDanger))
        #logger.info("car and car in front: %d", len(self.frame.get(CarAndCarInfront)))
        speedDict = {}
        for c in self.frame.get(CarAndCarInfront):
            vx = c.frontCar.Velocity.X
            vy = c.frontCar.Velocity.Y
            speedDict[c.car1.ID] = math.sqrt(vx * vx + vy * vy)

        for car in activeCars:
            if car.ID in speedDict:
                car.adjustSpeed(speedDict[car.ID])
            car.move()
            car.reportStatus()
        self.ticks += 1

    def shutdown(self):
        logger.info("traffic sim shut down")
        pass
