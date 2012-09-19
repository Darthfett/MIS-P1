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


def compare_average_color(image_list, index, colorModel):
    """
    Takes a list of images, the index of one image
    in that list, and the color model being used.
    Returns the image with the closest average color
    to the image at the index given
    """

    target_image = image_list[index]
    target_red, target_green, target_blue = average_RGB(target_image)
    
    # Remove the target image from the list.
    image_list= image_list[:index]+image_list[index+1:]
    closest_d = 10000

    # Pick which color model desired
    # Get average colors for target image in that model
    # Get average colors for each image in list, return the one closest
    if colorModel == 'RGB':
        # Get average color in target image.
        for i in image_list:
            # Get RGB values for i
            red, green, blue = average_RGB(i)
            r_dif = red-target_red
            g_dif = green-target_green
            b_dif = blue-target_blue
            d=math.sqrt(math.pow(r_dif,2)+math.pow(g_dif,2)+math.pow(b_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i

        return closeImage

    elif colorModel == 'XYZ':
        target_x,target_y,target_z = cm.RGB_to_XYZ(target_red,target_green,target_blue)
        for i in image_list:
            #get XYZ values for i
            x,y,z = cm.RGB_to_XYZ(*average_RGB(i))

            x_dif = x-target_x
            y_dif = y-target_y
            z_dif = z-target_z
            d=math.sqrt(math.pow(x_dif,2)+math.pow(y_dif,2)+math.pow(z_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i

        #Compare averages for target images and return
        return closeImage
    elif colorModel == 'CMY':
        target_c,target_m,target_y = cm.RGB_to_CMY(target_red,target_green,target_blue)
        for i in image_list:
            #get XYZ values for i
            c,m,y = cm.RGB_to_CMY(*average_RGB(i))

            c_dif = c-target_c
            m_dif = m-target_m
            y_dif = y-target_y
            d=math.sqrt(math.pow(c_dif,2)+math.pow(m_dif,2)+math.pow(y_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i

            return closeImage
    elif colorModel ==  'Lab':
        target_L,target_a,target_b = cm.RGB_to_LAB(target_red,target_green,target_blue) # Use default white X, Y, Z.
        for i in image_list:

            L,a,b = cm.RGB_to_LAB(*average_RGB(i)) # Use default white X, Y, Z.

            L_dif = L-target_L
            a_dif = a-target_a
            b_dif = b-target_b
            d=math.sqrt(math.pow(L_dif,2)+math.pow(a_dif,2)+math.pow(b_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i

        return closeImage


    elif colorModel == 'YUV':
        target_y,target_u,target_v = cm.RGB_to_YUV(target_red,target_green,target_blue)
        for i in image_list:

            y,u,v = cm.RGB_to_YUV(*average_RGB(i))

            y_dif = y-target_y
            u_dif = u-target_u
            v_dif = v-target_v
            d=math.sqrt(math.pow(y_dif,2)+math.pow(u_dif,2)+math.pow(v_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
        #Compare averages for target images and return
        return closeImage

    elif colorModel == 'YCbCr':
        target_y,target_cb,target_cr = cm.RGB_to_YCbCr(target_red,target_green,target_blue)
        for i in image_list:
            #Get RGB values for i
            y,cb,cr = cm.RGB_to_YCbCr(*average_RGB(i))

            y_dif = y-target_y
            cb_dif = cb-target_cb
            cr_dif = cr-target_cr
            d=math.sqrt(math.pow(y_dif,2)+math.pow(cb_dif,2)+math.pow(cr_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
        #Compare averages for target images and return
        return closeImage

    elif colorModel == 'YIQ':
        target_y,target_i,target_q = cm.RGB_to_YIQ(target_red,target_green,target_blue)
        for j in image_list: #for this branch had to make j the iterating variable so doesn't interfere with i of YIQ below
            #Get RGB values for j
            y,i,q = cm.RGB_to_YIQ(*average_RGB(j))

            y_dif = y-target_y
            i_dif = i-target_i
            q_dif = q-target_q
            d=math.sqrt(math.pow(y_dif,2)+math.pow(i_dif,2)+math.pow(q_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = j
        #Compare averages for target images and return
        return closeImage

    elif colorModel == "HSL":
        target_h,target_s,target_l = cm.RGB_to_HSL(target_red,target_green,target_blue)
        for i in image_list:
            #Get RGB values for i
            h,s,l = cm.RGB_to_HSL(*average_RGB(i))
            if h == None:
                h = 0 #Because need to be able to subtract
            h_dif = h-target_h
            s_dif = s-target_s
            l_dif = l-target_l
            d=math.sqrt(math.pow(h_dif,2)+math.pow(s_dif,2)+math.pow(l_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
        #Compare averages for target images and return
        return closeImage
    else :
        print("ERROR: Invalid color model chosen. Choices are: 'RGB','XYZ','Lab','YUV','YCbCr','YIQ', and 'HSL'")


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

