import time
import numpy as np

### THIS EXISTS TO TEST OUT THE EXECUTION TIME OF DIFFERENT FUNCTIONS 
### Example: using lists vs np.arrays() 


start_time = time.time_ns()

i=0
velocity = np.array([0.,0.])

while i<3000:
    if(not velocity.dtype == "float64"):
        velocity = velocity.astype(float)
        print("shfbed")
    velocity[0] = 3.
    velocity[0] = 2.
    i+=1

print((time.time_ns() - start_time) *1e-9)