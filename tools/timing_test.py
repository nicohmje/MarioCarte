import time
import numpy as np

### THIS EXISTS TO TEST OUT THE EXECUTION TIME OF DIFFERENT FUNCTIONS 
### Example: using lists vs np.arrays() 



i=0
velocity = np.array([12.3,15.3])

iterations = 30000

g = 1

start_time = time.time_ns()

a = np.array([2,3])

track = np.array([[2,3,3],[4,5,6],[3,5,6]])
b = np.array([4,5])

def fenetre_func(position):
    # fenetre = np.zeros([3,3])    
    # for i in range(3):
    #     for j in range(3):
    #         fenetre[i][j]=int(track[x+i][y+j])
    # return fenetre
    return np.array([track[position[0]:position[0]+3,position[1]:position[1]+3]]) 

for _ in range(iterations):
    fenetre_func([0,0])    

    
print((time.time_ns() - start_time) * 1e-9)
print(((time.time_ns() - start_time) * 1e-9)/iterations)