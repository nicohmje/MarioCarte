import numpy as np
# import matplotlib.pyplot as plt
# from typing import NamedTuple
# import random
import time
# import math
from Mapping import mapping
from kart import Kart
import pygame
import os
import logging

logger = logging.getLogger('MariooCarteLogger')

class AI_PARSE():  

    
    def __init__(self, track_string,initial_position, initial_angle):

        self.track_string = track_string
        self.pos_ini = initial_position
        self.angle_ini = -1*initial_angle + np.pi/2.
        self.f = 0.02

        AI_PARSE.need_to_map = False
        try:
            track_string_file = np.load('track_string.npy')
            logger.info("LOADED STRING")
            if (track_string_file == track_string):
                logger.info('TRACK STRING HAS NOT CHANGED')
                try:   
                    self.command = np.load("ai_commands.npy")
                    logger.info("LOADED COMMANDS")
                except:
                    logger.info("AI COMMANDS NOT FOUND")
                    AI_PARSE.need_to_map = True                    
            else: 
                logger.info('TRACK STRING HAS CHANGED')
                os.remove("ai_commads.npy")
                os.remove("track_string.npy")
                np.save('track_string.npy', np.array(self.track_string))
                AI_PARSE.need_to_map = True
        except:
            np.save('track_string.npy', np.array(self.track_string))
            AI_PARSE.need_to_map = True
            
                


        # plt.imshow(track)
        # plt.show()
        # fig, ax = plt.subplots()
        # logger.debug(path)

        if (AI_PARSE.need_to_map):
            logger.info("STARTED MAPPING")
            AI_PARSE.track, AI_PARSE.path = mapping(track_string)
            # logger.debug("NP SHAPE PATH")
            # logger.debug(np.shape(AI_PARSE.path))
            self.command = []
            self.command.append([True, False, False, False])
            self.largeur = AI_PARSE.track.shape[1]
            self.hauteur = AI_PARSE.track.shape[0]
            
            self.kart = Kart(AI_PARSE.path)
            self.kart.create_map(AI_PARSE.track)
            self.kart.reset(self.pos_ini,self.angle_ini) 
            self.kart.path = AI_PARSE.path 


        

    def parse(self):

        logger.info("STARTED FINDING PATH FOR AI")
        success = False
        step = 0
        x = []
        y = [] 
        while (not(success)):
            
            commanded_keys = [False, False, False, False]

            #Orientation control
            #logger.debug(np.shape(AI_PARSE.path))

            obj_pos = AI_PARSE.path[0]
            px = float(obj_pos[0])
            py = float(obj_pos[1])
            next_theta, _ = self.calculate_angle(self.kart.position,[px,py])

            cur_pos_x = int(self.kart.position[0])
            cur_pos_y = int(self.kart.position[1])

            future = np.array([20*self.kart.velocity[0], 20*self.kart.velocity[1]], dtype=np.int16) 

            try:
                future_point = self.kart.map[future[0]+cur_pos_x][future[1]+cur_pos_y]
            except:
                pass



            pos_rotated_velocity_vector = np.array([int(future[0]  * np.cos(0.40) - future[1] * np.sin(0.40)),int(future[0] * np.sin(0.40) + future[1] * np.cos(0.40))])

            neg_rotated_velocity_vector = np.array([int(future[0] * np.cos(-0.40) - future[1] * np.sin(-0.40)), int(future[0] * np.sin(-0.40) + future[1] * np.cos(-0.40))])

            try:
                pos_future_rotated_point = self.kart.map[pos_rotated_velocity_vector[0]+cur_pos_x][pos_rotated_velocity_vector[1]+cur_pos_y]      
            except:
                pass
                


            try:
                neg_future_rotated_point = self.kart.map[neg_rotated_velocity_vector[0]+cur_pos_x][neg_rotated_velocity_vector[1]+cur_pos_y]
            except:
                pass

            current_point = self.kart.map[int(cur_pos_x)][int(cur_pos_y)]

            delta = next_theta - self.kart.orientation
            if delta>np.pi:
                delta = delta - 2*np.pi

            elif delta < -1*np.pi:
                delta =  2*np.pi + delta 


            braking = self.kart.check_radar_speed(delta)


            logger.debug("pos X %i", cur_pos_x)  
            logger.debug("pos Y %i", cur_pos_y)
            logger.debug("CURRENT POINT %i", current_point)

            logger.debug("future X %i", future[0]+cur_pos_x)  
            logger.debug("future Y %i", future[1]+cur_pos_y)
            logger.debug("FUTURE POINT %i", future_point)

            logger.debug("onject X %i", px)
            logger.debug("object Y %i", py)
            logger.debug("NEXT THETA %f", delta)

            logger.debug("rotated pos X %i", pos_rotated_velocity_vector[0])
            logger.debug("rotated pos Y %i", pos_rotated_velocity_vector[1])
            logger.debug("FUTURE ROTATED pos POINT %i", pos_future_rotated_point)

            logger.debug("rotated neg X %i", neg_rotated_velocity_vector[0])
            logger.debug("rotated neg Y %i", neg_rotated_velocity_vector[1])
            logger.debug("FUTURE ROTATED Neg POINT %i", neg_future_rotated_point)

            logger.debug("lava along front: %s", self.lava_along_vector(future))
            logger.debug("lava along left: %s", self.lava_along_vector(neg_rotated_velocity_vector))
            logger.debug("lava along right: %s", self.lava_along_vector(pos_rotated_velocity_vector))

            if (self.lava_along_vector(future)):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING") 
                if (delta<0 and self.lava_along_vector(pos_rotated_velocity_vector)):
                    braking = True
                    logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
                elif (delta>0 and self.lava_along_vector(neg_rotated_velocity_vector)):
                    braking = True
                    logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
                    
            elif (self.lava_along_vector(pos_rotated_velocity_vector) and delta<0):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
            elif (self.lava_along_vector(neg_rotated_velocity_vector) and delta>0):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
                




            # if (logger.level < 11):
            #     time.sleep(0.04)



            if np.abs(delta) > 0.02:
                if delta >= 0:
                    self.kart.turn_right()
                    commanded_keys[-1] = True 
                elif delta < 0:
                    self.kart.turn_left()
                    commanded_keys[-2] = True
            
            
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
                logger.info('Successfully finished the map')
                break
            elif self.kart.map[x_][y_] == 10:
                logger.info("LAVA")
            step +=1
        
        np.save('ai_commands.npy', np.array(self.command))
        AI_PARSE.need_to_map = False

    def move(self,step):
        if step >= len(self.command):
            cmd =  [True, False, False, False]
        else:
            cmd = self.command[step]

        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        keys = {key: cmd[i] for i, key in enumerate(key_list)}
        return keys
    
    def lava_along_vector(self, vector):
        for i in range(int(np.linalg.norm(vector))+1):
                normalized = i/(int(np.linalg.norm(vector))+1e-3)
                along_line = np.array(self.kart.position + normalized*vector, dtype=np.int16) 
                try: 
                    if (self.kart.map[along_line[0]][along_line[1]] == 10):
                        return True
                except:
                    pass
        return False
    
    def calculate_angle(self,start_point, end_point):
    
        vector = end_point - start_point
        angle = np.arctan2(vector[1], vector[0])
        norm = np.linalg.norm(vector)
        
        return angle,norm
