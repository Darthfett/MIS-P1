from __future__ import division
from __future__ import print_function

# 3rd party imports
from wand.image import Image

# built-in libraries
import os
import sys

# project libraries
pass

def RGB_to_XYZ(rgb):
    """Get a tuple of the X, Y, Z component of the color."""
    r, g, b = rgb.red, rgb.green, rgb.blue
    
    #       [ 0.3935 0.3653 0.1916 ]
    # T =   [ 0.2124 0.7011 0.0866 ]
    #       [ 0.0187 0.1119 0.9582 ]
    # [X; Y; Z] = T * [R; G; B]
    
    x = 0.3935 * r + 0.3653 * g + 0.1916 * b
    y = 0.2124 * r + 0.7011 * g + 0.0866 * b
    z = 0.0187 * r + 0.1119 * g + 0.9582 * b
    return (x, y, z)

def partition_image(image, rows=6, cols=6):
    """
    Takes an image and partitions it into a 6x6 grid.
    
    Returns an array of 36 images, listed in row major order.
    """
    
    # Width and height of each individual image (as a float)
    width = image.width / cols
    height = image.height / rows
    images = []    
    
    # Partition image into 36 equal images
    for row in range(rows):
        for col in range(cols):
            left = int(round(width * col))
            right = int(round(width * (col + 1)))
            top = int(round(height * row))
            bot = int(round(height * (row + 1)))
            images.append(image[left:right, top:bot])
            
    return images
    
def main(args):
    if not args:
        print('main.py takes an argument as input: the path to an image file.')
        return
    
    if len(args) != 1:
        print('main.py takes exactly one argument as input: the path to an image file.')
    
    # Open image and partition in 36 pieces, and put into a 'pieces' folder
    with Image(filename=args[0]) as image:
        images = partition_image(image)
        try:
            os.mkdir('pieces')
        except WindowsError:
            pass
        for i, img in enumerate(images):
            img.format = 'png'
            img.save(filename='pieces/' + str(i) + '.png')
        print(get_average_color(image))

if __name__ == '__main__':
    main(sys.argv[1:]) # skip first argument ("main.py")