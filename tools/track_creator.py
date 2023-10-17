from PIL import Image
import numpy as np 


track_image = Image.open('track.png')

track_image_arr = np.array(track_image)
image64 = track_image_arr.astype(np.float64)

track_str = ""

for i in np.arange(np.shape(image64)[0]):   
    for j in np.arange(np.shape(image64)[1]):
        if (np.array_equiv(image64[i,j], [255.,255.,0.,255.])):
            track_str += "B"
        elif (np.array_equiv(image64[i,j], [255.,0.,0.])):
            track_str += "L"
        elif (np.array_equiv(image64[i,j], [50.,50.,0.,255.])):
            track_str += "C"
        elif (np.array_equiv(image64[i,j], [0.,255.,0.,255.])):
            track_str += "G"
        else:
            track_str += "R"
    track_str += "\n"

print(track_str)

