import time
import numpy as np

### THIS EXISTS TO TEST OUT THE EXECUTION TIME OF DIFFERENT FUNCTIONS 
### Example: using lists vs np.arrays() 



i=0
velocity = np.array([12.3,15.3])

iterations = 30000

g = 1

start_time = time.time_ns()

for _ in range(iterations):
    # match g:
    #     case 1:
    #         y = 2
    #     case 2: 
    #         y = 3
    #     case 3: 
    #         y = 5
    #     case 4: 
    #         y = 2

    if g == 1:
        y = 2
    if g ==2:
        y = 3
    if g == 3:
        y = 5
    if g == 4:
        y =2

    
print((time.time_ns() - start_time) * 1e-9)
print(((time.time_ns() - start_time) * 1e-9)/iterations)