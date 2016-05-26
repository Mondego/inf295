'''
Created on Apr 19, 2016

@author: Rohan Achar
'''
import datamodel.common.datamodel as common
import datamodel.carpedestrian.datamodel as carpedestrian
import datamodel.akshatp.datamodel as akshatp
import datamodel.nodesim.datamodel as nodesim
import datamodel.amazoncar.mydatamodel as amazoncar
import datamodel.uberCar_Xi.datamodel as xi
import datamodel.wpcar.datamodel as wp

DATAMODEL_TYPES = [
                                        carpedestrian.Car,
                                        carpedestrian.Pedestrian,
                                        carpedestrian.ActiveCar,
                                        carpedestrian.InactiveCar,
                                        carpedestrian.Walker,
                                        carpedestrian.PedestrianInDanger,
                                        carpedestrian.StoppedPedestrian,
                                        carpedestrian.CarAndPedestrianNearby,
                                        akshatp.Car_akshatp,
                                        akshatp.Pedestrian_akshatp,
                                        akshatp.ActiveCar_akshatp,
                                        akshatp.InactiveCar_akshatp,
                                        akshatp.Walker_akshatp,
                                        akshatp.StoppedPedestrian_akshatp,
                                        akshatp.CarAndPedestrianNearby_akshatp,
                                        akshatp.PedestrianHasAvodiedCollision_akshatp,
                                        nodesim.Waypoint,
                                        nodesim.BusinessNode,
                                        nodesim.ResidentialNode,
                                        nodesim.Node,
                                        nodesim.RouteRequest,
                                        nodesim.Route,
                                        nodesim.Road,
                                        nodesim.Edge,
                                        common.Vehicle,
                                        amazoncar.AmazonActiveCar,
                                        amazoncar.AmazonInactiveCar,
                                        xi.ActiveUberCar,
                                        xi.CarAndCarInfront,
                                        xi.InactiveUberCar,
                                        xi.UberCar,
                                        wp.AssignedWPCar,
                                        wp.FreeWPCar,
                                        wp.WPCar
                                ]
