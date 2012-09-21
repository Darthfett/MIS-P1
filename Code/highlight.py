from __future__ import division
from __future__ import print_function

import Image as PIL

import heapq
import itertools as it

import colormodel as cm

def splice_image(images):
    """Splice 36 images into a 6x6 grid in row-major order."""

    rows = 6
    cols = 6

    width = sum(width for width, _ in (image.size for image in images[:6]))
    height = sum(height for _, height in (image.size for image in images[::cols]))

    image = PIL.new('RGB', (width, height))

    top = 0
    left = 0
    for i, img in enumerate(images):
        w, h = img.size
        image.paste(img, (left, top))
        left += w
        
        if ((i+1) % rows) == 0:
            top += h
            left = 0
        

    return image

def highlight_cell(images, cell):
    image = images[cell]
    pixels = list(image.getdata())

    # For the given cell, map the color model to the list of pixels.
    cm_to_pixels = {}

    for model in cm.converter_for_colormodel:
        converted_pixels = list(it.starmap(cm.converter_for_colormodel[model], pixels))

        n = int(.2 * len(pixels))

        # Get indices for the pixels with the top 20% third color component
        largest_tuples = heapq.nlargest(n, enumerate(converted_pixels), key=lambda x: x[1][2])

        # Convert from enumerate tuples to just the indices
        largest_indices = [i for i, _ in largest_tuples]

        # Highlight pixel (turn to white)
        cm_to_pixels[model] = pixels[:]
        for i in largest_indices:
            cm_to_pixels[model][i] = (255, 255, 255)

    cm_to_image = {}

    for model in cm_to_pixels:
        new_cell_image = PIL.new('RGB',image.size)
        new_cell_image.putdata(cm_to_pixels[model])

        cell_images = images[:cell] + [new_cell_image] + images[cell + 1:]

        cm_to_image[model] = splice_image(cell_images)

    # PIL.Image.show(cm_to_image['RGB'])
    cm_to_image['YUV'].save('temp.png')
    
    for color_model, img in cm_to_image.items():
        img.save('../Outputs/highlight_{cm}.png'.format(cm=color_model))