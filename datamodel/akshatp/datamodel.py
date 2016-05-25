'''
Created on Dec 15, 2015

@author: arthurvaladares
'''

from __future__ import absolute_import
import logging
from pcc.subset import subset
from pcc.set import pcc_set
from pcc.attributes import dimension
from pcc.parameter import parameter
import math
from sympy.geometry import *
from datamodel.common.datamodel import Vehicle, Vector3
import uuid

logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"

@pcc_set
class Car_akshatp(Vehicle.Class()):

    _Route = []

    @dimension(list)
    def Route(self):
        return self._Route

    @Route.setter
    def Route(self, value):
        self._Route = value

    @dimension(float)
    def RouteLength(self):
        if len(self._Route) > 1:
            l = 0
            for i in range(1, len(self._Route)):
                x1 = self._Route[i-1]['X']
                y1 = self._Route[i-1]['Y']
                x2 = self._Route[i]['X']
                y2 = self._Route[i]['Y']
                l += math.sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))
            return l
        else:
            return 0

    @RouteLength.setter
    def RouteLength(self, RouteLength):
        pass

    @dimension(list)
    def CarRotatedBox(self):
        p = self.Position
        prevp = self.PrevPosition

        cangle = complex(prevp.X - p.X, prevp.Y - p.Y)
        cangle = 0 if abs(cangle) == 0 else (cangle / abs(cangle))

        center = complex(p.X, p.Y)

        x1 = p.X - self.Length / 2
        y1 = p.Y - self.Width / 2
        x2 = p.X + self.Length / 2
        y2 = p.Y - self.Width / 2
        x3 = p.X + self.Length / 2
        y3 = p.Y + self.Width / 2
        x4 = p.X - self.Length / 2
        y4 = p.Y + self.Width / 2

        xy1 = cangle * (complex(x1, y1) - center) + center
        xy2 = cangle * (complex(x2, y2) - center) + center
        xy3 = cangle * (complex(x3, y3) - center) + center
        xy4 = cangle * (complex(x4, y4) - center) + center

        return [xy1.real, xy1.imag, xy2.real, xy2.imag, xy3.real, xy3.imag, xy4.real, xy4.imag]

    @CarRotatedBox.setter
    def CarRotatedBox(self, CarBox):
        pass

    @dimension(list)
    def CarRotatedHitBox(self):
        p = self.Position
        prevp = self.PrevPosition

        cangle = complex(prevp.X - p.X, prevp.Y - p.Y)
        cangle = 0 if abs(cangle) == 0 else (cangle / abs(cangle))

        center = complex(p.X, p.Y)

        hx1 = p.X - self.Length / 2 - self.Velocity.X * 4
        hy1 = p.Y - self.Width / 2 - self.Width / 2

        hx2 = p.X - self.Length / 2
        hy2 = p.Y - self.Width / 2 - self.Width / 2

        hx3 = p.X - self.Length / 2
        hy3 = p.Y + self.Width / 2 + self.Width / 2

        hx4 = p.X - self.Length / 2 - self.Velocity.X * 4
        hy4 = p.Y + self.Width / 2 + self.Width / 2

        hxy1 = cangle * (complex(hx1, hy1) - center) + center
        hxy2 = cangle * (complex(hx2, hy2) - center) + center
        hxy3 = cangle * (complex(hx3, hy3) - center) + center
        hxy4 = cangle * (complex(hx4, hy4) - center) + center

        return [hxy1.real, hxy1.imag, hxy2.real, hxy2.imag, hxy3.real, hxy3.imag, hxy4.real, hxy4.imag]

    @CarRotatedHitBox.setter
    def CarRotatedHitBox(self, CarBox):
        pass

    _CurrentRoute = 0

    @dimension(int)
    def CurrentRoute(self):
        return self._CurrentRoute

    @CurrentRoute.setter
    def CurrentRoute(self, value):
        self._CurrentRoute = value

    _PrevPosition = Vector3(0, 0, 0)

    @dimension(Vector3)
    def PrevPosition(self):
        return self._PrevPosition

    @PrevPosition.setter
    def PrevPosition(self, value):
        self._PrevPosition = value

    _TopSpeed = 0

    @dimension(int)
    def TopSpeed(self):
        return self._TopSpeed

    @TopSpeed.setter
    def TopSpeed(self, value):
        self._TopSpeed = value

    def __init__(self):
        self.ID = str(uuid.uuid4())
        self.Position = Vector3(0, 0, 40.5)
        self.Velocity = Vector3(0, 0, 0)
        self.Length = 0
        self.Width = 0
        self.Name = ""


