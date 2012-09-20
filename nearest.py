'''
Created on Sep 17, 2012

@author: wes
'''

from __future__ import division
from __future__ import print_function

from wand.image import Image
from wand.image import Iterator
from wand.color import Color

import os
import sys
import math

import colormodel as cm


def compare_average_color(image_list, index, color_model):
    """
    Takes a list of images, the index of one image
    in that list, and the color model being used.
    Returns the image with the closest average color
    to the image at the index given
    """

    assert color_model in cm.converter_for_colormodel
    
    target_image = image_list[index]
    tar_red, tar_green, tar_blue = average_RGB(target_image)
    
    # Remove the target image from the list.
    image_list= image_list[:index]+image_list[index+1:]
    closest_d = 10000
    
    # Find euclidean distance for specified color model
    t1, t2, t3 = cm.converter_for_colormodel[color_model](tar_red, tar_green, tar_blue)
    for i in image_list:
        c1, c2, c3 = cm.converter_for_colormodel[color_model](*average_RGB(i))
        
        d1 = c1 - t1
        d2 = c2 - t2
        d3 = c3 - t3
        d = (d1 ** 2 + d2 ** 2 + d3 ** 2) ** .5
        if d < closest_d:
            closest_d = d
            closest_image = i

    return closest_image

def average_RGB(img):
    """
    Get the average RGB of the image, as a tuple.
    
    The value returned for each component is a fractional portion of the max red/green/blue.
    
    For example,
    (1, 1, 1) is white,
    (0, 0, 0) is black.
    """
    
    # Sum all the Reds, Greens, and Blues
    pixels = ((px.red, px.green, px.blue) for row in img for px in row)
    total = tuple(sum(colors) for colors in zip(*pixels))

    # Find average RGB
    num_pixels = img.width * img.height
    avg = tuple((component / num_pixels) / (2**16 - 1) for component in total)

    return avg


#Test code: input imgList (2 images), index of 1, and rgb as color model.
#It should see which of red.jpg and blue_gradient.jpg are closest to
#white.jpg given RGB color scheme (it took about 10-15 sec to
#run on my pc, so don't give up if it seems like it's stuck):
imgList = [Image(filename=fn) for fn in {'white.jpg', 'blue_gradient.jpg'}]
print(compare_average_color(imgList,1,'YIQ'))

