from __future__ import division
from __future__ import print_function

# 3rd party imports
from wand.image import Image
from wand.display import display

# built-in libraries
import os
import sys

# project libraries
import average
import colormodel as cm
import saturation as satmod

def partition_image(image, rows=6, cols=6):
    """
    Takes an image and partitions it into a 6x6 grid.

    Returns a list of 36 images, listed in row major order.
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

# Command delegator functions

def help(_):
    print(CMD_HELP)

def delegator_average(images, color_model):
    """Take a string color model, and print out the average color for each cell in the 6x6 grid."""
    # Validate color_model
    color_model = cm.str_to_model.get(color_model.lower(), None)
    if color_model is None:
        raise ValueError('color_model', color_model, "Invalid color model {model}".format(model=color_model))

    # delegate work to compute and print average color
    average.print_average(images, color_model)

def delegator_saturate(images, increase):
    """Take a string "increase" or "decrease", and increase/decrease the saturation of the first row of the image by 10%, while preserving the energy."""
        satmod.sat_top(images, increase)

    pass

def delegator_nearest(images, cell, color_model):
    """Take a string cell and a string color model, and locate the cell in the grid with the most similar average color."""
    near_Image = nearest.compare_average_color(images, cell, colorModel)
    display (near_Image)

def delegator_reduce(images, cell, n):
    """Take a string cell and a string n, and create 7 versions of the image, where the number of colors has been reduced to n."""
    pass

def delegator_highlight(images, cell):
    """Take a string cell, and create 7 versions of the image, where pixels with the highest 80% of the third color component are highlighted."""
    pass

CMD_HELP = """
Available commands:
    help : Show this help message.
    average <color_model> : Print out the average color for each cell in the 6x6 grid of the image in the specified color model.  Possible color models are:
        - RGB
        - XYZ
        - Lab
        - YUV
        - YCbCr
        - YIQ
        - HSL
    saturate <increase/decrease> : Increase or decrease the saturation of the first row of the image by 10% (while preserving the overall 'energy').
    nearest <cell> <color_model> : Given a cell in the grid and a color model, locate the cell in the grid with the most similar average color.  cell is an integer in the range [0, 35].
    reduce <cell> <N> : Given a cell in the grid and a number N, create 7 different versions of the image, where the number of colors has been reduced to N.
    highlight <cell> : Given a cell in the grid, create 7 different versions of the image, where pixels with the highest 80% of the third color component are highlighted.
"""

CMD_DICT = {
    'help': help,
    'average': delegator_average,
    'saturate': delegator_saturate,
    'nearest': delegator_nearest,
    'reduce': delegator_reduce,
    'highlight': delegator_highlight,
}

def main(args):
    """
    Enter the main event loop, and begin prompting for user commands.

    args is a list of arguments, and main will only accept up to a single argument: the path to an image file.
    """
    if len(args) > 1:
        print('main.py takes exactly one argument as input: the path to an image file.')
        return
    elif not args:
        filepath = raw_input('Enter the path to an image file: ')
    else:
        filepath = args.pop()
        
    # Verify that the image is good
    while True:
        try:
            image = Image(filename=filepath)
        except Exception:
            print('Invalid image or path "{filepath}"'.format(filepath=filepath))
            filepath = raw_input('Enter the path to an image file: ')
        else:
            # Image is good.
            break

    # splice image into a 6x6 grid of images (row-major order).
    images = partition_image(image)

    # Main command loop interface
    while True:
        # Accept a command with args from the user (and split into a list)
        command = raw_input('Enter a command (or "help"): ').strip().split(' ')

        cmd = command[0].lower() # command is case-insensitive
        args = command[1:]

        # validate cmd to be a valid command
        if cmd not in CMD_DICT:
            # command is not an exact match, try a partial match
            if any(command.startswith(cmd) for command in CMD_DICT):
                cmd = next(command for command in CMD_DICT if command.startswith(cmd))

        if cmd not in CMD_DICT:
            # command is a quit, exit, or invalid command.
            if cmd.startswith(('q', 'e')):
                break
            print('Invalid command "{cmd}".  Valid commands: {cmds}'.format(cmd=cmd, cmds=', '.join(sorted(CMD_DICT.keys()))))
            continue
        # At this point, cmd is a valid command.

        # Execute one of the delegator functions with the given arguments.
        CMD_DICT[cmd](images, *args)

if __name__ == '__main__':
    main(sys.argv[1:]) # skip first argument ("main.py")