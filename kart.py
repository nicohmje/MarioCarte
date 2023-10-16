import pygame
import numpy as np 
import math
from grass import Grass
from boost import Boost
from lava import Lava
from road import Road
from checkpoint import Checkpoint
import track

MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.50


class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """
    
    def __init__(self, controller):
        self.has_finished = False
        self.controller = controller
        self.position = [0,0]
        self.velocity = [0,0]
        self.acceleration = 0
        self.acceleration_c = 0

        self.orientation = 0
        #self.rotational_velocity = 0
        #self.rotational_acceleration = 0
 
        # A modifier et completer
        pass
       
    def reset(self, initial_position, initial_orientation):
        self.position = initial_position
        self.orientation = initial_orientation

        pass
        
    def forward(self):
        self.acceleration_c = MAX_ACCELERATION
        pass
    
    def backward(self):
        self.acceleration_c = -MAX_ACCELERATION
        pass
    
    def turn_left(self):
        self.orientation = self.orientation - MAX_ANGLE_VELOCITY
        pass
        
    def turn_right(self):
        self.orientation = self.orientation + MAX_ANGLE_VELOCITY
        pass
    
    def update_position(self, string, screen):

        boosting = False

        theta_v = math.atan2(self.velocity[1], self.velocity[0])

        #Bound the position to the screen. Account for the position being the top left of the rectangle. Adapt if switching from rec to pic maybe.
        self.position[0] = (self.position[0], self.position[0] + self.velocity[0])[self.position[0] + self.velocity[0]>0 and self.position[0] + self.velocity[0] < screen.get_size()[0]-20]
        self.position[1] = (self.position[1], self.position[1] + self.velocity[1])[self.position[1] + self.velocity[1]>1 and self.position[1] + self.velocity[1] < screen.get_size()[1]-20]
        
        screen_pixel = (screen.get_at((int(self.position[0]), int(self.position[1]))))[0:3]
        if screen_pixel == Grass.color:
            f = Grass.surface_type
        elif screen_pixel == Boost.color:
            f = Boost.surface_type
            boosting = True
        elif screen_pixel == Road.color:
            f = Road.surface_type
        elif screen_pixel == Lava.color:
            f = 0.6
        elif screen_pixel == Checkpoint.color:
            f = 0.02

        self.acceleration = self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v))
        vel = self.acceleration + np.linalg.norm(self.velocity)
        if (not boosting):
            self.velocity[0] = vel * np.cos(self.orientation)
            self.velocity[1] = vel * np.sin(self.orientation)
        else:
            self.velocity[0] = 25 * np.cos(self.orientation)
            self.velocity[1] = 25 * np.sin(self.orientation)
       

        print(f)

        





        
        self.acceleration_c = 0
        pass
    
    def draw(self, screen):
        # A modifier et completer
        kart_position = [self.position[0], self.position[1]]
        kart_radius = 20
        
        #print(self.position)
        # Draw a circle
        # pygame.draw.rect(screen, (255, 255, 255), kart_position, kart_radius)

        pygame.draw.rect(screen, (255,255,0), (kart_position, (kart_radius, kart_radius)))

    # Completer avec d'autres methodes si besoin (ce sera probablement le cas)