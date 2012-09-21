"""
Will take in partitioned image,
convert image to HSL
set saturation
edit rest of image to maintain 'energy'
return the image
"""

# Note: this is just a code sketch, I'll fill in code as I go along.

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
    # edit the H and L values to keep energy the same
    # convert back to RGB
    # copy these values back to the pixel's rgb values.
    # end loop
    """
    for col in range(cols):
        pixels = sat_images[col]
        for pix in range(pix_size):
            pixel = pixels[pix]
            pix_hue, pix_sat, pix_lum = cm.RGB_to_HSL(pixel.red, pixel.green, pixel.blue)
            pix_sat = pix_sat * sat_amt
            #add in fix for energy here, once I figure that out
            pixel.red,pixel.green,pixel.blue = HSL_to_RGB(pix_hue, pix_sat, pix_lum)
            pixels[pix] = pixel     #update pixel in the list
        
        sat_images[col] = pixels;   #update block to altered pixels list

    return sat_images

def compare_energy(images, alter_images):

    # compare 'energy' of images
    # and change the bottom two rows of alter_images to match
    # prof says this is on MiNC, whatever the hell that is.
    return alter_images

def HSL_to_RGB(hue, sat, lum): #math found here is sourced from equations found on wikipedia
    chroma = (1 - abs(2 * lum - 1) ) * sat
    hue_prime = hue / 60

    x = chroma * (1 - abs( (hue_prime %2) - 1) ) #intermediate value.

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
    else    
        r1,g1,b1 = (0,0,0) #H was undefined.

    li = lum - (.5*chroma) #"lightness"

    return (r1 + li, g1 + li, b1 + li)