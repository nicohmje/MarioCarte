import numpy as np
# import matplotlib.pyplot as plt
# from typing import NamedTuple
# import random
# import time
# import math
from Mapping import mapping
from kart import Kart
import pygame

# track_string = """GGGGGGGGGGGGGGGGGGGGGGGGGG
# GRRRRRRCRRRRRRRRRBRRRRRRRG
# GRRRRRRCRRRRRRRRRBRRRRRRRG
# GRRRRRRCRRRRRRRRRRRRRRRRRG
# GRRRRRRCRRRRRRRRRRRRRRRRRG
# GGGGGGGGGGGGGGGGGGGGGRRRRG
# GGGGGGGGGGGGGGGGGGGGGRRRRG
# GRRRRGGGGGGGGGGGGGGGGRRRRG
# GFFRRGGGGGGGGGGGGGGGGRRRRG
# GLRRRGGGGGGGGGGGGGGGGRRRRG
# GRRRRGGGGGGGGGGGGGGGGDDDDG
# GRRRRRERRRRRRRBRRRRRRRRLLG
# GRRRRRERRRRRRRBRRRRRRRRRRG
# GLRRRRERRRRRGGBRRRRRRRRRRG
# GLLRRRERRRRRGGBRRRRRRRRRRG
# GGGGGGGGGGGGGGGGGGGGGGGGGG"""

# track_string = """GGGGGG
# GRRRRG
# GRRRRG
# GRRRRG
# GRRRRG
# GCCCCG
# GRRRRG
# GRRRRG
# GRRRBG
# GRRRRG
# GDDDDG
# GRRRRG
# GEEEEG
# GRRRRG
# GRRRRG
# GFFFFG
# GGGGGG"""

class AI_PARSE():  

    
    def __init__(self, track_string,initial_position, initial_angle):

        self.track_string = track_string
        self.pos_ini = initial_position
        self.angle_ini = -1*initial_angle + np.pi/2.

        AI_PARSE.need_to_map = False
        try:
            track_string_file = np.load('track_string.npy')
        except:
            np.save('track_string.npy', np.array(self.track_string))
            print("[INFO] STARTED MAPPING")
            AI_PARSE.track, AI_PARSE.path = mapping(track_string)
        else: 
            track_string_file = np.load('track_string.npy')
            print("[INFO] LOADED STRING")
            if (track_string_file == track_string):
                print('[INFO] TRACK STRING HAS NOT CHANGED')
                try:   

                    self.command = np.load("ai_commands.npy")
                except:
                    print("[INFO] AI COMMANDS NOT FOUND")
                    AI_PARSE.need_to_map = True
                else:
                    self.command = np.load("ai_commands.npy")
                    print("[INFO] LOADED COMMANDS")
            else: 
                print('[INFO] TRACK STRING HAS CHANGED')
                AI_PARSE.need_to_map = True
                


        # plt.imshow(track)
        # plt.show()
        # fig, ax = plt.subplots()
        # print(path)

        if (AI_PARSE.need_to_map):
            print("[INFO] STARTED MAPPING")
            AI_PARSE.track, AI_PARSE.path = mapping(track_string)
            print(np.shape(AI_PARSE.path))
            self.command = []
            self.command.append([True, False, False, False])
            self.largeur = AI_PARSE.track.shape[1]
            self.hauteur = AI_PARSE.track.shape[0]
            
            self.kart = Kart(AI_PARSE.path)
            self.kart.create_map(AI_PARSE.track)
            self.kart.reset(self.pos_ini,self.angle_ini) 
            self.kart.path = AI_PARSE.path 


        

    def parse(self):

        # if len(self.command) > 2:
            
        #     return

        print("[INFO] STARTED FINDING PATH FOR AI")
        success = False
        step = 0
        x = []
        y = [] 
        while (not(success)):
            
            commanded_keys = [False, False, False, False]

            #Orientation control
            print(np.shape(AI_PARSE.path))
            obj_pos = AI_PARSE.path[0]
            px = float(obj_pos[0])
            py = float(obj_pos[1])
            next_theta, _ = self.calculate_angle(self.kart.position,[px,py])
            delta = next_theta - self.kart.orientation
            if delta>np.pi:
                delta = delta - 2*np.pi

            elif delta < -1*np.pi:
                delta =  2*np.pi + delta 

            if np.abs(delta) > 0.02:
                if delta >= 0:
                    self.kart.turn_right()
                    commanded_keys[-1] = True 
                elif delta < 0:
                    self.kart.turn_left()
                    commanded_keys[-2] = True

            braking = self.kart.check_radar_speed(delta)
            
            #Speed control
            if braking :
                self.kart.backward()
                commanded_keys[1] = True
            else:
                self.kart.forward()
                commanded_keys[0] = True
                
            self.command.append(commanded_keys)
            self.kart.update_pos_AI()
            self.kart.radar_points()
            x_ = int(np.copy(self.kart.position[0]))
            y_ = int(np.copy(self.kart.position[1]))
            x.append(-1*self.kart.position[0])
            y.append(self.kart.position[1])

            if self.kart.map[x_][y_]==104:
                success = True
                print('Successfully finished the map')
                break
            step +=1
        np.save('ai_commands.npy', np.array(self.command))
        AI_PARSE.need_to_map = False

    def move(self,step):
        # self.step+=1
        if step >= len(self.command):
            cmd =  [True, False, False, False]
        else:
            cmd = self.command[step]

        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        keys = {key: cmd[i] for i, key in enumerate(key_list)}
        return keys
    
    def calculate_angle(self,start_point, end_point):
    
        vector = end_point - start_point
        angle = np.arctan2(vector[1], vector[0])
        norm = np.linalg.norm(vector)
        
        return angle,norm

