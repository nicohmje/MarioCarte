import numpy as np
import matplotlib.pyplot as plt
from typing import NamedTuple
import random
import time
import math
from Mapping import mapping

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

track_string = """GGGGGG
GRRRRG
GRRRRG
GRRRRG
GRRRRG
GCCCCG
GRRRRG
GRRRRG
GRRRBG
GRRRRG
GDDDDG
GRRRRG
GEEEEG
GRRRRG
GRRRRG
GFFFFG
GGGGGG"""

track = mapping(track_string)
#plt.imshow(track)
#plt.show()
fig, ax = plt.subplots()




### Initializing qtable :
largeur = track.shape[1]
hauteur = track.shape[0]

ax.imshow(track, extent=[0, largeur, -1*hauteur, 0])

qtable = np.zeros([hauteur,largeur,9])

#Setting number of episodes
total_episodes=1000
# Set the seed
seed=14675
rng = np.random.default_rng(seed)

#Definition of kart's position and orientation
pos_ini = np.array([100.,100.])
angle_ini = 0.
f = 0.02
#Definition of accelerations
MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25
BOOST_SPEED = 25.


class Kart():
    
    f = 0.02
    
    def __init__(self):
        
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
        
    def create_map(self,useable_array):
        self.map = useable_array
        
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
    
    def read_map(self):
        boosting = False
        X = np.array(self.position, dtype='int')

        match self.map[X[0]][X[1]]:
            case 255:
                return 'R',boosting
            case 101:
                if (self.checkpoint<1):
                    self.checkpoint=1
                    return 'X', boosting
                else: 
                    return 'C',boosting
            case 102:
                if (self.checkpoint<2):
                    self.checkpoint=2
                    return 'Y', boosting
                else:
                    return 'D',boosting
            case 103:
                if (self.checkpoint<3):
                    self.checkpoint=3
                    return 'Z', boosting
                else:
                    return 'E', boosting
            case 104:
                self.success = True
                return 'F',boosting
            case 0:
                return 'G',boosting
            case 10:
                return 'A',boosting #stands for apex corner
            case 200:
                boosting = True
                return 'B',boosting
            case 5:
                return 'AS',boosting #stands for A star trajectory
            case 180:
                return 'ASP', boosting #stands for A star points
                
        

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



        
def rewarding(position,prec_pos,road_block): 
    if np.any(position!=prec_pos):
        match road_block:
            case 'R':
                return 10.
            case'X':
                return 500.
            case'Y':
                return 800.
            case'Z':
                return 1000.
            # case'D') and (checkpoint<2):
            #     return 90.
            # case'E') and (checkpoint<3):
            #     return 190.
            case 'F':
                return 4000.
            case 'G':
                return -10000.
            case 'L':
                return -10000.
            case'A':
                return 2000.
            case 'B':
                return 300.
            case 'AS':
                return 2000.
            case 'ASP':
                return 2000.
            case _:
                return 0.
            
    else:
        return -10.
        
        
    
    


commands = {
    0 : 'F + L',
    1 : 'F + S',
    2 : 'F + R',
    3 : 'B + L',
    4 : 'B + S',
    5 : 'B + R',
    6 : 'L + L',
    7 : 'L + S',
    8 : 'L + R'
}

class RollingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer = [0] * window_size
        self.index = 0
        self.sum = 0

    def update(self, new_value):
        old_value = self.buffer[self.index]
        self.buffer[self.index] = new_value

        self.sum = self.sum - old_value + new_value
        self.index = (self.index + 1) % self.window_size

    def get_average(self):
        return self.sum / min(self.window_size*1., (self.index + 1.)*1.)




#List of rewards : 
rewards=[]
nbr_episode=0

traj = np.array([])
gamma=0.95
epsilon=1.0
decay_rate=0.0001 
kart = Kart()
kart.create_map(track)

max_epsilon = 0.9
min_epsilon = 0.001
max_command = 1000

#command_nbr_avg = RollingAverage(30)
start = time.time()

action_map = {
    0: (MAX_ACCELERATION, - MAX_ANGLE_VELOCITY ),
    1: (MAX_ACCELERATION, 0),
    2: (MAX_ACCELERATION, + MAX_ANGLE_VELOCITY ),
    3: (-MAX_ACCELERATION, - MAX_ANGLE_VELOCITY ),
    4: (-MAX_ACCELERATION, 0 ),
    5: (-MAX_ACCELERATION, + MAX_ANGLE_VELOCITY ),
    6: (0, - MAX_ANGLE_VELOCITY ),
    7: (0, 0),
    8: (0, + MAX_ANGLE_VELOCITY )
}

#Defining the maximum coordinates used later to pursue training
# command_max = 0
# max_pos = np.array([0.,0.])
# max_orient = 0.

