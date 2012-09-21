from __future__ import print_function
from __future__ import division

import colormodel as cm

"""
Will take in partitioned image,
convert image to HSL
set saturation
edit rest of image to maintain 'energy'
return the image
"""

def sat_top(images, command):
    cols = 6;
    pix_size = len(images[1])

    sat_images = images
    sat_amt = 1.10

    if command == 'decrease':
        sat_amt = .90

    """
    # access first 6 elements in Images, this is the top row of the 6x6 grid in images
    # in each item, access every sub element (assuming they are pixels here)
    # convert each pixel's rgb values to HSL. Alter the saturation
    # edit the L values to keep energy the same
    # convert back to RGB
    # copy these changes back.
    # end loop
    """
    for col in range(cols):
        pixels = sat_images[col]
        for pix in range(pix_size):
            pixel = pixels[pix]
            #convert RGB -> HSL
            pix_hue, pix_sat, pix_lum = cm.RGB_to_HSL(pixel.red, pixel.green, pixel.blue)
            
            #alter saturation
            pix_sat_alt = pix_sat * sat_amt

            #to compensate for altered saturation, change luminance
            pix_lum_alt = alter_luminance(pix_hue, pix_sat, pix_lum, pix_sat_alt)

            #convert (now altered) HSL -> RGB
            pixel.red,pixel.green,pixel.blue = cm.HSL_to_RGB(pix_hue, pix_sat_alt, pix_lum_alt)
            
            #update pixel in list of pixels
            pixels[pix] = pixel

        #update pixel list to altered pixels list
        sat_images[col] = pixels;   

    return sat_images

#returns a new luminance value that will keep energy value of a pixel with altered saturation
def alter_luminance(h,s,l, s_new):
    #solve for energy of original HSL values (euclidean distance)
    e = sqrt(h*h + s*s + l*l)

    #solve for new luminance value, using the new saturation (solving for Y, basically)
    l_new = sqrt(e*e - h*h - s_new*s_new)   

    return (l_new)