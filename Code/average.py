from __future__ import division
from __future__ import print_function

import colormodel as cm

#########################################
#
# Temporarily Copied from nearest.py
#
def average_RGB(img):
    """
    Get the average RGB of the image, as a tuple.
    
    The value returned for each component is a fractional portion of the max red/green/blue.
    
    For example,
    (1, 1, 1) is white,
    (0, 0, 0) is black.
    """
    
    # Sum all the Reds, Greens, and Blues
    pixels = tuple(img.getdata())
    total = tuple(sum(colors) for colors in zip(*pixels))

    # Find average RGB
    width, height = img.size
    num_pixels = width * height
    avg = tuple((component / num_pixels) / (255) for component in total)

    return avg
#
#
#########################################

def print_average(images, color_model):
    if color_model not in cm.converter_for_colormodel:
        raise ValueError("print_average: Invalid color model {cm}".format(cm=color_model))
    average_RGBs = [average_RGB(image) for image in images]
    print("Average {cm} color:".format(cm=color_model))
    for cell, avg in enumerate(average_RGBs):
        print("\tCell {cell}: {color}".format(cell=cell+1, color=cm.converter_for_colormodel[color_model](*avg)))
            