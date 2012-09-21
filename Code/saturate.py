from __future__ import division

import Image as PIL

import copy

import colormodel as cm

"""
Will take in partitioned image,
convert image to HSL
set saturation
edit rest of image to maintain 'energy'
return the image
"""

def saturate_top(images, inc_or_dec):
    if inc_or_dec == 'decrease':
        saturation_pct = 0.9
    else:
        saturation_pct = 1.1
        
    first_row = []
        
    for i, cell_image in enumerate(images[:6]):
        first_row.append(PIL.new('RGB', cell_image.size))
        pixels = list(cell_image.getdata())
        
        # Convert to HSL
        unmod_HSL = [cm.RGB_to_HSL(*px) for px in pixels]
        
        # Increase luminance without losing energy
        mod_HSL = [luminance_alterer(saturation_pct)(*px) for px in unmod_HSL]
        
        # Convert back to RGB
        mod_RGB = [tuple(map(int, cm.HSL_to_RGB(*px))) for px in mod_HSL]
        
        # Put to image
        first_row[i].putdata(mod_RGB)
    
    return first_row + images[6:]
    
def luminance_alterer(s_mod):    
    def alter_luminance(h, s, l):
        # overall energy
        energy = (h*h + s*s + l*l) ** .5
        
        # modify saturation
        new_s = s * s_mod
    
        # alter luminance to keep energy consistent
        new_l = (energy * energy - h * h - new_s * new_s) ** .5
        
        return h, new_s, new_l
    return alter_luminance