@subset(Car_akshatp)
class InactiveCar_akshatp(Car_akshatp.Class()):
    @staticmethod
    def __query__(cars):
        return [c for c in cars if InactiveCar_akshatp.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return len(c.Route) == 0

    def start(self, route=[], v=10):
        self.TopSpeed = v
        self.Velocity = Vector3(v,0,0)
        self.Route = route

        r = route
        l = len(r)
        cr = 1
        p = self.Position
        if l > cr > 0 and v > 0:
            lastx = r[l-1]['X']
            lasty = r[l-1]['Y']
            if not (p.X == lastx and p.Y == lasty):
                currx = p.X
                curry = p.Y
                routeendx = r[cr]['X']
                routeendy = r[cr]['Y']
                dist = math.sqrt(((routeendx-currx)*(routeendx-currx))+((routeendy-curry)*(routeendy-curry)))
                if dist != 0:
                    finalx = currx + (v / dist) * (routeendx - currx)
                    finaly = curry + (v / dist) * (routeendy - curry)
                    finaldist = math.sqrt(((finalx-currx)*(finalx-currx))+((finaly-curry)*(finaly-curry)))
                    if finaldist <= dist:
                        if not (p.X == self.PrevPosition.X and p.Y == self.PrevPosition.Y and p.Z == self.PrevPosition.Z):
                            self.PrevPosition = Vector3(p.X, p.Y, p.Z)
                        self.Position = Vector3(finalx, finaly, p.Z)
                    else:
                        if not (p.X == self.PrevPosition.X and p.Y == self.PrevPosition.Y and p.Z == self.PrevPosition.Z):
                            self.PrevPosition = Vector3(p.X, p.Y, p.Z)
                        self.Position = Vector3(routeendx, routeendy, p.Z)
                        self.CurrentRoute += 1

@subset(Car_akshatp)
class ActiveCar_akshatp(Car_akshatp.Class()):
    @staticmethod
    def __query__(cars):
        lst = [c for c in cars if ActiveCar_akshatp.__predicate__(c)]
        return lst

    @staticmethod
    def __predicate__(c):
        return len(c.Route) > 0

    def move(self):
        r = self.Route
        l = len(r)
        cr = self.CurrentRoute
        p = self.Position
        v = self.Velocity

        if l > cr > 0 and v > 0:
            lastx = r[l-1]['X']
            lasty = r[l-1]['Y']
            if p.X == lastx and p.Y == lasty:
                self.stop()
            else:
                currx = p.X
                curry = p.Y
                routeendx = r[cr]['X']
                routeendy = r[cr]['Y']
                dist = math.sqrt(((routeendx - currx) * (routeendx - currx)) + ((routeendy - curry) * (routeendy - curry)))
                if dist != 0:
                    finalx = currx + (v / dist) * (routeendx - currx)
                    finaly = curry + (v / dist) * (routeendy - curry)
                    finaldist = math.sqrt(((finalx - currx) * (finalx - currx)) + ((finaly - curry) * (finaly - curry)))
                    if finaldist < dist:
                        if not (p.X == self.PrevPosition.X and p.Y == self.PrevPosition.Y and p.Z == self.PrevPosition.Z):
                            self.PrevPosition = Vector3(p.X, p.Y, p.Z)
                        self.Position = Vector3(finalx, finaly, p.Z)
                    else:
                        if not (p.X == self.PrevPosition.X and p.Y == self.PrevPosition.Y and p.Z == self.PrevPosition.Z):
                            self.PrevPosition = Vector3(p.X, p.Y, p.Z)
                        self.Position = Vector3(routeendx, routeendy, p.Z)
                        self.CurrentRoute += 1
        if v < self.TopSpeed:
            self.Velocity = Vector3(min(v + (0.3*self.TopSpeed), self.TopSpeed),0,0)

    def stop(self):
        self.Velocity = Vector3(0,0,0)
        self.TopSpeed = 0
        self.Position = Vector3(0, 0, 0)
        self.PrevPosition = Vector3(0, 0, 0)
        self.CurrentRoute = 0
        self.Route = []


@parameter(Car_akshatp)
@subset(Car_akshatp)
class CarAndCarNearby_akshatp(Car_akshatp.Class()):

    @staticmethod
    def __query__(cars, cars_in_danger):
        c = []
        for c1 in cars:
            for c2 in cars_in_danger:
                if CarAndCarNearby_akshatp.__predicate__(c1, c2):
                    c.append(c1)
        return c

    @staticmethod
    def __predicate__(c1, c2):
        if c1.Route != [] and c1.ID != c2.ID:
            m = list(map(round, c1.CarRotatedHitBox))
            n = list(map(round, c2.CarRotatedBox))
            a = Polygon((m[0], m[1]), (m[2], m[3]), (m[4], m[5]), (m[6], m[7]))
            b = Polygon((n[0], n[1]), (n[2], n[3]), (n[4], n[5]), (n[6], n[7]))
            if a.intersection(b) != []:
                return True
        return False

    def slowDown(self):
        self.Velocity = Vector3(0,0,0)

