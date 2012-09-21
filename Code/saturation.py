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
            pixel.red,pixel.green,pixel.blue = HSL_to_RGB(pix_hue, pix_sat_alt, pix_lum_alt)
            
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

def HSL_to_RGB(hue, sat, lum): #math found here is sourced from equations found on wikipedia
    #solve for chroma
    chroma = (1 - abs(2 * lum - 1) ) * sat
    
    #get hue degree ratio(?)
    hue_prime = hue / 60

    #intermediate value. Wasn't explained what this was, other than "it's needed"
    x = chroma * (1 - abs( (hue_prime %2) - 1) )

    #get intermediate R,G,B values. This block right here is why I had to look online for help. No clue why it's this way
    if hue_prime >= 0 and hue_prime < 1:
        r1,g1,b1 = (chroma, x, 0)
    elif hue_prime >= 1 and hue_prime < 2:
        r1,g1,b1 = (x, chroma, 0)
    elif hue_prime >= 2 and hue_prime < 3:
        r1,g1,b1 = (0, chroma, x)
    elif hue_prime >= 3 and hue_prime < 4:
        r1,g1,b1 = (0, x, chroma)
    elif hue_prime >= 4 and hue_prime < 5:
        r1,g1,b1 = (x, 0, chroma)
    elif hue_prime >= 5 and hue_prime < 6:
        r1,g1,b1 = (chroma, 0, x)
    else:
        r1,g1,b1 = (0,0,0) #H was undefined.

    #get the "lightness"
    li = lum - (.5*chroma)

    return (r1 + li, g1 + li, b1 + li)