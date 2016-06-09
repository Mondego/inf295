'''
Created on Dec 15, 2015

@author: arthurvaladares
'''
from __future__ import absolute_import
import logging
import os
import math
import sys



from pcc.join import join
from pcc.subset import subset
#from pcc.parameterize import parameterize
from pcc.parameter import parameter
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey
from datamodel.common.datamodel import Vehicle, Vector3


from sympy.geometry import *

#from spacetime_local.frame import frame

import traceback


logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"
class Color:
    Red = 0
    Green = 1
    Blue = 2
    Yellow = 3
    Black = 4
    White = 5
    Grey = 6

#Vector3 = namedtuple("Vector3", ['X', 'Y', 'Z'])
class Vector3(object):
    X = 0
    Y = 0
    Z = 0

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def __json__(self):
        return self.__dict__

    def __str__(self):
        return self.__dict__.__str__()

    def __eq__(self, other):
        return (isinstance(other, Vector3) and (other.X == self.X and other.Y == self.Y and other.Z == self.Z))

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def __decode__(dic):
        return Vector3(dic['X'], dic['Y'], dic['Z'])

@pcc_set
class Car_teja(Vehicle.Class()):
    '''
    classdocs
    '''
    #SPEED = 4; # move 4 units for tick
    
    _ID = None
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    _Position = Vector3(0, 0, 0)
    @dimension(Vector3)
    def Position(self):
        return self._Position

    @Position.setter
    def Position(self, value):
        self._Position = value

    _Velocity = 0# changed velocity to number of units to move per tick Vector3(0, 0, 0)
    @dimension(int)
    def Velocity(self):
        return self._Velocity

    @Velocity.setter
    def Velocity(self, value):
        self._Velocity = value

    _Color = Color.White
    @dimension(Color)
    def Color(self):
        return self._Color

    @Color.setter
    def Color(self, value):
        self._Color = value

    _Length = 0
    @dimension(int)
    def Length(self):
        return self._Length

    @Length.setter
    def Length(self, value):
        self._Length = value

    _Width = 0
    @dimension(int)
    def Width(self):
        return self._Width

    @Width.setter
    def Width(self, value):
        self._Width = value

    

    #teja start   
    
    _Lines = None
    @dimension(list)
    def Lines(self):
        return self._Lines
    
    @Lines.setter
    def Lines(self,value):   
        self._Lines = value;

    _FINAL_POSITION = 0
    @dimension(int)
    def FINAL_POSITION(self):
        return self._FINAL_POSITION;

    @FINAL_POSITION.setter
    def FINAL_POSITION(self,value):
        self._FINAL_POSITION=value;
    
    _CurrentSourceIndex=0
    @dimension(int)
    def CurrentSourceIndex(self):
        return self._CurrentSourceIndex

    @CurrentSourceIndex.setter
    def CurrentSourceIndex(self,value):
        self._CurrentSourceIndex = value
    
    #teja end

    #def __init__(self, uid=None):
    def __init__(self, uid=None):
        self.ID = uid
        self.Length = 30;
        self._Velocity = 0;# car at start is zero speed

    def setRoute(self,route=[]):
        try:
            path_data = os.path.dirname(os.path.realpath(__file__))
            #trying to initialize this in client side using route request.
            self.Lines = [line.rstrip('\n') for line in open(os.path.join(path_data,'package/car-4.rd'))];
            #self.Lines = route.Waypoints
            self.Lines = [];
            for value in route.Waypoints:
                t = (value['X'],value['Y']);
                self.Lines.append(t);

            self.CurrentSourceIndex =0;
            #a,b,c =str(self.Lines[0]).split(',');
            #i,a= a.split(':');
            #i,b= b.split(':');
            temp = self.Lines[0];
            self.Position.X = temp[0];
            self.Position.Y = temp[1];

            temp = self.Lines[len(self.Lines) - 1];
            temp1 = temp[0];
            temp2 = temp[1];
            self.FINAL_POSITION = [temp1,temp2]
            print(self.Lines[0]);

            temp = self.Lines[0];
            x,y = temp[0],temp[1];
            print x;
            print y; 
        except :
            print(ex.message);


    def slope(self):
        a,b=str(self.Lines[self.CurrentSourceIndex]).split(',');
        x1 = float(a)
        y1=  float(b)
        a,b=str(self.Lines[self.CurrentSourceIndex +1]).split(',');
        x2 = float(a)
        y2=  float(b)
        return ( (y2-y1)/(x2-x1));#not handling perpendicular line
        

    def toadd(self,m):
        return float(self.Velocity/math.sqrt(1+m*m));

