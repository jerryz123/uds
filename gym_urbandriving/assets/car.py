import numpy as np
from gym_urbandriving.assets.primitives import *
from gym_urbandriving.assets import *
from gym import spaces

class Car(Rectangle):
    
    def __init__(self, x, y, xdim=50, ydim=25, angle=0.0, vel=0.0, acc=0.0, max_vel=20.0, mass=100.0):
        Rectangle.__init__(self, x, y, xdim, ydim, angle, sprite="grey_car_lite.png")
        self.vel = vel
        self.acc = acc
        self.max_vel = max_vel
        self.mass = mass
        self.action_space = spaces.Box(np.array([-2, -1]),
                                       np.array([2, 1]))


    def step(self, action, info_dict=None):
        """
        Updates the car for one timestep.
        Args:
            action: 1x2 array, steering / acceleration action.
            info_dict: dict, contains information about the environment.
        """
        if action is None:
            action_steer, action_acc = 0.0, 0.0
        else:
            action_steer, action_acc = action
        self.angle += action_steer
        self.angle %= 360.0
        self.angle = self.angle
        self.acc = action_acc
        self.acc = max(min(self.acc, self.max_vel - self.vel), -self.vel)

        t = 1
        dist = self.vel * t + 0.5 * self.acc * (t ** 2)
        dx = dist * np.cos(np.radians(self.angle))
        dy = dist * -np.sin(np.radians(self.angle))
        self.x += dx
        self.y += dy
        self.vel += self.acc
        self.vel = max(min(self.vel, self.max_vel), 0.0)
        
    def get_state(self):
        """
        Get state. 
        Returns:
            state: 1x3 array, contains x, y, angle of car.
            info_dict: dict, contains information about car.
        """
        return self.x,self.y,self.x_dim,self.y_dim,self.angle


    def collides(self, other):
        from gym_urbandriving.assets.kinematic_car import KinematicCar
        if type(other) in {Terrain, Sidewalk, Car, KinematicCar, Pedestrian}:
            return self.intersect(other)
        return False
