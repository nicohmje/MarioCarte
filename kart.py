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
from common import Common




#This is the Kart class.
#It includes the necessary functions to make an AI or Human powered Kart work. It also includes some texture loading for the Kart's sprite.






MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25
BOOST_SPEED = 25.

TEXT = True

logger = logging.getLogger('MariooCarteLogger')


class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """

    __nbr_of_karts = 0
    __splash_screen = None
    __music_playing = False
    __ongrass = 0
    __screen_size = None

    sound = None
    __started = False

    @property 
    def has_finished(self):
        return self.__has_finished
    
    @property 
    def checkpoint(self):
        return self.__checkpoint

    @property 
    def controller(self):
        return self.__controller
    
    @property 
    def position(self):
        return self.__position
    
    @property 
    def checkpoint_pos(self):
        return self.__checkpoint_pos
    @property 
    def checkpoint_orient(self):
        return self.__checkpoint_orient
    
    @property 
    def velocity(self):
        return self.__velocity
    
    @property 
    def orientation(self):
        return self.__orientation
    
    @classmethod
    def nbr_of_karts_(cls):
        return Kart.__nbr_of_karts
    
    def __del__(self):
        Kart.__nbr_of_karts -= 1

    def __init__(self, controller):

        self.__has_finished = False

        self.__controller = controller

        Kart.__nbr_of_karts += 1
        

        self.__id = Kart.__nbr_of_karts

        self.__position = np.array([0.,0.], dtype=float)       
        self.__orientation = 0
        self.__velocity = np.array([0.,0.], dtype=float)

        self.__acceleration = 0
        self.__acceleration_c = 0

        self.__checkpoint = 0 
        self.__checkpoint_pos = np.array([150,150])
        self.__checkpoint_orient = 0.
        self.__checkpoint_step = 0

        self.__grass = False
        

        self.__start_time = time.time_ns()
        self.__end_time = 0.0

        self.__char_map = np.empty((100,100), dtype=str)

        self.__initialized = False

        self.__best_time = 0

        self.__input = 0 #1 FORW 2 LEFT 3 RIGHT 4 BACK

        pass
       
    def reset(self, position, orientation, step=0):
        self.__position = np.copy(position)
        self.__orientation = np.copy(orientation)   
        self.__velocity = np.array([0.,0.], dtype=float)
        self.__acceleration_c = 0
        self.__acceleration = 0
        if self.__initialized and not np.isnan(step):
            self.__controller.reset(step)
            self.__checkpoint_pos = np.copy(self.controller.initial_position)
            self.__checkpoint_orient = np.copy(self.controller.initial_angle)
            self.__position = np.copy(self.controller.initial_position)
            self.__orientation = np.copy(self.controller.initial_angle)
            # time.sleep(4)
        pass
        
    def forward(self):
        self.__acceleration_c += MAX_ACCELERATION
        self.__input = 1

        logger.debug("Kart number %i: FORWARDS, pos %s", self.__id, self.__position)

        pass
    
    def backward(self):
        self.__acceleration_c += -MAX_ACCELERATION
        self.__input = 4

         
        logger.debug("Kart number %i: BACKWARDS", self.__id)

        pass
    
    def turn_left(self):
        self.__orientation = self.__orientation - MAX_ANGLE_VELOCITY
        self.__input = 2

         
        logger.debug("Kart number %i: LEFT", self.__id)

        pass
        
    def turn_right(self):
        self.__orientation = self.__orientation + MAX_ANGLE_VELOCITY
        self.__input = 3
         
        logger.debug("Kart number %i: RIGHT", self.__id)

        pass
    
    def update_position(self, string, screen):

         
        #logger.debug("Kart number %i: POSITION TYPE: %s", self.__id, self.__position.dtype)

        if(not self.__position.dtype == "float64"): 
            self.__position = self.__position.astype(float)

        if(not self.__velocity.dtype == "float64"): 
            self.__velocity = self.__velocity.astype(float)

        #INITIALIZATION 
        if (not self.__initialized):
            if 'F' in string:
                self.__checkpoint_nbr = 4
            elif 'E' in string:
                self.__checkpoint_nbr = 3
            elif 'D' in string:
                self.__checkpoint_nbr = 2
            elif 'C' in string:
                self.__checkpoint_nbr = 1
            else:
                raise ValueError("Track string contains no checkpoints. They are represented by the letters C,D,E and F.")
            
            
            
            i,j = 0,0
            for char in string:
                if char.isalpha():
                    self.__char_map[i,j] = char
                if char == "\n":
                    j += 1
                    i = 0
                else:
                    i += 1
            # print(np.shape(self.__char_map))
            # self.__char_map = np.resize(self.__char_map, (i+1, j+1))
            # print(np.shape(self.__char_map))
            pygame.mixer.music.load("sounds/grass.wav")

        if Kart.__started:
            boosting = False    


            self.__orientation = Common.RadiansLim(self.__orientation)

            theta_v = math.atan2(self.__velocity[1], self.__velocity[0])

            if Kart.__screen_size is None:
                Kart.__screen_size = screen.get_size()

            string_letter = ord(self.__char_map[int(np.floor(self.__position[0]/track.BLOCK_SIZE)), int(np.floor(self.__position[1]/track.BLOCK_SIZE))])


            if string_letter == ord('G') and not Kart.__music_playing and not self.__grass:
                pygame.mixer.music.play(-1)
                f = Grass.surface_type_()
                Kart.__music_playing = True
                Kart.__ongrass += 1
                self.__grass = True
            elif string_letter == ord('G') and Kart.__music_playing:
                f = Grass.surface_type_()

            if not string_letter == ord('G') and Kart.__music_playing and self.__grass:
                #logger.debug("Kart number %i: stop grass sound")
                Kart.__ongrass -=1
                if (not Kart.__ongrass):
                    pygame.mixer.music.fadeout(300)
                Kart.__music_playing = False
                self.__grass = False

            match string_letter:
                case 66: #ASCII FOR B
                    pygame.mixer.Sound.play(Boost.sound)
                    f = Boost.surface_type_()
                    boosting = True

                case 82: #ASCII FOR R
                    f = Road.surface_type_()

                case 76: #ASCII FOR L
                    pygame.mixer.Sound.play(Lava.sound)
                    f = Checkpoint.surface_type_()
                    self.reset(np.array(self.__checkpoint_pos), self.__checkpoint_orient, np.nan)

                case 67|68|69|70:
                    f = Checkpoint.surface_type_()
                    cur_checkpoint = (string_letter - ord('C')) + 1
                    if cur_checkpoint > self.__checkpoint + 1:
                        pass
                    elif cur_checkpoint == self.__checkpoint_nbr:

                        self.__has_finished = False

                        #time_took = self.__end_time - self.__start_time
                        if (self.controller.step < self.__best_time or self.__best_time == 0):
                            self.__best_time = self.controller.step

                        logger.info("Finished in %i steps", self.controller.step)
                        #self.__start_time = time.time_ns()
                        self.reset(self.controller.initial_position, self.controller.initial_angle, -1)
                        self.__checkpoint = 0
                        pass
                    elif cur_checkpoint>self.__checkpoint:
                        if (not self.__controller.is_ai):
                            logger.info("Checkpoint reached: %i" , cur_checkpoint)
                        pygame.mixer.Sound.play(Checkpoint.sound)
                        self.__checkpoint = cur_checkpoint
                        self.__checkpoint_step = self.__controller.step
                        self.__checkpoint_pos[0] = np.copy(self.__position[0])
                        self.__checkpoint_pos[1] = np.copy(self.__position[1])
                        self.__checkpoint_orient = np.copy(self.__orientation)


            self.__acceleration = (self.__acceleration_c - (f * np.linalg.norm(self.__velocity) * np.cos(self.__orientation - theta_v)))
            vel = self.__acceleration + np.linalg.norm(self.__velocity) 
            
            #logger.debug("Kart number %i: vel: %s ; orientation: %s ; theta_v: %s", self.__id, vel, self.__orientation, theta_v)

            if (not boosting):
                self.__velocity = np.array([round((vel * np.cos(self.__orientation)),4), round((vel*np.sin(self.__orientation)),4)])
            else:
                self.__velocity = np.array([round(25 * np.cos(self.__orientation),4), round(25*np.sin(self.__orientation),4)])
            

            if TEXT and not (self.__controller.is_ai and Kart.nbr_of_karts_()>1):
                status_checkpoint_str = "Checkpoint: " + str(self.__checkpoint)
                font = pygame.font.SysFont(None, size=36)  # You can adjust the size as needed
                text = font.render(status_checkpoint_str, True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.center = (95, 27)  # Adjust the position as needed
                screen.blit(text, text_rect)


                font = pygame.font.SysFont(None, size=60)  # You can adjust the size as needed
                if ((self.controller.step)> self.__best_time) : 
                    color = (255, 30, 30)
                else:
                    color = (0, 0, 0)
                    
                text = font.render(("%4i steps" % (self.controller.step)), True, color)
                text_rect = text.get_rect()
                text_rect.center = (Kart.__screen_size[0]//2, Kart.__screen_size[1]//2)  # Adjust the position as needed
                screen.blit(text, text_rect)

                font = pygame.font.SysFont(None, size=40)  # You can adjust the size as needed
                text = font.render(("Best time: %4i steps" % self.__best_time), True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.center = (Kart.__screen_size[0]//2, Kart.__screen_size[1]//2+100)  # Adjust the position as needed
                screen.blit(text, text_rect)

            #logger.debug("Kart number %i: accel: %s ; velocity(norm): %s ; velocity : %s ", self.__id, self.__acceleration, np.linalg.norm(self.__velocity), self.__velocity)

            self.__position = self.__position.astype(float)
            


            #Bound the position to the screen. Account for the position being the top left of the rectangle. Adapt if switching from rec to pic maybe.
            if (self.__position[0] + self.__velocity[0]>0. and self.__position[0] + self.__velocity[0] < Kart.__screen_size[0]):
                self.__position[0] += self.__velocity[0]
            else:
                self.reset(self.__checkpoint_pos, self.__checkpoint_orient, np.NaN)
                return
            if (self.__position[1] + self.__velocity[1]>0. and self.__position[1] + self.__velocity[1] < Kart.__screen_size[1]):
                self.__position[1] = self.__position[1] + self.__velocity[1]
            else:
                self.reset(self.__checkpoint_pos, self.__checkpoint_orient, np.NaN)
                return
            
            
            
            self.__acceleration_c = 0
        pass
    
    def draw(self, screen):

        kart_position = np.copy(self.__position)

        #IF NONE OF THE TEXTURES HAVE BEEN LOADED, LOAD THEM:
        if (not self.__initialized):
            scale = 0.05

            Kart.__splash_screen = pygame.image.load("textures/splash_screen.jpg").convert()


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


            self.__initialized = True
            logger.debug("ID: %i, is ai? %s nbr of karts: %i", self.__id, self.controller.is_ai, Kart.nbr_of_karts_())
            if self.__id == Kart.nbr_of_karts_():
                Kart.__started = game.splash_screen(screen,Kart.__splash_screen, Kart.__started)
                self.reset(self.controller.initial_position, self.controller.initial_angle, -1)
            #self.__start_time = time.time_ns()

        #Figure out the orientation's cardinal direction, and blit the appropriate image. 
        # quadr = Common.quadrant(float(self.__orientation))
        vel_scale = 0

        if (np.linalg.norm(self.__velocity)>2 and np.linalg.norm(self.__velocity)<5):
            vel_scale = 1
        elif (np.linalg.norm(self.__velocity)>=5):
            vel_scale = 2

        output_texture = Kart.textures[self.__input-1][vel_scale]
        output_texture = pygame.transform.rotate(output_texture, -1* Common.RadToDegrees(self.__orientation))
        screen.blit(output_texture, (kart_position[0]-(output_texture.get_height()/2), kart_position[1]-(output_texture.get_width()/2)))

        if (not self.__controller.is_ai and Kart.__nbr_of_karts > 1):
            pygame.draw.circle(screen, (255,255,0), [self.__position[0], self.__position[1]-30], 5)

        if (self.__controller.is_ai):
            Vel_dir = self.__velocity / (max(np.abs(self.__velocity)) +1e-3)

            Ratio = max(min(np.linalg.norm(self.__velocity)*20, 230), 45)

            future_x = int(Ratio*Vel_dir[0])
            future_y = int(Ratio*Vel_dir[1])

            k = 0.5
            angle = 0.30 + 0.4 * (1 - np.exp(-k * np.linalg.norm(self.__velocity)))
            vec_scale = 1/1

            if np.linalg.norm(self.__velocity) < 2:
                    angle = 1.2 

            skew = (0.,0.)

            if self.__input == 3:
                skew = (1.,-1.) #pos is left
                vec_scale = 0.8
            elif self.__input == 2:
                skew = (-1.,1.) 
                vec_scale = 0.8

            pos_rotated_velocity_vector_x = int(vec_scale*int(future_x  * np.cos(angle+ skew[0]*0.2) - future_y * np.sin(angle+ skew[0]*0.2)))
            pos_rotated_velocity_vector_y = int(vec_scale*int(future_x * np.sin(angle+ skew[0]*0.2) + future_y * np.cos(angle+ skew[0]*0.2)))

            neg_rotated_velocity_vector_x = int(vec_scale*int(future_x * np.cos(-(angle+ skew[1]*0.2)) - future_y * np.sin(-(angle+ skew[1]*0.2))))
            neg_rotated_velocity_vector_y = int(vec_scale*int(future_x * np.sin(-(angle+ skew[1]*0.2)) + future_y * np.cos(-(angle+ skew[1]*0.2))))

            pygame.draw.circle(screen, (255, 255, 255), [future_x+self.__position[0],future_y+self.__position[1]], 2.0)
            pygame.draw.circle(screen, (255, 255, 255), [pos_rotated_velocity_vector_x+self.__position[0],pos_rotated_velocity_vector_y+self.__position[1]], 2.0)
            pygame.draw.circle(screen, (255, 255, 255), [neg_rotated_velocity_vector_x+self.__position[0],neg_rotated_velocity_vector_y+self.__position[1]], 2.0)

        self.__input = 0 

    def check_radar_speed(self,delta):
        braking = False
        radar_readings = []
        range_points = 10*int(np.linalg.norm(self.__velocity))
        if abs(delta) < 0.2 and (np.linalg.norm(self.__velocity) < 13.):
            return braking
        elif np.linalg.norm(self.__velocity) >= 15.:
            braking = True
            return braking
        elif abs(delta) > 1.2:
            braking = True
            return braking
        else:
            for i in range(1, range_points + 2):
                # Calculate the position of the point in front of the kart
                x_check = int(self.__position[0] + i * np.cos(self.__orientation))
                y_check = int(self.__position[1] + i * np.sin(self.__orientation))

                # Check if the calculated position is within the map boundaries
                if 0 <= x_check < self.__char_map.shape[0] and 0 <= y_check < self.__char_map.shape[1]:
                    # Read the value at the calculated position
                    block_value = self.__char_map[x_check, y_check]
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
        X = np.array(self.__position, dtype=np.int16)
        point = self.map[X[0]][X[1]]

        if point >= 101 and point <=104:
            f = Checkpoint.surface_type_()
            if point-100 > self.__checkpoint + 1:
                pass
            elif point-100 > self.__checkpoint:
                self.__checkpoint = point-100
                self.__checkpoint_pos = np.copy(self.__position)
                self.__checkpoint_orient = np.copy(self.__orientation)

            return 'ap',boosting, f 

        match point:
            case  0:
                f = Grass.surface_type_()
                return 'ap',boosting, f
            case 200:
                boosting = True
                f = Boost.surface_type_()
                return 'ap',boosting, f
            case _:
                f = Road.surface_type_()
                return 'a',boosting, f
        
    def radar_points(self):
        dist_min_y = 150
        dist_min_x = 70

        #x is forward
        #y is right 

        p = self.path[0] 
        px = float(p[0])
        py = float(p[1])

        obj_vec = np.array([px - self.__position[0], py - self.__position[1]]) #Kart to object

        X = np.array(self.__position, dtype=np.int16)
        point = self.map[int(px)][int(py)]
        if point >= 101 and point <=104:
            if point-100 > self.__checkpoint+1:
                pass
            elif point-100 > self.__checkpoint:
                return

        #We now compute the Kart to object vector in the Kart frame
        obj_vec_K = np.array([obj_vec[0] * np.cos(-1*self.__orientation) - obj_vec[1]*np.sin(-1*self.__orientation), obj_vec[0]*np.sin(-1*self.__orientation) + obj_vec[1] * np.cos(-1*self.__orientation)])
        
        #Ellipse equation 
        #obj_vec_K[0]**2/(dist_min_x**2) + obj_vec_K[1]**2/(dist_min_y**2)<= 1
        
        #If the point is inside that ellipse, we'll delete it, as long as it isn't the last point. 
        if (obj_vec_K[0]**2/(dist_min_x**2) + obj_vec_K[1]**2/(dist_min_y**2)<= 1) and (p!=self.path[-1]):
            self.path.remove(p)

    def create_map(self,useable_array):
        self.map = useable_array

    def update_pos_AI(self):
        _, boosting,f = self.read_map()
        theta_v = math.atan2(self.__velocity[1], self.__velocity[0])
        self.__acceleration = self.__acceleration_c - (f * np.linalg.norm(self.__velocity) * np.cos(self.__orientation - theta_v))
        vel = self.__acceleration + np.linalg.norm(self.__velocity) 
        
        if (not boosting):
                self.__velocity = (vel * np.cos(self.__orientation), vel*np.sin(self.__orientation))
        else:
                self.__velocity = (BOOST_SPEED * np.cos(self.__orientation), BOOST_SPEED*np.sin(self.__orientation))
                        
        if (self.__position[0] + self.__velocity[0]>0. and self.__position[0] + self.__velocity[0] < np.shape(self.map)[0]):
                self.__position[0] += self.__velocity[0]
        else:
            self.reset(self.__checkpoint_pos, self.__checkpoint_orient, np.NaN)
            logger.warn("Exited boundary")
            # raise Exception("Exited boundary")
        
        if (self.__position[1] + self.__velocity[1]>0. and self.__position[1] + self.__velocity[1] < np.shape(self.map)[1]):
            self.__position[1] = self.__position[1] + self.__velocity[1]
        else:
            self.reset(self.__checkpoint_pos, self.__checkpoint_orient, np.NaN)
            logger.warn("Exited boundary")
            # raise Exception("Exited boundary")


        logger.debug("MAP SIZE: %s", np.shape(self.__char_map))

        self.__acceleration_c = 0       
        pass