@subset(Car_teja)
#class InactiveCar_teja(Car_teja):
class InactiveCar_teja(Car_teja.Class()):
    @staticmethod
    def __query__(cars):
        return [c for c in cars if InactiveCar_teja.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        #return c.Position == Vector3(0,0,0)
        return c.Velocity == 0 
      

    #def start(self):
    #    logger.debug("[InactiveCar_teja]: {0} starting".format(self.ID))
    #    self.Velocity = 4;#SPEED

    def start(self,i):
        logger.debug("[InactiveCar_teja]: {0} starting".format(self.ID))
        self.Velocity = i*4;#SPEED setting speed equal to index * 4 
        
@subset(Car_teja)
#class ActiveCar_teja(Car_teja):
class ActiveCar_teja(Car_teja.Class()):
    @staticmethod
    def __query__(cars):  # @DontTrace
        return [c for c in cars if ActiveCar_teja.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.Velocity !=0# Vector3(0,0,0)
        

    def move(self):

        #temp fix inactive carstar failing
        #self.Velocity = 4;#SPEED
        #get what current index is      
       

        # End of ride -- if source index is dest
        print("\n"+str(self.CurrentSourceIndex))
        print("\n"+str(len(self.Lines) - 1)+"\n\n\n")
        if (self.CurrentSourceIndex == (len(self.Lines) - 1)):            
            self.stop();
            return;

        m = self.slope();
        k = self.toadd(m);
       
         #update positions based on formulas
        self.Position = Vector3(self.Position.X + k, self.Position.Y + k*m, self.Position.Z + 0)

        #check if position is still in between two or not
        pflag = self.validatePoint()
        if(pflag == False):
            a,b=str(self.Lines[self.CurrentSourceIndex]).split(',');# as it implies overshoot
            self.Position.X = float(a)
            self.Position.Y = float(b)
            self.CurrentSourceIndex +=1;#new pos reached
            print(self.CurrentSourceIndex)
            print("\n\n\n\n\n")
             
        logger.debug("[ActiveCar_teja]: {0}".format(self.ID));
        logger.debug("[ActiveCar_teja]: Current velocity: {0}, New position {1}".format(self.Velocity, self.Position));

    

      

        
    
    def slope(self):
        a,b=str(self.Lines[self.CurrentSourceIndex]).split(',');
        x1 = float(a)
        y1=  float(b)
        a,b=str(self.Lines[self.CurrentSourceIndex +1]).split(',');
        x2 = float(a)
        y2=  float(b)

        if(x2-x1 == 0):
            return sys.maxint #for handling perpendicular line
       
        return ( (y2-y1)/(x2-x1));#not handling perpendicular line
        

    def toadd(self,m):
        return float(self.Velocity/math.sqrt(1+m*m));

    def validatePoint(self):
        a,b=str(self.Lines[self.CurrentSourceIndex]).split(',');
        x1 = float(a)
        y1=  float(b)

        a,b=str(self.Lines[self.CurrentSourceIndex +1]).split(',');
        x2 = float(a)
        y2=  float(b)
        d1 = math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1))

        a,b = self.Position.X,self.Position.Y;
        x2= float(a)
        y2=float(b)
        d2 = math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1))

        if(d2>=d1):
            return False;

        return True;
        

    def stop(self):
        logger.debug("[ActiveCar_teja]: {0} stopping".format(self.ID));
        self.Position.X = 0;
        self.Position.Y = 0;
        self.Position.Z = 0;
        #self.Velocity.X = 0;
        #self.Velocity.Y = 0;
        #self.Velocity.Z = 0;
        self.Velocity = 0;

#teja start

#collisions for now assumed in same path and in same direction. Head on is not considered
#TODO: udpate it so that a circle around a car to check for collision with body of others

