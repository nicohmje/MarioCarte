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
import logging



# ROAD MAP: ADD TRAIL (and boosting effect) || FIX AI AND HUMAN || FIND FINISH LINE

from common import Common

MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25
BOOST_SPEED = 25.

TEXT = True

logger = logging.getLogger('MariooCarteLogger')



class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """

    nbr_of_karts = 0

    kart_texture_top = None
    kart_texture_side = None
    splash_screen = None
    screen_size = None

    sound = None
    started = False


    def __init__(self, controller):

        self.has_finished = False
        self.controller = controller

        Kart.nbr_of_karts += 1

        self.id = Kart.nbr_of_karts

        self.position = np.array([0.,0.], dtype=float)       
        self.orientation = 0

        self.velocity = np.array([0.,0.], dtype=float)

        self.acceleration = 0
        self.acceleration_c = 0

        self.checkpoint = 0 
        self.checkpoint_pos = np.array([150,150])
        self.checkpoint_orient = 0.
        self.checkpoint_step = 0
        

        self.start_time = time.time_ns()
        self.__end_time = 0.0

        self.char_map = np.empty((10000,10000), dtype=str)

        self.initialized = False

        self.best_time = 0.0

        self.__input = 0 #1 FORW 2 LEFT 3 RIGHT 4 BACK
        self.music_playing = False

        pass
       
    def reset(self, initial_position, initial_orientation, step=0):
        self.position = np.copy(initial_position)
        self.orientation = np.copy(initial_orientation)        
        self.velocity = np.array([0.,0.])
        if self.initialized:
            self.controller.reset(step)
            # time.sleep(4)

        pass
        
    def forward(self):
        self.acceleration_c += MAX_ACCELERATION
        self.__input = 1

        logger.debug("Kart number %i: FORWARDS", self.id)

        pass
    
    def backward(self):
        self.acceleration_c += -MAX_ACCELERATION
        self.__input = 4

         
        logger.debug("Kart number %i: BACKWARDS", self.id)

        pass
    
    def turn_left(self):
        self.orientation = self.orientation - MAX_ANGLE_VELOCITY
        self.__input = 2

         
        logger.debug("Kart number %i: LEFT", self.id)

        pass
        
    def turn_right(self):
        self.orientation = self.orientation + MAX_ANGLE_VELOCITY
        self.__input = 3
         
        logger.debug("Kart number %i: RIGHT", self.id)

        pass
    
    def update_position(self, string, screen):
         
        #logger.debug("Kart number %i: POSITION TYPE: %s", self.id, self.position.dtype)

        if(not self.position.dtype == "float64"): 
            self.position = self.position.astype(float)

        if(not self.velocity.dtype == "float64"): 
            self.velocity = self.velocity.astype(float)

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
                    self.char_map[i,j] = char
                if char == "\n":
                    j += 1
                    i = 0
                else:
                    i += 1
            self.char_map = self.char_map[0:i+1, 0:j+1]
            pygame.mixer.music.load("sounds/grass.wav")

        if Kart.started:
            boosting = False    

            self.orientation = Common.RadiansLim(self.orientation)

            self.next_checkpoint_id = self.checkpoint + 1

            theta_v = math.atan2(self.velocity[1], self.velocity[0])

            if self.screen_size is None:
                self.screen_size = screen.get_size()

            string_letter = ord(self.char_map[int(np.floor(self.position[0]/track.BLOCK_SIZE)), int(np.floor(self.position[1]/track.BLOCK_SIZE))])


            if string_letter == ord('G') and not self.music_playing:
                pygame.mixer.music.play(-1)
                f = Grass.surface_type
                self.music_playing = True
            elif string_letter == ord('G') and self.music_playing:
                f = Grass.surface_type

            if not string_letter == ord('G') and self.music_playing :
                #logger.debug("Kart number %i: stop grass sound")
                pygame.mixer.music.fadeout(300)
                self.music_playing = False

            match string_letter:
                case 66: #ASCII FOR B
                    pygame.mixer.Sound.play(Boost.sound)
                    f = Boost.surface_type
                    boosting = True

                case 82: #ASCII FOR R
                    f = Road.surface_type

                case 76: #ASCII FOR L
                    pygame.mixer.Sound.play(Lava.sound)
                    f = Checkpoint.surface_type
                    self.reset(np.array(self.checkpoint_pos), self.checkpoint_orient, self.checkpoint_step)

                case 67|68|69|70:
                    f = Checkpoint.surface_type
                    cur_checkpoint = (string_letter - ord('C')) + 1
                    if cur_checkpoint > self.checkpoint + 1:
                        pass
                    elif cur_checkpoint == self.checkpoint_nbr:
                        self.__end_time = time.time_ns()

                        self.has_finished = False

                        time_took = self.__end_time - self.start_time
                        if (time_took*1e-9 < self.best_time or self.best_time == 0.0):
                            self.best_time = time_took*1e-9

                        logger.info("Finished in", time_took*1e-9, "s")
                        self.start_time = time.time_ns()
                        self.reset([150.,150.], 0., -1)
                        self.checkpoint = 0
                        logger.info(self.checkpoint)
                        pass
                    elif cur_checkpoint>self.checkpoint:
                        logger.info("Checkpoint reached: %i" , cur_checkpoint)
                        pygame.mixer.Sound.play(Checkpoint.sound)
                        self.checkpoint = cur_checkpoint
                        self.checkpoint_step = self.controller.step
                        self.checkpoint_pos[0] = np.copy(self.position[0])
                        self.checkpoint_pos[1] = np.copy(self.position[1])
                        self.checkpoint_orient = np.copy(self.orientation)


            self.acceleration = (self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v)))
            vel = self.acceleration + np.linalg.norm(self.velocity) 
            
            #logger.debug("Kart number %i: vel: %s ; orientation: %s ; theta_v: %s", self.id, vel, self.orientation, theta_v)

            if (not boosting):
                self.velocity = np.array([round((vel * np.cos(self.orientation)),4), round((vel*np.sin(self.orientation)),4)])
            else:
                self.velocity = np.array([round(25 * np.cos(self.orientation),4), round(25*np.sin(self.orientation),4)])
            

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

            #logger.debug("Kart number %i: accel: %s ; velocity(norm): %s ; velocity : %s ", self.id, self.acceleration, np.linalg.norm(self.velocity), self.velocity)

            self.position = self.position.astype(float)

            #Bound the position to the screen. Account for the position being the top left of the rectangle. Adapt if switching from rec to pic maybe.
            if (self.position[0] + self.velocity[0]>0. and self.position[0] + self.velocity[0] < self.screen_size[0]-20.):
                self.position[0] += self.velocity[0]
            else:
                self.reset(self.checkpoint_pos, self.checkpoint_orient, self.checkpoint_step)
                return
            if (self.position[1] + self.velocity[1]>1 and self.position[1] + self.velocity[1] < self.screen_size[1]-20):
                self.position[1] = self.position[1] + self.velocity[1]
            else:
                self.reset(self.checkpoint_pos, self.checkpoint_orient, self.checkpoint_step)
                return
            
            
            self.acceleration_c = 0
        pass
    
    def draw(self, screen):
        kart_position = np.copy(self.position)
        kart_radius = 20




        #IF NONE OF THE TEXTURES HAVE BEEN LOADED, LOAD THEM:
        if (not self.initialized):
            scale = 0.05

            Kart.splash_screen = pygame.image.load("textures/splash_screen.jpg").convert()



            Kart.texture_top_fast = pygame.image.load("textures/Kart/forw_fast.png").convert_alpha()
            Kart.texture_top_slow = pygame.image.load("textures/Kart/forw_slow.png").convert_alpha()
            Kart.texture_top_stop = pygame.image.load("textures/Kart/stationnary.png").convert_alpha()

            Kart.texture_top_fast = pygame.transform.scale(Kart.texture_top_fast, (Kart.texture_top_fast.get_width() * scale, Kart.texture_top_fast.get_height() * scale))
            Kart.texture_top_slow = pygame.transform.scale(Kart.texture_top_slow, (Kart.texture_top_slow.get_width() * scale, Kart.texture_top_slow.get_height() * scale))
            Kart.texture_top_stop = pygame.transform.scale(Kart.texture_top_stop, (Kart.texture_top_stop.get_width() * scale, Kart.texture_top_stop.get_height() * scale))

            Kart.texture_top = np.array([Kart.texture_top_stop, Kart.texture_top_slow, Kart.texture_top_fast])


            Kart.texture_right_fast = pygame.image.load("textures/Kart/right_fast.png").convert_alpha()
            Kart.texture_right_slow = pygame.image.load("textures/Kart/right_slow.png").convert_alpha()
            Kart.texture_right_stop = pygame.image.load("textures/Kart/right.png").convert_alpha()

            Kart.texture_right_fast = pygame.transform.scale(Kart.texture_right_fast, (Kart.texture_right_fast.get_width() * scale, Kart.texture_right_fast.get_height() * scale))
            Kart.texture_right_slow = pygame.transform.scale(Kart.texture_right_slow, (Kart.texture_right_slow.get_width() * scale, Kart.texture_right_slow.get_height() * scale))
            Kart.texture_right_stop = pygame.transform.scale(Kart.texture_right_stop, (Kart.texture_right_stop.get_width() * scale, Kart.texture_right_stop.get_height() * scale))

            Kart.texture_right = np.array([Kart.texture_right_stop, Kart.texture_right_slow, Kart.texture_right_fast])


            Kart.texture_left_fast = pygame.image.load("textures/Kart/left_fast.png").convert_alpha()
            Kart.texture_left_slow = pygame.image.load("textures/Kart/left_slow.png").convert_alpha()
            Kart.texture_left_stop = pygame.image.load("textures/Kart/left.png").convert_alpha()

            Kart.texture_left_fast = pygame.transform.scale(Kart.texture_left_fast, (Kart.texture_left_fast.get_width() * scale, Kart.texture_left_fast.get_height() * scale))
            Kart.texture_left_slow = pygame.transform.scale(Kart.texture_left_slow, (Kart.texture_left_slow.get_width() * scale, Kart.texture_left_slow.get_height() * scale))
            Kart.texture_left_stop = pygame.transform.scale(Kart.texture_left_stop, (Kart.texture_left_stop.get_width() * scale, Kart.texture_left_stop.get_height() * scale))

            Kart.texture_left = np.array([Kart.texture_left_stop, Kart.texture_left_slow, Kart.texture_left_fast])

            Kart.textures = np.array([Kart.texture_top, Kart.texture_left, Kart.texture_right, Kart.texture_top])


            self.initialized = True
            Kart.started = game.splash_screen(screen,Kart.splash_screen, Kart.started)
            self.start_time = time.time_ns()

        #Figure out the orientation's cardinal direction, and blit the appropriate image. 
        # quadr = Common.quadrant(float(self.orientation))
        vel_scale = 0 

        if (np.linalg.norm(self.velocity)>2 and np.linalg.norm(self.velocity)<5):
            vel_scale = 1
        elif (np.linalg.norm(self.velocity)>=5):
            vel_scale = 2

        output_texture = Kart.textures[self.__input-1][vel_scale]
        output_texture = pygame.transform.rotate(output_texture, -1* Common.RadToDegrees(self.orientation))
        screen.blit(output_texture, (kart_position[0]-(output_texture.get_height()/2), kart_position[1]-(output_texture.get_width()/2)))

        Vel_dir = self.velocity / (max(np.abs(self.velocity)) +1e-3)

        Ratio = max(min(np.linalg.norm(self.velocity)*20, 230), 45)

        future_x = int(Ratio*Vel_dir[0])
        future_y = int(Ratio*Vel_dir[1])


        k = 0.3
        angle = 0.30 + 0.4 * (1 - np.exp(-k * np.linalg.norm(self.velocity)))
        scale = 1/1

        if np.linalg.norm(self.velocity) < 2:
                angle = 1.2 

        skew = (0.,0.)

        if self.__input == 3:
            skew = (1.,-1.) #pos is left
        elif self.__input == 2:
            skew = (-1.,1.) 



        pos_rotated_velocity_vector_x = int(scale*int(future_x  * np.cos(angle+ skew[0]*0.2) - future_y * np.sin(angle+ skew[0]*0.2)))
        pos_rotated_velocity_vector_y = int(scale*int(future_x * np.sin(angle+ skew[0]*0.2) + future_y * np.cos(angle+ skew[0]*0.2)))

        neg_rotated_velocity_vector_x = int(scale*int(future_x * np.cos(-(angle+ skew[1]*0.2)) - future_y * np.sin(-(angle+ skew[1]*0.2))))
        neg_rotated_velocity_vector_y = int(scale*int(future_x * np.sin(-(angle+ skew[1]*0.2)) + future_y * np.cos(-(angle+ skew[1]*0.2))))

        pygame.draw.circle(screen, (255, 255, 255), [future_x+self.position[0],future_y+self.position[1]], 2.0)
        pygame.draw.circle(screen, (255, 255, 255), [pos_rotated_velocity_vector_x+self.position[0],pos_rotated_velocity_vector_y+self.position[1]], 2.0)
        pygame.draw.circle(screen, (255, 255, 255), [neg_rotated_velocity_vector_x+self.position[0],neg_rotated_velocity_vector_y+self.position[1]], 2.0)



        self.__input = 0 

    def check_radar_speed(self,delta):
        braking = False
        radar_readings = []
        range_points = 10*int(np.linalg.norm(self.velocity))
        if delta < 0.2 and (np.linalg.norm(self.velocity) < 15.):
            return braking
        elif np.linalg.norm(self.velocity) >= 20.:
            braking = True
            return braking
        elif np.absolute(delta) > 0.6:
            braking = True
            return braking
        

        else:

            for i in range(1, range_points + 2):
                # Calculate the position of the point in front of the kart
                x_check = int(self.position[0] + i * np.cos(self.orientation))
                y_check = int(self.position[1] + i * np.sin(self.orientation))

                # Check if the calculated position is within the map boundaries
                if 0 <= x_check < self.char_map.shape[0] and 0 <= y_check < self.char_map.shape[1]:
                    # Read the value at the calculated position
                    block_value = self.char_map[x_check, y_check]
                    radar_readings.append(block_value)
                else:
                    # If the position is outside the map, consider it as a wall
                    radar_readings.append(0)
            
            sr = set(radar_readings)
            if (sr.intersection([0]) == set([0])):
                braking = True
                return braking
            else:
                return braking

    def read_map(self):
        boosting = False
        X = np.array(self.position, dtype=np.int16)
        point = self.map[X[0]][X[1]]

        if point >= 101 and point <=104:
            f = Checkpoint.surface_type
            return 'ap',boosting, f 

        match point:
            case  0:
                f = Grass.surface_type
                return 'ap',boosting, f
            case 200:
                boosting = True
                f = Boost.surface_type
                return 'ap',boosting, f
            case _:
                f = Road.surface_type
                return 'a',boosting, f
        
    def radar_points(self):
        dist_min = 100
        for p in self.path:
            px = float(p[0])
            py = float(p[1])
            dx = self.position[0] - px
            dy = self.position[1] - py
            dist = np.sqrt(dx**2 + dy**2)
            if (dist<dist_min) and (p!=self.path[-1]) :
                self.path.remove(p)
                # print('removed :',p)

    def create_map(self,useable_array):
        self.map = useable_array

    def update_pos_AI(self):
        _, boosting,f = self.read_map()
        theta_v = math.atan2(self.velocity[1], self.velocity[0])
        self.acceleration = self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v))
        vel = self.acceleration + np.linalg.norm(self.velocity) 
        
        if (not boosting):
                self.velocity = (vel * np.cos(self.orientation), vel*np.sin(self.orientation))
        else:
                self.velocity = (BOOST_SPEED * np.cos(self.orientation), BOOST_SPEED*np.sin(self.orientation))
                        
        if (self.position[0] + self.velocity[0]>0. and self.position[0] + self.velocity[0] < np.shape(self.char_map)[0]):
                self.position[0] += self.velocity[0]
        else:
            pass
        
        if (self.position[1] + self.velocity[1]>0 and self.position[1] + self.velocity[1] < np.shape(self.char_map)[1]-20):
            self.position[1] = self.position[1] + self.velocity[1]
        else:
            pass

        logger.debug("MAP SIZE: %s", np.shape(self.char_map))

        self.acceleration_c = 0       
        pass