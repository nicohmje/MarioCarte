import numpy as np
# import matplotlib.pyplot as plt
# from typing import NamedTuple
# import random
# import time
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
        except:
            np.save('track_string.npy', np.array(self.track_string))
            AI_PARSE.need_to_map = True
        else: 
            track_string_file = np.load('track_string.npy')
            logger.info("LOADED STRING")
            if (track_string_file == track_string):
                logger.info('TRACK STRING HAS NOT CHANGED')
                try:   

                    self.command = np.load("ai_commands.npy")
                except:
                    logger.info("AI COMMANDS NOT FOUND")
                    AI_PARSE.need_to_map = True
                else:
                    self.command = np.load("ai_commands.npy")
                    logger.info("LOADED COMMANDS")
            else: 
                logger.info('TRACK STRING HAS CHANGED')
                os.remove("track_string.npy")
                np.save('track_string.npy', np.array(self.track_string))
                AI_PARSE.need_to_map = True
                


        # plt.imshow(track)
        # plt.show()
        # fig, ax = plt.subplots()
        # logger.debug(path)

        if (AI_PARSE.need_to_map):
            logger.info("STARTED MAPPING")
            AI_PARSE.track, AI_PARSE.path = mapping(track_string)
            logger.debug(np.shape(AI_PARSE.path))
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
                logger.info('Successfully finished the map')
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
