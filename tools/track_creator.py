from PIL import Image
import numpy as np 


### This very rudimentary tool transcribes an image into the corresponding string.
### Needs some love, is very very very basic.

track_image = Image.open('track_creator.png')

track_image_arr = np.array(track_image)
image64 = track_image_arr.astype(np.float64)

track_str = ""

for i in np.arange(np.shape(image64)[0]):   
    for j in np.arange(np.shape(image64)[1]):
        print(image64[i,j])
        if (np.array_equiv(image64[i,j], [255.,255.,0.,255.])):
            track_str += "B"
        elif (np.array_equiv(image64[i,j], [255.,0.,0.,255.])):
            track_str += "L"
        elif (np.array_equiv(image64[i,j], [50.,50.,0.,255.])):
            track_str += "C"
        elif (np.array_equiv(image64[i,j], [0.,255.,0.,255.])):
            track_str += "G"
        else:
            track_str += "R"
    
    track_str += "\n"

print(track_str)

