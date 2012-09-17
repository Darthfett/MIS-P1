from __future__ import division
from __future__ import print_function

# 3rd party imports
from wand.image import Image

# built-in libraries
import os
import sys

# project libraries
pass

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
    if len(args) > 1:
        print('main.py takes exactly one argument as input: the path to an image file.')
        return
    elif not args:
        filepath = input('Enter the path to an image file: ')
    else:
        filepath = args.pop()

    # Open image and partition in 36 pieces, and put into a 'pieces' folder
    with Image(filename=filepath) as image:
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