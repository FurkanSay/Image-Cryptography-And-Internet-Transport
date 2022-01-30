import cv2
import numpy as np

image_name = "encrypted_images/pic1.png" # image name
image_name1 =  "input/pic1.png"
img = cv2.imread(image_name1) # read image

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# flatten channels
# use hist function to acquire histograms and normalized histograms of channels
size_y = img.shape[0] # get shape
size_x = img.shape[1]

flattened = img.reshape([size_x*size_y])  # Flatten matrices

from matplotlib import pyplot as plt # import pylot
rhist,_ ,_ = plt.hist(flattened, bins=256)# ,log=True)
plt.show() # hist functions returns number values for each bin

rhist,_ ,_ = plt.hist(flattened, bins=32)# ,log=True)
plt.show() # hist functions returns number values for each bin

rhist,_ ,_ = plt.hist(flattened, bins=8)# ,log=True)
plt.show() # hist functions returns number values for each bin
