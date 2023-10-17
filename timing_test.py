import time
import numpy as np

start_time = time.time_ns()

i=0
velocity = np.array([0,0])

while i<3000:

    boosting = False
    vel = 0.2
    orientation = 0.4
    if boosting:
        velocity = (vel * np.cos(orientation), vel*np.sin(orientation))
    else:
        velocity = (25 * np.cos(orientation), 25*np.sin(orientation))
    i+=1

print((time.time_ns() - start_time) *1e-9)