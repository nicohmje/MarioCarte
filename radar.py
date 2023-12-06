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
                os.remove("ai_commands.npy")
                os.remove("track_string.npy")
                np.save('track_string.npy', np.array(self.track_string))
                AI_PARSE.need_to_map = True
        except:
            np.save('track_string.npy', np.array(self.track_string))
            track_string_file = str("john")
            AI_PARSE.need_to_map = True
            
                


        # plt.imshow(track)
        # plt.show()
        # fig, ax = plt.subplots()
        # logger.debug(path)

        if (AI_PARSE.need_to_map):
            logger.info("STARTED MAPPING")
            if (track_string_file == track_string):
                logger.info("TRYING TO LOAD TRACK AND PATH")
                if os.path.isfile("track.npy") and os.path.isfile("path.txt"):
                    AI_PARSE.track = np.load("track.npy")
                    logger.info("Loaded previous track")
                    AI_PARSE.path = []
                    with open(r'path.txt', 'r') as fp:
                        for line in fp:
                            x = line
                            AI_PARSE.path.append(eval(x))
                    fp.close()
                    logger.info("Loaded previous path")
                    logger.info("Loaded previous mapping")
                else:
                    AI_PARSE.track, AI_PARSE.path = mapping(track_string)
                    np.save("track.npy", AI_PARSE.track)
                    with open(r'path.txt', 'w') as fp:
                        fp.write("\n".join(str(item) for item in AI_PARSE.path))
                    fp.close()
            else:
                logger.debug("TRACK STRING HAS CHANGED")
                if (os.path.exists("track.npy")):  
                    os.remove("track.npy")
                if (os.path.exists("path.txt")):
                    os.remove("path.txt")
                AI_PARSE.track, AI_PARSE.path = mapping(track_string)
                np.save("track.npy", AI_PARSE.track)
                with open(r'path.txt', 'w') as fp:
                        fp.write("\n".join(str(item) for item in AI_PARSE.path))
                fp.close()   
            # logger.debug("NP SHAPE PATH")
            # logger.debug(np.shape(AI_PARSE.path))

            logger.info("Number of points (A*): %s", np.shape(AI_PARSE.path))
            self.command = []
            self.command.append([False, False, False, False])
            self.largeur = AI_PARSE.track.shape[1]
            self.hauteur = AI_PARSE.track.shape[0]
            
            self.kart = Kart(AI_PARSE.path)

            logger.debug("TRACK ARRAY %s", AI_PARSE.track[140:145,153:158])

            self.kart.create_map(AI_PARSE.track)
            self.kart.reset(self.pos_ini,self.angle_ini) 
            self.kart.path = AI_PARSE.path 


        

    def parse(self):

        logger.info("STARTED FINDING PATH FOR AI")
        success = False
        step = 0
        # x = []
        # y = [] 
        lava_pos = ()
        lava_pos_l = ()
        lava_pos_r = ()
        intersect = False
        distance = 0

        turning_left, turning_right = False, False

        while (not(success)):
            
            commanded_keys = [False, False, False, False]

            obj_pos = AI_PARSE.path[0]
            logger.debug("LENGTH AI PARSE PATH %i", len(AI_PARSE.path))
            px = float(obj_pos[0])
            py = float(obj_pos[1])
            next_theta, _ = self.calculate_angle(self.kart.position,[px,py])

            cur_pos_x = (self.kart.position[0])
            cur_pos_y = (self.kart.position[1])
            

            normalized_velocity = self.kart.velocity / (max(np.abs(self.kart.velocity)) + 1e-3)
            velocity_norm = np.linalg.norm(self.kart.velocity)

            Ratio = max(min(velocity_norm*20, 250), 35)

            logger.debug(normalized_velocity)
            logger.debug(Ratio)
            

            #This is the future point, which the kart will reach if keeps going straight

            future = np.array([Ratio*normalized_velocity[0], Ratio*normalized_velocity[1]], dtype=np.int16) 

            try:
                future_point = self.kart.map[int(future[0]+cur_pos_x)][int(future[1]+cur_pos_y)]
            except:
                pass

            diydar_lava_front, dist_to_lava_diydar = self.diydar(future)

            if dist_to_lava_diydar > 1e3:
                dist_to_lava_diydar = 0.

            k = 0.3

            angle = 0.30 + 0.4 * (1 - np.exp(-k * np.linalg.norm(self.kart.velocity)))


            if velocity_norm < 1.5:
                angle = 1.2

            logger.debug("ANGLE %f", angle)

            scale = 1. 

            skew = (0.,0.)

            if turning_left:
                skew = (1.,-1.) #pos is left
            elif turning_right:
                skew = (-1.,1.)


            pos_rotated_velocity_vector = np.array([int(scale*((future[0]  * np.cos(angle + skew[0]*0.2)) - future[1] * np.sin(angle+ skew[0]*0.2))),int(scale*(future[0] * np.sin(angle+ skew[0]*0.2) + future[1] * np.cos(angle+ skew[0]*0.2)))])

            neg_rotated_velocity_vector = np.array([(int(scale*(future[0] * np.cos(-(angle+ skew[1]*0.2)) - future[1] * np.sin(-(angle+ skew[1]*0.2))))), int(scale*(future[0] * np.sin(-(angle+ skew[1]*0.2)) + future[1] * np.cos(-(angle+ skew[1]*0.2))))])


            
            pos_future_rotated_point = self.min_along_vector(pos_rotated_velocity_vector)
            if pos_future_rotated_point == 0:
                pos_future_rotated_point = 15
            elif pos_future_rotated_point>=100 and pos_future_rotated_point<=105:
                pos_future_rotated_point = 1000

            neg_future_rotated_point = self.min_along_vector(neg_rotated_velocity_vector)
            if neg_future_rotated_point == 0:
                neg_future_rotated_point = 15
            elif neg_future_rotated_point>=100 and neg_future_rotated_point<=105:
                neg_future_rotated_point = 1000
            
            
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

            # logger.debug("MAP %s", self.kart.map[140:145,153:158])
            # logger.debug("TRACK %s", AI_PARSE.track[140:145,153:158])

            if lava_front and distance_front < 1e4:
                lava_pos = ((future/np.linalg.norm(future)) * distance_front) + self.kart.position
            elif lava_left and distance_left < 1e4:
                lava_pos = ((pos_rotated_velocity_vector/np.linalg.norm(pos_rotated_velocity_vector)) * distance_left) + self.kart.position
            elif lava_right and distance_right < 1e4:
                lava_pos = ((neg_rotated_velocity_vector/np.linalg.norm(neg_rotated_velocity_vector)) * distance_right) + self.kart.position

            

            
            logger.debug("POS X %i, POS Y %i", cur_pos_x,cur_pos_y)  
            logger.debug("POINT %i, CURRENT VEL %f", current_point, np.linalg.norm(self.kart.velocity))

            logger.debug("future X %i, future Y %i", future[0]+cur_pos_x, future[1]+cur_pos_y)  
            logger.debug("FUTURE POINT %i", future_point)

            logger.debug("object X %i, object Y %i", px, py)
            logger.debug("delta %f", delta)

            logger.debug("FUTURE ROTATED pos POINT %i, FUTURE ROTATED Neg POINT %i", pos_future_rotated_point, neg_future_rotated_point)

            logger.debug("lava along front: %s,Lava position (front) %s", lava_front,lava_pos)
            logger.debug("lava along front [DIYDAR]: %s", diydar_lava_front)
            logger.debug("lava along left: %s, Lava position (left) %s", lava_left, lava_pos_l)
            logger.debug("lava along right: %s, Lava position (right) %s", lava_right,lava_pos_r)

            sum = 0
            V_0 = velocity_norm

            for h in range(int(V_0/0.25)):
                sum += V_0 - h*0.25
            dist_to_stop = sum

            if len(lava_pos) >0:
                intersect, intersection_point = self.line_intersects_circle(self.kart.position, future, lava_pos)
                intersect_left, _ = self.line_intersects_circle(self.kart.position, pos_rotated_velocity_vector, lava_pos)
                intersect_right, _ = self.line_intersects_circle(self.kart.position, neg_rotated_velocity_vector, lava_pos)


                lava_vector = np.array([(lava_pos[0]-cur_pos_x), (lava_pos[1]-cur_pos_y)])
                distance = np.linalg.norm(lava_vector)

                angle_to_lava = np.arccos(np.dot(self.kart.velocity, lava_vector)/ (velocity_norm * distance))

                if abs(angle_to_lava)>1.75:
                    logger.debug("ANGLE TO LAVA: %f", angle_to_lava)
                    logger.debug("IGNORED LAVA")
                    lava_pos = ()


            else:
                intersect = False
                intersect_left = False
                intersect_right = False
  
        

            if (lava_front):
                braking = (True,False)[1.2*dist_to_stop<distance]
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING") 
            if (diydar_lava_front):
                braking = (True,False)[dist_to_stop<dist_to_lava_diydar]
                logger.debug("BRAKING DIYDAR BRAKING DIYDAR BRAKING DIYDAR BRAKING DIYDAR BRAKING DIYDAR BRAKING DIYDAR")    
            if ((lava_right or intersect_right)):
                delta = +0.5
                logger.debug("CHOICE2 %f", delta)
                braking = (True,False)[1.2*dist_to_stop<distance]
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
            elif ((lava_left or intersect_left)):
                delta = -0.5
                logger.debug("CHOICE3 %f", delta)
                braking = (True,False)[1.2*dist_to_stop<distance]
                logger.debug("BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING BRAKING")
            elif (len(lava_pos)>0 and intersect):
                logger.debug('INTERSECTION WITH LAVA')
                logger.debug("Lava pos: %s", lava_pos)
                logger.debug("Lava distance: %s", distance)

                if intersect_left and not intersect_right:
                    delta = -0.5
                    logger.debug("CHOICE4 %f", delta)
                elif intersect_right and not intersect_left:
                    delta = 0.5
                    logger.debug("CHOICE5 %f", delta)
                else:
                    delta += (+0.3, -0.3)[pos_future_rotated_point<neg_future_rotated_point]
                    logger.debug("CHOICE6 %f", delta)


            if np.abs(delta) > 0.02:
                if delta >= 0:
                    turning_left = True
                    turning_right = False
                    self.kart.turn_right() # WHICH MEANS TURN LEFT (for some reason)
                    commanded_keys[-1] = True 
                elif delta < 0:
                    turning_right = True
                    turning_left = False
                    self.kart.turn_left() # WHICH MEANS TURN RIGHT (for some reason)
                    commanded_keys[-2] = True
            else:
                turning_right, turning_left = False, False
            
            #Speed control
            if braking and velocity_norm > 0.3:
                self.kart.backward()
                commanded_keys[1] = True
            else:
                self.kart.forward()
                commanded_keys[0] = True
                
            self.command.append(commanded_keys)
            self.kart.update_pos_AI()
            self.kart.radar_points()
            x_ = (np.copy(self.kart.position[0]))
            y_ = (np.copy(self.kart.position[1]))
            # x.append(-1*self.kart.position[0])
            # y.append(self.kart.position[1])
            if self.kart.map[int(x_)][int(y_)]==104:
                success = True
                logger.info('Successfully finished the map')
                break
            elif self.kart.map[int(x_)][int(y_)] == 10:
                logger.info("LAVA")
                # time.sleep(2)

            # if step>150 and step<180:
            #      time.sleep(1.4)
            step +=1
        
        np.save('ai_commands.npy', np.array(self.command))
        AI_PARSE.need_to_map = False

    def move(self,step):
        if step >= len(self.command) or step < 0:
            cmd =  [True, False, False, False]
        else:
            cmd = self.command[step]

        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        keys = {key: cmd[i] for i, key in enumerate(key_list)}
        return keys
    
    def lava_along_vector(self, vector):
        for i in np.linspace(0,int(np.linalg.norm(vector)),20):
                normalized = i/(int(np.linalg.norm(vector))+1e-3)

                along_line = np.array(self.kart.position + normalized*vector, dtype=np.int16) 
                try: 
                    if (self.kart.map[along_line[0]][along_line[1]] == 10):
                        return True, i
                except:
                    pass
                    # return True, 1e9

        return False, 1e9
    
    def min_along_vector(self, vector):
        for i in range(int(np.linalg.norm(vector))+1):
                smallest = 1e9
                normalized = i/(int(np.linalg.norm(vector))+1e-3)
                along_line = np.array(self.kart.position + normalized*vector, dtype=np.int16) 
                try: 
                    if (self.kart.map[along_line[0]][along_line[1]] < smallest):
                        smallest = self.kart.map[along_line[0]][along_line[1]]
                except:
                    pass
        return (1, smallest)[smallest < 1e8]
    
    def line_intersects_circle(self, X, vector, circle_center, circle_radius=10):
        
        #Ref mathworld.worldfram.com Circle-Line Intersection
        #we have our circle in circle_center, so we can simply subtract that

        x1 = X[0] - circle_center[0]
        y1 = X[1] - circle_center[1]

        x2 = vector[0]*2 + X[0] - circle_center[0]
        y2 = vector[1]*2 + X[1] - circle_center[1]

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
    
    def diydar(self, future):
        for i in np.linspace(np.pi/10, np.pi/6, 6):
            vector = np.array([int(future[0]  * np.cos(i) - future[1] * np.sin(i)),int(future[0] * np.sin(i) + future[1] * np.cos(i))])

            lava_detected, distance = self.lava_along_vector(vector)

            if lava_detected:
                return lava_detected, distance
            
            hector = np.array([int(future[0]  * np.cos(-i) - future[1] * np.sin(-i)),int(future[0] * np.sin(-i) + future[1] * np.cos(-i))])
            
            lava_detected, distance = self.lava_along_vector(hector)

            if lava_detected:
                return lava_detected, distance

        return False, 50000

