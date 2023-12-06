import numpy as np
import matplotlib.pyplot as plt
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
        lava_pos = ()
        lava_pos_l = ()
        lava_pos_r = ()
        intersect = False
        distance = 0
        while (not(success)):
            
            
            # if (len(lava_pos) >0):
            #     plt.figure()
            #     plt.ylim(-300,0)
            #     plt.xlim(0,1650)
            #     plt.scatter(self.kart.position[1], -self.kart.position[0])
            #     plt.scatter(lava_pos[1],-lava_pos[0], color='red')
            #     plt.show()
            #     time.sleep(0.1)
            #     plt.close()
            
            commanded_keys = [False, False, False, False]

            #Orientation control
            #logger.debug(np.shape(AI_PARSE.path))

            obj_pos = AI_PARSE.path[0]
            px = float(obj_pos[0])
            py = float(obj_pos[1])
            next_theta, _ = self.calculate_angle(self.kart.position,[px,py])

            cur_pos_x = int(self.kart.position[0])
            cur_pos_y = int(self.kart.position[1])
            

            Vel_dir = self.kart.velocity / (max(np.abs(self.kart.velocity)) + 1e-3)

            Ratio = max(min(np.linalg.norm(self.kart.velocity)*13, 200), 55)

            logger.debug(Vel_dir)
            logger.debug(Ratio)

            future = np.array([Ratio*Vel_dir[0], Ratio*Vel_dir[1]], dtype=np.int16) 

            try:
                future_point = self.kart.map[future[0]+cur_pos_x][future[1]+cur_pos_y]
            except:
                pass


            pos_rotated_velocity_vector = np.array([int(future[0]  * np.cos(0.65) - future[1] * np.sin(0.65)),int(future[0] * np.sin(0.65) + future[1] * np.cos(0.65))])

            neg_rotated_velocity_vector = np.array([int(future[0] * np.cos(-0.65) - future[1] * np.sin(-0.65)), int(future[0] * np.sin(-0.65) + future[1] * np.cos(-0.65))])

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


            lava_front, distance_front = self.lava_along_vector(future)
            lava_left, distance_left = self.lava_along_vector(pos_rotated_velocity_vector)
            lava_right, distance_right = self.lava_along_vector(neg_rotated_velocity_vector)

            
            if lava_front:
                lava_pos = ((future/np.linalg.norm(future)) * distance_front) + self.kart.position
            if lava_left:
                lava_pos_l = ((future/np.linalg.norm(future)) * distance_left) + self.kart.position
            if lava_right:
                lava_pos_r = ((future/np.linalg.norm(future)) * distance_right) + self.kart.position


            logger.debug("pos X %i", cur_pos_x)  
            logger.debug("pos Y %i", cur_pos_y)
            logger.debug("CURRENT POINT %i", current_point)
            logger.debug("CURRENT VEL %d", np.linalg.norm(self.kart.velocity))


            logger.debug("future X %i", future[0]+cur_pos_x)  
            logger.debug("future Y %i", future[1]+cur_pos_y)
            logger.debug("FUTURE POINT %i", future_point)

            logger.debug("onject X %i", px)
            logger.debug("object Y %i", py)
            logger.debug("delta %f", delta)

            logger.debug("FUTURE ROTATED pos POINT %i", pos_future_rotated_point)
            logger.debug("FUTURE ROTATED Neg POINT %i", neg_future_rotated_point)

            logger.debug("lava along front: %s", lava_front)
            logger.debug("lava along left: %s", lava_left)
            logger.debug("lava along right: %s", lava_right)

            logger.debug("Lava position (front) %s", lava_pos)
            logger.debug("Lava position (left) %s", lava_pos_l)
            logger.debug("Lava position (right) %s", lava_pos_r)



            if (lava_front):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING") 
                if (delta<0 and lava_right):
                    braking = True
                    logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
                elif (delta>0 and lava_left):
                    braking = True
                    logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")           
            elif (lava_right and delta<0):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
            elif (lava_left and delta>0):
                braking = True
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
            
            if len(lava_pos)>0:
                intersect, intersection_point = self.line_intersects_circle(self.kart.position, future, lava_pos)
                distance = np.sqrt((intersection_point[0]-cur_pos_x)**2 + (intersection_point[1]-cur_pos_y)**2)

            if (len(lava_pos)>0 and intersect and distance<40):
                logger.debug('INTERSECTION WITH LAVA')
                logger.debug("Lava pos: %s", lava_pos)
                if lava_right and lava_left:
                    delta = 0.5 * np.sign(delta)
                elif lava_right and not lava_left:
                    delta = +0.5
                elif lava_left and not lava_right: 
                    delta = -0.5
                else:
                    delta = (+0.5, -0.5)[pos_future_rotated_point<neg_future_rotated_point]



            if np.abs(delta) > 0.02:
                if delta >= 0:
                    self.kart.turn_right() # WHICH MEANS TURN LEFT (for some reason)
                    commanded_keys[-1] = True 
                elif delta < 0:
                    self.kart.turn_left() # WHICH MEANS TURN RIGHT (for some reason)
                    commanded_keys[-2] = True
            
            
            #Speed control
            if braking:
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
                time.sleep(2)
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
                        return True, i
                except:
                    pass
        return False, 1e9
    
    def line_intersects_circle(self, X, vector, circle_center, circle_radius=10):
        
        #Ref mathworld.worldfram.com Circle-Line Intersection
        #we have our circle in circle_center, so we can simply subtract that

        x1 = X[0] - circle_center[0]
        y1 = X[1] - circle_center[1]

        x2 = vector[0] + X[0] - circle_center[0]
        y2 = vector[1] + X[1] - circle_center[1]

        dx = x2 - x1
        dy = y2 - y1

        dr = np.sqrt(dx**2 + dy**2)

        D = x1*y2 - x2*y1
        
        discriminant = circle_radius**2 * dr**2 - D**2

        if discriminant >= 0:
            intersect_x_1 =  (D*dy + np.sign(dy) * dx * np.sqrt(discriminant)) / dr**2
            intersect_x_2 =  (D*dy - np.sign(dy) * dx * np.sqrt(discriminant)) / dr**2

            intersect_y_1 =  (-1*D*dx + np.abs(dy) * np.sqrt(discriminant)) / dr**2
            intersect_y_2 =  (-1*D*dx - np.abs(dy) * np.sqrt(discriminant)) / dr**2

            intersect_vector1 = np.array([intersect_x_1 - x1, intersect_y_1 - y1])
            intersect_vector2 = np.array([intersect_x_2 - x1, intersect_y_2 - y1])

            if (np.linalg.norm(intersect_vector1) < np.linalg.norm(intersect_vector2)):
                return True, (intersect_x_1+circle_center[0], intersect_y_1+circle_center[1])
            else:
                return True, (intersect_x_2+circle_center[0], intersect_y_2+circle_center[1])
        else: 
            return False, (1e9,1e9)

    
    def calculate_angle(self,start_point, end_point):
    
        vector = end_point - start_point
        angle = np.arctan2(vector[1], vector[0])
        norm = np.linalg.norm(vector)
        
        return angle,norm
