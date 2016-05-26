from __future__ import absolute_import
import traceback
import logging
import math
from pcc.subset import subset
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey
from pcc.parameter import parameter
from pcc.join import join
from datamodel.common.datamodel import Vector3, Vehicle

logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"

@pcc_set
class UberCar(Vehicle.Class()):

    _Speed = 20
    @dimension(float)
    def Speed(self):
        return self._Speed
    @Speed.setter
    def Speed(self, value):
        self._Speed = value

    _Route = None

    @dimension(list)
    def Route(self):
        return self._Route

    @Route.setter
    def Route(self, value):
        self._Route = value

    _NextNodeIdx = 0

    @dimension(int)
    def NextNodeIdx(self):
        return self._NextNodeIdx

    @NextNodeIdx.setter
    def NextNodeIdx(self, idx):
        self._NextNodeIdx = idx

    def adjustSpeed(self, newSpeed):
        self.Velocity.X = self.Velocity.X / self.Speed * newSpeed
        self.Velocity.Y = self.Velocity.Y / self.Speed * newSpeed
        self.Speed = newSpeed

    def __init__(self, uid=None):
        self.ID = uid
        self.Velocity = Vector3(0, 0, 0)
        self.Name = "uberCar"
        self.Position = Vector3(0, 0, 40.5)
        self.Velocity = Vector3(0, 0, 0)
        self.Length = 10
        self.Width = 10


@subset(UberCar)
class InactiveUberCar(UberCar.Class()):
    @staticmethod
    def __query__(cars):
        return [c for c in cars if InactiveUberCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Velocity == Vector3(0, 0, 0)

    def start(self, route):
        self.Route = route

        dx = route[1][0] - route[0][0]
        dy = route[1][1] - route[0][1]
        if dx == 0 and dy == 0:
            dx = route[2][0] - route[1][0]
            dy = route[2][1] - route[1][1]
            self.NextNodeIdx += 1
        dis = math.sqrt(dx * dx + dy * dy)
        self.Velocity = Vector3(dx / dis * self.Speed, dy / dis * self.Speed, 0)
        self.Position = Vector3(route[0][0], route[0][1], 40.5)
        self.NextNodeIdx += 1
        logger.info("[InactiveCar]: {0} starting".format(self.ID))
        logger.info("velocity: ")
        logger.info(self.Velocity)


@subset(UberCar)
class ActiveUberCar(UberCar.Class()):
    @staticmethod
    def __query__(cars):  # @DontTrace
        return [c for c in cars if ActiveUberCar.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Velocity != Vector3(0, 0, 0)

    def move(self):
        logger.info("[ActiveCar]: move car {0}".format(self.ID))
        logger.info("   Route Length: " + str(len(self.Route)) + "   Next node: " + str(self.NextNodeIdx))
        self.Position = Vector3(self.Position.X + self.Velocity.X, self.Position.Y + self.Velocity.Y,
                                self.Position.Z + self.Velocity.Z)

        if (self.Position.X >= self.Route[self.NextNodeIdx-1][0] and self.Position.X >= self.Route[self.NextNodeIdx][0]) or (self.Position.X < self.Route[self.NextNodeIdx-1][0] and self.Position.X < self.Route[self.NextNodeIdx][0]):
            self.Position = Vector3(self.Route[self.NextNodeIdx][0], self.Route[self.NextNodeIdx][1], 40.5)
            if self.NextNodeIdx + 1 == len(self.Route):
                self.stop()
            else:
                self.NextNodeIdx += 1
                dx = self.Route[self.NextNodeIdx][0] - self.Route[self.NextNodeIdx-1][0]
                dy = self.Route[self.NextNodeIdx][1] - self.Route[self.NextNodeIdx-1][1]
                dis = math.sqrt(dx * dx + dy * dy)
                self.Velocity = Vector3(dx / dis * self.Speed, dy / dis * self.Speed, 0)

        logger.debug("[ActiveCar]: Current velocity: {0}, New position {1}".format(self.Velocity, self.Position));

    def stop(self):
        logger.debug("[ActiveCar]: {0} stopping!!!!!!!!!!!!!!!!!!!!!!!!".format(self.ID))
        self.Velocity = Vector3(0, 0, 0)
        self.NextNodeIdx = 0

    def reportStatus(self):
        logger.debug("[ActiveCar]: {0} speed: ".format(self.ID) + str(self.Speed))

'''
@parameter(UberCar)
@subset(UberCar)
class CarInDanger(UberCar.Class()):
    def distance(self, p1, p2):
        dx = p1.X - p2.X
        dy = p1.Y - p2.Y
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def __query__(cars1, cars2):
        return [c for c in cars1 if CarInDanger.__predicate__(c, cars2)]

    @staticmethod
    def __predicate__(p, cars):
        return False

    def move(self):
        logger.debug("[Car]: {0} avoiding collision!".format(self.ID));
'''

@join(UberCar, Vehicle)
class CarAndCarInfront(object):

    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @dimension(UberCar)
    def car1(self):
        return self._car1

    @car1.setter
    def car1(self, value):
        self._car1 = value

    @dimension(Vehicle)
    def frontCar(self):
        return self._frontCar
    @frontCar.setter
    def frontCar(self, value):
        self._frontCar = value

    def __init__(self, car1, frontCar):
        self.car1 = car1
        self.frontCar = frontCar

    @staticmethod
    def __query__(cars1, cars2):
        return [(c1, c2) for c1 in cars1 for c2 in cars2 if CarAndCarInfront.__predicate__(c1, c2)]

    # if c2 is in front of c1, and the distance < 100, and speed of c2 is less than c1, return true
    @staticmethod
    def __predicate__(c1, c2):
        dx = c2.Position.X - c1.Position.X
        dy = c2.Position.Y - c1.Position.Y
        dis = math.sqrt(dx * dx + dy * dy)
        vx = c1.Velocity.X
        vy = c1.Velocity.Y
        if dis == 0:
            return False
        if c1.Velocity == Vector3(0, 0, 0):
            return False
        cosTheta = (dx * vx + dy * vy)/(math.sqrt(dx*dx+dy*dy) * math.sqrt(vx*vx+vy*vy))
        if cosTheta > 0.9 and dis < 10:
            return True
        return False

    def reportStatus(self):
        logger.debug("[Car]: {0} follow the speed of the front car!".format(self.ID));
        logger.debug("this car: {0}".format(self.car1.ID))
        logger.debug("speed: " + str(self.car1.Speed))
        logger.debug("front car: {0}".format(self.frontCar.ID))
        logger.debug("speed2: " + str(self.frontCar.Speed))