@parameter(Car_teja)
@subset(Car_teja)
class CarWhichCouldCollide(Car_teja.Class()):
   
    #@staticmethod
    #def __query__(cars, cars2):
        #c = []
        #for c1 in cars1:
        #    for c2 in cars2:
        #        #check if c1 would collide with anyother,if yes add in list, and stop second loop
        #        if CarWhichCouldCollide.__predicate__(c1, c2):                    
        #            c.append(c1)
        #            break
        #return c
        #return [c1 for c1 in cars1 if CarWhichCouldCollide.__predicate__(c1, cars2)]

    @staticmethod
    def __predicate__(c1, cars2):
        m1 = c1.slope();
        k1 = c1.toadd(m1);

        for c2 in cars2:
            #so that this wouldn't be checked at start and TODO:flow won't stop till all reach end
            if(c1.Velocity!=0):
                m2= c2.slope();           
                if(m1 == m2): #in the same line. TODO: How about in the same route
                    if(c1.CurrentSourceIndex<= c2.CurrentSourceIndex): #c1 is behind c2
                        if(c1.Position.X + k1 >= c2.Position.X and c1.Position.Y + k1*m1 >= c2.Position.Y): #c1 is faster than c2, collision could happen
                            return True

        return False

#teja end

@pcc_set
class Pedestrian(object):
    INITIAL_POSITION = 500;
    SPEED = 20;

    _ID = None
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    _X = 0
    @dimension(int)
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        self._X = value

    _Y = 0
    @dimension(int)
    def Y(self):
        return self._Y

    @Y.setter
    def Y(self, value):
        self._Y = value

    def __init__(self, i=None):
        self.ID = i
        self.X = self.INITIAL_POSITION;
        self.Y = 0;

    def move(self):
        self.X -= self.SPEED;

        logger.debug("[Pedestrian]: {0} New position <{1}, {2}>".format(self.ID, self.X, self.Y));

        # End of ride
        if self.X <= 0:
            self.stop();


    def stop(self):
        logger.debug("[Pedestrian]: {0} stopping".format(self.ID));
        self.X = self.INITIAL_POSITION;
        self.Y = 0;

    def setposition(self, x):
        self.X = x;


@subset(Pedestrian)
class StoppedPedestrian(Pedestrian):
    @staticmethod
    def __query__(peds):
        return [p for p in peds if StoppedPedestrian.__predicate__(p)]

    @staticmethod
    def __predicate__(p):
        return p.X == Pedestrian.INITIAL_POSITION
    """() =>
      from p in Frame.Store.Get<Pedestrian>()
      where p.X.Equals(INITIAL_POSITION)
      select p;
    """


@subset(Pedestrian)
class Walker(Pedestrian):
    @staticmethod
    def __query__(peds):
        return [p for p in peds if Walker.__predicate__(p)]

    @staticmethod
    def __predicate__(p):
        return p.X != Pedestrian.INITIAL_POSITION

    """() =>
      from p in Frame.Store.Get<Pedestrian>()
      where !p.X.Equals(INITIAL_POSITION)
      select p;
    """

#@parameterize(Car_teja)
@parameter(Car_teja)
@subset(Pedestrian)
class PedestrianInDanger(Pedestrian):
    def distance(self, p1, p2):
        return abs(self.p1.X - self.p2.X);
        #return Math.Sqrt(Math.Pow(Math.Abs(p1.X -p2.X), 2) +
        #  Math.Pow(Math.Abs(p1.Y -p2.Y), 2));

    @staticmethod
    def __query__(peds, cars):
        return [p for p in peds if PedestrianInDanger.__predicate__(p, cars)]

    @staticmethod
    def __predicate__(p, cars):
        for c in cars:
            if abs(c.Position.X - p.X) < 130 and c.Position.Y == p.Y:
                return True
        return False

    def move(self):
        logger.debug("[Pedestrian]: {0} avoiding collision!".format(self.ID));
        self.Y += 50;

@join(Pedestrian, Car_teja)
class CarAndPedestrianNearby(object):

    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @dimension(Car_teja)
    def car(self):
        return self._car

    @car.setter
    def car(self, value):
        self._car = value

    @dimension(Pedestrian)
    def pedestrian(self):
        return self._ped

    @pedestrian.setter
    def pedestrian(self, value):
        self._ped = value

    def __init__(self, p, c):
        self.car = c
        self.pedestrian = p

    @staticmethod
    def __query__(peds, cars):
        return [CarAndPedestrianNearby.Create(p, c) for p in peds for c in cars if CarAndPedestrianNearby.__predicate__(p, c)]

    @staticmethod
    def __predicate__(p, c):
        if abs(c.Position.X - p.X) < 130 and c.Position.Y == p.Y:
            return True
        return False

    def move(self):
        logger.debug("[Pedestrian]: {0} avoiding collision!".format(self.ID));
        self.pedestrian.Y += 50;

if __name__=="__main__":
    car = Car_teja(10)
    print car.Color
    car.Color = Color.Red
    #print dimensions
    #print sets
    #print subsets
    print car.Color
    print car.ID