for episode in range(total_episodes):
    # print('New episode beginning : number',episode)
    
    pos_x = []
    pos_y = []
    
    #start_time_ns = time.time_ns()
    
    #Reseting the environnement
    
    command = 0
    total_rewards = 0
    kart.reset(pos_ini, angle_ini)
    
    #Definition of the parameters
    
    learning_rate=0.01+0.09*((total_episodes-episode)/total_episodes)
    #learning_rate = 0.05
    
    
    for command in range(max_command):
        #Generating a random number       
        exp_exp_tradeoff = random.random()
        #Saving the current position
        position = np.array([kart.position[0], kart.position[1]], dtype=int)
        # if command > command_max:
        #     max_pos = np.copy(position)
        #     max_orient = kart.orientation
        #     command_max = command


        
        
        #This value decides whether we prefer exploitation or exploration (<eps -> exploration)
        if (exp_exp_tradeoff>epsilon) or (episode == total_episodes-1):
            action = np.argmax(qtable[position[0]][position[1]])
            #action = np.argmax(qtable[position[1]][position[0]])
            
        else:#Otherwise we chose a random action from the nine possible
            if np.linalg.norm(kart.velocity)>15.:
                action = random.randrange(9)#All choices available
            else:
                action = random.randrange(3)#Consider only accelerating as the speed is too low

        #Take the action (a) and observe the outcome state(s') and reward (r)
        
        #Forwars [0:2]
        #0 : Forward + Left
        #1 : Forward + Straight
        #2 : Forward + Right
        
        #Backward [3:5]
        #3 : Backward + Left
        #4 : Backward + Straight
        #5 : Backward + Right
        
        #Lift off the throttle [6:8]
        #6 : Lift + Left
        #7 : Lift + Straight
        #8 : Lift + Right
        
        #To do maybe: if speed < speed_min -> no brakes
        action_accel, action_orient = action_map[action]
        kart.acceleration_c += action_accel
        kart.orientation += action_orient
    
        
        prec_pos = np.copy(kart.position)
        prec_road_block, pre_boosting = kart.read_map()
        kart.update_pos()
        #Rewarding : 
        road_block, boosting = kart.read_map()
        reward = rewarding(kart.position,prec_pos,road_block)
                
        

        if road_block == 'G' or road_block == 'L':
            break

        
        #Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        # qtable[new_state,:] : all the actions we can take from new state
        next_lig = int(np.copy(kart.position[0]))
        next_col = int(np.copy(kart.position[1]))
        next_position = np.array([next_lig,next_col])
        best_next_action = np.argmax(qtable[next_lig][next_col])
        qtable[position[0]][position[1]][action] += learning_rate*(reward + gamma*qtable[next_lig][next_col][best_next_action]-qtable[position[0]][position[1]][action])# update following Bellman's equation
        #qtable[position[1]][position[0]][action] += learning_rate*(reward + gamma*np.argmax(qtable[next_col][next_lig])-qtable[position[1]][position[0]][action])# update following Bellman's equation

        total_rewards += reward
        #if (not command%10):
            #print('block',road_block,'reward:',reward,'velocity:',np.linalg.norm(kart.velocity), 'action taken', commands[action],'number of steps in the current episode: ',command)
        
        
        if (episode> (total_episodes-10) or episode<(20)):
        #if True : 
            pos_x.append(-1*kart.position[0])
            pos_y.append(kart.position[1])

        
        if road_block == 'F':
            break

    # delta_s = (time.time_ns() - start_time_ns) * 1e-9
    if (not pos_y == []):
        if (300>=command>200):
            ax.plot(pos_y, pos_x, label=episode,color='green')
        elif(400>=command>300):
            ax.plot(pos_y, pos_x, label=episode,color='black')
        elif(500>=command>400):
            ax.plot(pos_y, pos_x,label=episode,color='yellow')
        elif (200>=command>100):
            ax.plot(pos_y, pos_x,color='magenta')
        else:
            ax.plot(pos_y, pos_x,color='blue')

    #Reduce epsilon as we progress       
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode) 

    rewards.append(total_rewards)
    if (not episode%(total_episodes/100.)):
        print("Progress :", (episode/total_episodes)*100., "%")
        end = time.time()
        delay = end-start
        ETA = 100.*(1.- episode/total_episodes)*delay
        print('ETA : ',ETA, 's')
        start = end

ax.plot(pos_y, pos_x, color='red') #Corresponds to the trajectory the AI would take while playing
#plt.plot(max_pos[1],-1*max_pos[0], label = 'ultimate pos', marker = '+')

#ax.xlabel('x')
#ax.ylabel('y')
#plt.legend()
#plt.axis('square')
#plt.ylim([-170,0])
#plt.xlim([0,60])
plt.show()
plt.figure()
plt.plot(np.arange(total_episodes),rewards)
plt.title('Rewards en fonction du nombre d épisodes')
plt.xlabel('episode')
plt.ylabel('rewards')
plt.show()
#print(command_max)

#idée : apprendre à partir du point le plus loin atteint (aka celui ayant le nombre de commande le plus élevé), comme ça on explore à partir de point différents, sinon on explore
#juste au début, mais une fois avancé dans la map on ne fait plus qu'exploiter dans une zone inexplorée.

#Memorizing best trajectory by adding distance between Xi and Xi+1 point

#Need to add smthg that finds the end point
   

