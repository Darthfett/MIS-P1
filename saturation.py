"""
Will take in partitioned image,
convert image to HSL
set saturation
edit rest of image to maintain 'energy'
return the image
"""

# Note: this is just a code sketch, I'll fill in code as I go along.

def desat_top(images):

    desat_images = images

    # convert copy of images to HSL

    # set top row of desat_images to 10 less saturation

    # convert back to RGB

    # use images to compare overall change in color balance
    # or whatever makes sense for 'energy'
    # and change bottom two rows of desat_images to meet that requirement

def sat_top(images):

    sat_images = images

    # convert copy of images to HSL

    # set top row of desat_images to 10+ saturation

    # convert back to RGB

    # use images to compare overall change in color balance
    # or whatever makes sense for 'energy'
    # and change bottom two rows of desat_images to meet that requirement

    return sat_images

def compare_energy(images, alter_images):

    # compare 'energy' of images
    # and change the bottom two rows of alter_images to match

    return alter_images