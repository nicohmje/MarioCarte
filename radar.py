import numpy as np
import matplotlib.pyplot as plt
from typing import NamedTuple
import random
import time
import math
from Mapping import mapping






track_string = """GGGGGGGGGGGGGGGGGGGGGGGGGG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGRRRRG
GFFRRGGGGGGGGGGGGGGGGRRRRG
GLRRRGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGDDDDG
GRRRRRERRRRRRRBRRRRRRRRLLG
GRRRRRERRRRRRRBRRRRRRRRRRG
GLRRRRERRRRRGGBRRRRRRRRRRG
GLLRRRERRRRRGGBRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGGGGGG"""

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

track, path = mapping(track_string)
plt.imshow(track)
plt.show()
fig, ax = plt.subplots()
print(path)


pos_ini = np.array([150.,150.])
angle_ini = np.pi/2.
f = 0.02

### Initializing qtable :
largeur = track.shape[1]
hauteur = track.shape[0]

ax.imshow(track, extent=[0, largeur, -1*hauteur, 0])



#Definition of kart's position and orientation
pos_ini = np.array([150.,150.])
angle_ini = np.pi/2.
f = 0.02
#Definition of accelerations
MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25
BOOST_SPEED = 25.


class Kart():
    
    f = 0.02
    
    def __init__(self,path):
        
        self.position = np.array([30.,20.])    
        print(self.position)   
        self.orientation = 0.
        self.velocity = np.array([0.,0.])
        self.acceleration = 0.
        self.acceleration_c = 0.
        self.checkpoint = 0 
        self.start_time = time.time_ns()
        self.map = np.array([])
        self.success = False
        self.reset_nbr = 0
        self.path = path
        
    def create_map(self,useable_array):
        self.map = useable_array
        
    def forward(self):
        self.acceleration_c += MAX_ACCELERATION
        
    
    def backward(self):
        self.acceleration_c += -MAX_ACCELERATION
        
    
    def turn_left(self):
        self.orientation = self.orientation - MAX_ANGLE_VELOCITY
        
        
    def turn_right(self):
        self.orientation = self.orientation + MAX_ANGLE_VELOCITY
        
    
    def read_map(self):
        boosting = False
        X = np.array(self.position, dtype='int')

        if self.map[X[0]][X[1]] == 200:
            boosting = True
            return 'ap',boosting
        
        else:
            return 'a',boosting

            # match self.map[X[0]][X[1]]:
            #     case 255:
            #         return 'R',boosting
            #     case 101:
            #         if (self.checkpoint<1):
            #             self.checkpoint=1
            #             return 'X', boosting
            #         else: 
            #             return 'C',boosting
            #     case 102:
            #         if (self.checkpoint<2):
            #             self.checkpoint=2
            #             return 'Y', boosting
            #         else:
            #             return 'D',boosting
            #     case 103:
            #         if (self.checkpoint<3):
            #             self.checkpoint=3
            #             return 'Z', boosting
            #         else:
            #             return 'E', boosting
            #     case 104:
            #         self.success = True
            #         return 'F',boosting
            #     case 0:
            #         return 'G',boosting
            #     case 10:
            #         return 'A',boosting #stands for apex corner
            #     case 200:
            #         boosting = True
            #         return 'B',boosting
            #     case 5:
            #         return 'AS',boosting #stands for A star trajectory
            #     case 180:
            #         return 'ASP', boosting #stands for A star points
            
            

    def check_radar_speed(self,delta):
        braking = False
        radar_readings = []
        range_points = 10*int(np.linalg.norm(self.velocity))
        if delta < 0.2 and (np.linalg.norm(self.velocity) < 15.):
            return braking
        elif np.linalg.norm(self.velocity) >= 15.:
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
                if 0 <= x_check < self.map.shape[0] and 0 <= y_check < self.map.shape[1]:
                    # Read the value at the calculated position
                    block_value = self.map[x_check, y_check]
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

    
    def radar_points(self):
        
        dist_min = 100
        for p in self.path:
            px = float(p[0])
            py = float(p[1])
            dx = self.position[0] - px
            dy = self.position[1] - py
            dist = np.sqrt(dx**2 + dy**2)
            if (dist<dist_min) and (p!=(450,150)) :
                self.path.remove(p)
                print('removed :',p)


                
        

    def reset(self, initial_position, initial_orientation):
        self.position = np.copy(initial_position)
        self.orientation = np.copy(initial_orientation)        
        self.velocity = np.array([0.,0.])
        self.checkpoint = 0
        self.reset_nbr += 1

        pass
    
    def update_pos(self):
        _, boosting = self.read_map()
        theta_v = math.atan2(self.velocity[1], self.velocity[0])
        self.acceleration = self.acceleration_c - (f * np.linalg.norm(self.velocity) * np.cos(self.orientation - theta_v))
        vel = self.acceleration + np.linalg.norm(self.velocity) 
        
        if (not boosting):
                self.velocity = (vel * np.cos(self.orientation), vel*np.sin(self.orientation))
        else:
                self.velocity = (BOOST_SPEED * np.cos(self.orientation), BOOST_SPEED*np.sin(self.orientation))
                        
        self.position[0]+= self.velocity[0]
        self.position[1]+= self.velocity[1]
        self.acceleration_c = 0       
        pass



def calculate_angle(start_point, end_point):
    
    vector = end_point - start_point
    angle = np.arctan2(vector[1], vector[0])
    norm = np.linalg.norm(vector)
    
    return angle,norm


fig, ax = plt.subplots()




largeur = track.shape[1]
hauteur = track.shape[0]

ax.imshow(track, extent=[0, largeur, -1*hauteur, 0])
kart = Kart(path)
kart.create_map(track)
kart.reset(pos_ini,angle_ini)

success = False

command = []
command.append((kart.acceleration_c,kart.orientation))
step = 0
x = []
y = []
while (not(success)):
    # if not(step%10):
    #     print('position du kart',kart.position)
    print('Step taken : ', step)
    

    #Orientation control
    obj_pos = path[0]
    px = float(obj_pos[0])
    py = float(obj_pos[1])
   # next_vec = np.array([px,py]) - kart.position
    #next_theta = math.atan2(next_vec[0],next_vec[1])
    next_theta, norm = calculate_angle(kart.position,[px,py])
    delta = next_theta - kart.orientation
    if delta>np.pi:
        delta = delta - 2*np.pi

    elif delta < -1*np.pi:
        delta =  2*np.pi + delta 

    # if not(step%10):
    #     print('delta = ',delta)
    if delta >= 0:
        kart.turn_right()
        print('virage a gauche')
    elif delta < 0:
        kart.turn_left()
        print('virage a droite')

    braking = kart.check_radar_speed(delta)
    
    #Speed control
    if braking :
        kart.backward()
    else:
        kart.forward()
        
    print('pedale : ', kart.acceleration_c, 'delta = ', delta, ' position : ', kart.position, 'orientation du kart :', kart.orientation - angle_ini,  'next obj :', obj_pos, 'norm:', norm)
    command.append((kart.acceleration_c,kart.orientation))
    kart.update_pos()
    kart.radar_points()
    x_ = int(np.copy(kart.position[0]))
    y_ = int(np.copy(kart.position[1]))
    x.append(-1*kart.position[0])
    y.append(kart.position[1])

    if kart.map[x_][y_]==104:
        success = True
        print('Successfully finished the map')
        break
    step +=1
    #time.sleep(0.1)


#print(command)
ax.plot(y, x, color='red')
plt.show()

        

