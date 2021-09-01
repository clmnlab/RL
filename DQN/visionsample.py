import torchvision
import numpy as np
from PIL import Image as pilimg
import matplotlib.pyplot as plt
import tensorflow as tf

image = pilimg.open('./a.bmp').convert('L')
plt.imshow(image, cmap= 'gray')
plt.show()