# ax.imshow(track, extent=[0, largeur, -1*hauteur, 0])



#Definition of kart's position and orientation
# pos_ini = np.array([150.,150.])
# angle_ini = np.pi/2.
# f = 0.02
# #Definition of accelerations
# MAX_ANGLE_VELOCITY = 0.05
# MAX_ACCELERATION = 0.25
# BOOST_SPEED = 25.


# class Kart():
    
#     f = 0.02
    
#     def __init__(self,path):
        
#         self.position = np.array([30.,20.])    
#         # print(self.position)   
#         self.orientation = 0.
#         self.velocity = np.array([0.,0.])
#         self.acceleration = 0.
#         self.acceleration_c = 0.
#         self.checkpoint = 0 
#         self.start_time = time.time_ns()
#         self.map = np.array([])
#         self.success = False
#         self.reset_nbr = 0
#         self.path = path
        
#     def create_map(self,useable_array):
#         self.map = useable_array
        
#     def forward(self):
#         self.acceleration_c += MAX_ACCELERATION
        
    
#     def backward(self):
#         self.acceleration_c += -MAX_ACCELERATION
        
    
#     def turn_left(self):
#         self.orientation = self.orientation - MAX_ANGLE_VELOCITY
        
        
#     def turn_right(self):
#         self.orientation = self.orientation + MAX_ANGLE_VELOCITY
        
    
#     def read_map(self):
#         boosting = False
#         X = np.array(self.position, dtype='int')

#         if self.map[X[0]][X[1]] == 200:
#             boosting = True
#             return 'ap',boosting
        
#         else:
#             return 'a',boosting

#     def check_radar_speed(self,delta):
#         braking = False
#         radar_readings = []
#         range_points = 10*int(np.linalg.norm(self.velocity))
#         if delta < 0.2 and (np.linalg.norm(self.velocity) < 15.):
#             return braking
#         elif np.linalg.norm(self.velocity) >= 15.:
#             braking = True
#             return braking
#         elif np.absolute(delta) > 0.6:
#             braking = True
#             return braking
        

#         else:

#             for i in range(1, range_points + 2):
#                 # Calculate the position of the point in front of the kart
#                 x_check = int(self.position[0] + i * np.cos(self.orientation))
#                 y_check = int(self.position[1] + i * np.sin(self.orientation))

#                 # Check if the calculated position is within the map boundaries
#                 if 0 <= x_check < self.map.shape[0] and 0 <= y_check < self.map.shape[1]:
#                     # Read the value at the calculated position
#                     block_value = self.map[x_check, y_check]
#                     radar_readings.append(block_value)
#                 else:
#                     # If the position is outside the map, consider it as a wall
#                     radar_readings.append(0)
            
#             sr = set(radar_readings)
#             if (sr.intersection([0]) == set([0])):
#                 braking = True
#                 return braking
#             else:
#                 return braking

    
#     def radar_points(self):
        
#         dist_min = 100
#         for p in self.path:
#             px = float(p[0])
#             py = float(p[1])
#             dx = self.position[0] - px
#             dy = self.position[1] - py
#             dist = np.sqrt(dx**2 + dy**2)
#             if (dist<dist_min) and (p!=(450,150)) :
#                 self.path.remove(p)
#                 # print('removed :',p)


                
        

#     def reset(self, initial_position, initial_orientation):
#         self.position = np.copy(initial_position)
#         self.orientation = np.copy(initial_orientation)        
#         self.velocity = np.array([0.,0.])
#         self.checkpoint = 0
#         self.reset_nbr += 1

#         pass
    
#     def update_pos(self):
#         _, boosting = self.read_map()
#         theta_v = math.atan2(self.velocity[1], self.velocity[0])
#         self.acceleration = self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v))
#         vel = self.acceleration + np.linalg.norm(self.velocity) 
        
#         if (not boosting):
#                 self.velocity = (vel * np.cos(self.orientation), vel*np.sin(self.orientation))
#         else:
#                 self.velocity = (BOOST_SPEED * np.cos(self.orientation), BOOST_SPEED*np.sin(self.orientation))
                        
#         self.position[0]+= self.velocity[0]
#         self.position[1]+= self.velocity[1]
#         self.acceleration_c = 0       
#         pass






# fig, ax = plt.subplots()




# largeur = track.shape[1]
# hauteur = track.shape[0]

# # ax.imshow(track, extent=[0, largeur, -1*hauteur, 0])




# return command


#print(command)
# ax.plot(y, x, color='red')
# plt.show()

        


