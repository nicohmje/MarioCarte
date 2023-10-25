import pygame
import numpy as np 
import math
from grass import Grass
from boost import Boost
from lava import Lava
from road import Road
from checkpoint import Checkpoint
import track
import game
import time

from common import Common

MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25

TEXT = True

class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """

    nbr_of_karts = 0

    kart_texture_top = None
    kart_texture_side = None
    splash_screen = None
    screen_size = None

    started = False


    def __init__(self, controller):

        self.has_finished = False
        self.controller = controller

        Kart.nbr_of_karts += 1

        self.position = np.array([0.,0.])       
        self.orientation = 0

        self.velocity = np.array([0.,0.])

        self.acceleration = 0
        self.acceleration_c = 0

        self.checkpoint = 0 
        self.checkpoint_pos = np.array([150,150])
        self.checkpoint_orient = 0.
        

        self.start_time = time.time_ns()
        self.__end_time = 0.0

        self.map = np.empty((10000,10000), dtype=str)

        self.initialized = False

        self.best_time = 0.0

        pass
       
    def reset(self, initial_position, initial_orientation):
        self.position = np.copy(initial_position)
        self.orientation = np.copy(initial_orientation)

        print(initial_orientation)
        
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

        #INITIALIZATION 
        if (not self.initialized):
            if 'C' in string:
                self.checkpoint_nbr = 1
            if 'D' in string:
                self.checkpoint_nbr = 2
            if 'E' in string:
                self.checkpoint_nbr = 3
            if 'F' in string:
                self.checkpoint_nbr = 4
            
            i,j = 0,0
            for char in string:
                if char.isalpha():
                    self.map[i,j] = char
                if char == "\n":
                    j += 1
                    i = 0
                else:
                    i += 1
            self.map = self.map[0:i+1, 0:j+1]

        if Kart.started:
            boosting = False    

            self.next_checkpoint_id = self.checkpoint + 1

            theta_v = math.atan2(self.velocity[1], self.velocity[0])

            if self.screen_size is None:
                self.screen_size = screen.get_size()

            #Bound the position to the screen. Account for the position being the top left of the rectangle. Adapt if switching from rec to pic maybe.
            if (self.position[0] + self.velocity[0]>0 and self.position[0] + self.velocity[0] < self.screen_size[0]-20):
                self.position[0] = self.position[0] + self.velocity[0]
            else:
                self.reset(self.checkpoint_pos, self.checkpoint_orient)
                return
            if (self.position[1] + self.velocity[1]>1 and self.position[1] + self.velocity[1] < self.screen_size[1]-20):
                self.position[1] = self.position[1] + self.velocity[1]
            else:
                self.reset(self.checkpoint_pos, self.checkpoint_orient)
                return


            string_letter = ord(self.map[int(np.floor(self.position[0]/track.BLOCK_SIZE)), int(np.floor(self.position[1]/track.BLOCK_SIZE))])
        
            if string_letter == ord('G'):
                f = Grass.surface_type

            elif string_letter == ord('B'):
                f = Boost.surface_type
                boosting = True

            elif string_letter == ord('R'):
                f = Road.surface_type

            elif string_letter == ord('L'):
                f = Checkpoint.surface_type
                print("LAVA")
                self.reset(np.array(self.checkpoint_pos), self.checkpoint_orient)

            elif (string_letter >= ord('C') and string_letter <= ord('F')):
                f = Checkpoint.surface_type

                cur_checkpoint = (string_letter - ord('C')) + 1
                
                if cur_checkpoint > self.checkpoint + 1:
                    pass
                elif cur_checkpoint == self.checkpoint_nbr:
                    self.__end_time = time.time_ns()

                    #self.has_finished = True

                    time_took = self.__end_time - self.start_time
                    if (time_took*1e-9 < self.best_time or self.best_time == 0.0):
                        self.best_time = time_took*1e-9

                    print("Finished in", time_took*1e-9, "s")
                    self.start_time = time.time_ns()
                    self.reset([150,150], 0)
                    self.checkpoint = 0
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
                self.velocity = (vel * np.cos(self.orientation), vel*np.sin(self.orientation))
            else:
                self.velocity = (25 * np.cos(self.orientation), 25*np.sin(self.orientation))
            

            if TEXT:
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
                text_rect.center = (self.screen_size[0]//2, self.screen_size[1]//2)  # Adjust the position as needed
                screen.blit(text, text_rect)

                font = pygame.font.SysFont(None, size=40)  # You can adjust the size as needed
                text = font.render(("Best time: %0.2f s" % self.best_time), True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.center = (self.screen_size[0]//2, self.screen_size[1]//2+100)  # Adjust the position as needed
                screen.blit(text, text_rect)


            self.acceleration_c = 0
        pass
    
    def draw(self, screen):
        kart_position = [self.position[0], self.position[1]]
        kart_radius = 20




        #IF NONE OF THE TEXTURES HAVE BEEN LOADED, LOAD THEM:
        if (not self.initialized):
            scale = 3

            Kart.splash_screen = pygame.image.load("textures/splash_screen.jpg").convert()

            Kart.kart_texture_top = pygame.image.load("textures/kart_side.png").convert_alpha()
            Kart.kart_texture_top = pygame.transform.scale(Kart.kart_texture_top, (Kart.kart_texture_top.get_width() * scale, Kart.kart_texture_top.get_height() * scale))

            Kart.kart_texture_side = pygame.image.load("textures/kart_top2.png").convert_alpha()
            Kart.kart_texture_side= pygame.transform.scale(Kart.kart_texture_side, (Kart.kart_texture_side.get_width() * scale, Kart.kart_texture_side.get_height() * scale))

            Kart.kart_texture_diag = pygame.image.load("textures/kart_diag.png").convert_alpha()
            Kart.kart_texture_diag = pygame.transform.scale(Kart.kart_texture_diag, (Kart.kart_texture_diag.get_width() * scale, Kart.kart_texture_diag.get_height() * scale))

            Kart.kart_texture_diag2 = pygame.image.load("textures/kart_diag2.png").convert_alpha()
            Kart.kart_texture_diag2 = pygame.transform.scale(Kart.kart_texture_diag2, (Kart.kart_texture_diag2.get_width() * scale, Kart.kart_texture_diag2.get_height() * scale))

            Kart.texture_arr = np.array([Kart.kart_texture_side, Kart.kart_texture_diag, Kart.kart_texture_top, Kart.kart_texture_diag2, Kart.kart_texture_side, Kart.kart_texture_diag, Kart.kart_texture_top, Kart.kart_texture_diag2])

            self.initialized = True
            Kart.started = game.splash_screen(screen,Kart.splash_screen, Kart.started)
            self.start_time = time.time_ns()

        #Figure out the orientation's cardinal direction, and blit the appropriate image. 
        quadr = Common.quadrant(float(self.orientation))
        screen.blit(Kart.texture_arr[quadr], (kart_position[0]-kart_radius, kart_position[1]-kart_radius))
            