from __future__ import division
from __future__ import print_function

# 3rd party imports
import Image as PIL

# built-in libraries
import os
import sys

# project libraries
import highlight
import average
import nearest
import colormodel as cm
import saturate
import reduce

def partition_image(image, rows=6, cols=6):
    """
    Takes an image and partitions it into a 6x6 grid.

    Returns a list of 36 images, listed in row major order.
    """

    # Width and height of each individual image (as a float)
    width, height = image.size
    
    width //= cols
    height //= rows
    
    images = []
    
    
    
    for row in range(rows):
        for col in range(cols):
            left = int(round(width * col))
            top = int(round(height * row))
            if col == cols-1:
                right = image.size[0]
            else:
                right = int(round(width * (col + 1)))
            if row == rows-1:
                bot = image.size[1]
            else:
                bot = int(round(height * (row + 1)))
            img = image.crop((left, top, right, bot))
            img.load()
            images.append(img)

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
    img = highlight.splice_image(saturate.saturate_top(images, increase))
    
    img.save('../Outputs/saturate.png')

    pass

def delegator_nearest(images, cell, color_model):
    """Take a string cell and a string color model, and locate the cell in the grid with the most similar average color."""
    near_image = nearest.compare_average_color(images, int(cell), color_model)
    print(images.index(near_image))
    # display (near_Image)

def delegator_reduce(images, cell, n):
    img = images[int(cell)]
    reduced_list = reduce.reduce_instances(img,int(n))
    RGB_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[0]] + images[int(cell)+1:])
    RGB_reduced_spliced.save('../Outputs/reduce_RGB.png')


    XYZ_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[1]] + images[int(cell)+1:])
    XYZ_reduced_spliced.save('../Outputs/reduce_XYZ.png')

    CMY_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[2]] + images[int(cell)+1:])
    CMY_reduced_spliced.save('../Outputs/reduce_CMY.png')

    YUV_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[3]] + images[int(cell)+1:])
    YUV_reduced_spliced.save('../Outputs/reduce_YUV.png')

    YIQ_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[4]] + images[int(cell)+1:])
    YIQ_reduced_spliced.save('../Outputs/reduce_YIQ.png')

    YCbCr_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[5]] + images[int(cell)+1:])
    YCbCr_reduced_spliced.save('../Outputs/reduce_YCbCr.png')

    Lab_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[6]] + images[int(cell)+1:])
    Lab_reduced_spliced.save('../Outputs/reduce_Lab.png')

    HSL_reduced_spliced = highlight.splice_image(images[:int(cell)] + [reduced_list[7]] + images[int(cell)+1:])
    HSL_reduced_spliced.save('../Outputs/reduce_HSL.png')
    """Take a string cell and a string n, and create 7 versions of the image, where the number of colors has been reduced to n."""
    pass

def delegator_highlight(images, cell):
    """Take a string cell, and create 7 versions of the image, where pixels with the highest 80% of the third color component are highlighted."""
    highlight.highlight_cell(images, int(cell))
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
            image = PIL.open(filepath)
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
        #try:
        CMD_DICT[cmd](images, *args)
        #except TypeError:
            #print('Invalid number of arguments for command "{cmd}"'.format(cmd=cmd))
            #continue

if __name__ == '__main__':
    main(sys.argv[1:]) # skip first argument ("main.py")