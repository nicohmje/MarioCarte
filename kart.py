import pygame
import numpy as np 
import math
from grass import Grass
from boost import Boost
from lava import Lava
from road import Road
from checkpoint import Checkpoint
import track
import time

MAX_ANGLE_VELOCITY = 0.1
MAX_ACCELERATION = 0.25


class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """
    
    def __init__(self, controller):

        self.has_finished = False
        self.controller = controller
        

        self.position = [0,0]       
        self.orientation = 0

        self.velocity = [0,0]

        self.acceleration = 0
        self.acceleration_c = 0

        self.checkpoint = 0 
        self.checkpoint_pos = [150,150]
        self.checkpoint_orient = 0.
        

        self.start_time = time.time_ns()
        self.end_time = 0.0

        self.initialized = False

        self.best_time = 0.0

        pass
       
    def reset(self, initial_position, initial_orientation):
        self.position = initial_position
        self.orientation = initial_orientation
        
        self.velocity = [0.,0.]

        pass
        
    def forward(self):
        self.acceleration_c += MAX_ACCELERATION
        pass
    
    def backward(self):
        self.acceleration_c += -MAX_ACCELERATION
        pass
    
    def turn_left(self):
        self.orientation = self.orientation - MAX_ANGLE_VELOCITY
        pass
        
    def turn_right(self):
        self.orientation = self.orientation + MAX_ANGLE_VELOCITY
        pass
    
    def update_position(self, string, screen):

        boosting = False    

        self.next_checkpoint_id = self.checkpoint + 1

        theta_v = math.atan2(self.velocity[1], self.velocity[0])

        #Bound the position to the screen. Account for the position being the top left of the rectangle. Adapt if switching from rec to pic maybe.
        self.position[0] = (self.position[0], self.position[0] + self.velocity[0])[self.position[0] + self.velocity[0]>0 and self.position[0] + self.velocity[0] < screen.get_size()[0]-20]
        self.position[1] = (self.position[1], self.position[1] + self.velocity[1])[self.position[1] + self.velocity[1]>1 and self.position[1] + self.velocity[1] < screen.get_size()[1]-20]

        if (not self.initialized):
            if 'C' in string:
                self.checkpoint_nbr = 1
            if 'D' in string:
                self.checkpoint_nbr = 2
            if 'E' in string:
                self.checkpoint_nbr = 3
            if 'F' in string:
                self.checkpoint_nbr = 4
            self.initialized = True
            


        screen_pixel = (screen.get_at((int(self.position[0]), int(self.position[1]))))[0:3]

        if screen_pixel == Grass.color:
            f = Grass.surface_type

        elif screen_pixel== Boost.color:
            f = Boost.surface_type
            boosting = True

        elif screen_pixel == Road.color:
            f = Road.surface_type

        elif screen_pixel == Lava.color:
            f = Checkpoint.surface_type
            print("LAVA")
            self.reset(np.array(self.checkpoint_pos), self.checkpoint_orient)

        elif screen_pixel[0:2] == Checkpoint.color[0:2]:
            f = Checkpoint.surface_type

            cur_checkpoint = (screen_pixel[2] - Checkpoint.color[2])+1
                        
            if cur_checkpoint > self.checkpoint + 1:
                pass
            elif cur_checkpoint == self.checkpoint_nbr:
                self.end_time = time.time_ns()
                #self.has_finished = True
                time_took = self.end_time - self.start_time
                if (time_took*1e-9 < self.best_time or self.best_time == 0.0):
                    self.best_time = time_took*1e-9
                print("Finished in", time_took*1e-9, "s")
                self.start_time = time.time_ns()
                self.reset([150,150], 0)
                self.checkpoint = 0 #THIS ONE HERE
                print(self.checkpoint)
                pass
            elif cur_checkpoint>self.checkpoint:

                print("Checkpoint reached:", cur_checkpoint)
                self.checkpoint = cur_checkpoint
                self.checkpoint_pos[0] = np.copy(self.position[0])
                self.checkpoint_pos[1] = np.copy(self.position[1])
                self.checkpoint_orient = np.copy(self.orientation)
            
                

        self.acceleration = self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v))
        vel = self.acceleration + np.linalg.norm(self.velocity) 
        if (not boosting):
            self.velocity[0] = vel * np.cos(self.orientation)
            self.velocity[1] = vel * np.sin(self.orientation)
        else:
            self.velocity[0] = 25 * np.cos(self.orientation)
            self.velocity[1] = 25 * np.sin(self.orientation)

        status_checkpoint_str = "Checkpoint: " + str(self.checkpoint)
        font = pygame.font.SysFont(None, size=36)  # You can adjust the size as needed
        text = font.render(status_checkpoint_str, True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (95, 27)  # Adjust the position as needed
        screen.blit(text, text_rect)

        font = pygame.font.SysFont(None, size=60)  # You can adjust the size as needed
        if (((time.time_ns() - self.start_time)*1e-9)> self.best_time) : 
            color = (255, 30, 30)
        else:
            color = (0, 0, 0)
        text = font.render(("%0.2f s" % ((time.time_ns() - self.start_time)*1e-9)), True, color)
        text_rect = text.get_rect()
        text_rect.center = (screen.get_size()[0]//2, screen.get_size()[1]//2)  # Adjust the position as needed
        screen.blit(text, text_rect)

        font = pygame.font.SysFont(None, size=40)  # You can adjust the size as needed
        text = font.render(("Best time: %0.2f s" % self.best_time), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (screen.get_size()[0]//2, screen.get_size()[1]//2+100)  # Adjust the position as needed
        screen.blit(text, text_rect)

        

        self.acceleration_c = 0
        pass
    
    def draw(self, screen):
        # A modifier et completer
        kart_position = [self.position[0], self.position[1]]
        kart_radius = 20
        
        #print(self.position)
        # Draw a circle
        # pygame.draw.rect(screen, (255, 255, 255), kart_position, kart_radius)

        pygame.draw.circle(screen, (255,255,0), kart_position, kart_radius)

        circle_pos=[0,0]
        circle_pos[0] = kart_position[0] + (15 * np.cos(self.orientation))
        circle_pos[1] = kart_position[1] + (15 * np.sin(self.orientation))

        pygame.draw.circle(screen, (0,0,0), circle_pos, kart_radius/5.)

        



    # Completer avec d'autres methodes si besoin (ce sera probablement le cas)