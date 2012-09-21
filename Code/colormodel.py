from __future__ import division

def RGB_to_XYZ(r, g, b):
    """Get a tuple of the X, Y, Z component of the color."""

    # Copied from book/notes:
    # X = 0.607 * R + 0.174 * G + 0.200 * B
    # Y = 0.299 * R + 0.587 * G + 0.114 * B
    # Z = 0.000 * R + 0.066 * G + 1.116 * B

    x = 0.607 * r + 0.174 * g + 0.200 * b
    y = 0.299 * r + 0.587 * g + 0.114 * b
    z =             0.066 * g + 1.116 * b
    return (x, y, z)

def RGB_to_CMY(r, g, b):
    return (1 - r, 1 - g, 1 - b)

def RGB_to_YUV(r, g, b):
    y =  0.299 * r +  0.587 * g +  0.144 * b
    u = -0.299 * r + -0.587 * g +  0.886 * b
    v =  0.701 * r + -0.587 * g + -0.114 * b
    return (y, u, v)

def RGB_to_YIQ(r, g, b):
    y =  0.299 * r +  0.587 * g +  0.144 * b
    i = 0.595879 * r + -0.274133 * g + -0.321746 * b
    q = 0.211205 * r + -0.523083 * g + 0.311878 * b
    return (y, i, q)

def RGB_to_YCbCr(r, g, b):
    y =  0.299 * r +  0.587 * g +  0.144 * b
    cb = -0.168736 * r + -0.331264 * g + 0.5 * b + 0.5
    cr = 0.5 * r + -0.418688 * g + -0.081312 * b + 0.5
    return (y, cb, cr)

DEFAULT_XYZ = 50
def RGB_to_LAB(r, g, b, xn=DEFAULT_XYZ, yn=DEFAULT_XYZ, zn=DEFAULT_XYZ):
    """Get a tuple of the L, a, b components of the color (relative to the white point xn, yn, zn)."""
    x = 0.3935 * r + 0.3653 * g + 0.1916 * b
    y = 0.2124 * r + 0.7011 * g + 0.0866 * b
    z = 0.0187 * r + 0.1119 * g + 0.9582 * b

    rel_x = (x / xn) ** (1 / 3)
    rel_y = (y / yn) ** (1 / 3)
    rel_z = (z / zn) ** (1 / 3)

    L = 116 * (rel_y) - 16
    a = 500 * (rel_x - rel_y)
    b = 500 * (rel_y - rel_z)

    return (L, a, b)

def RGB_to_HSL(r, g, b):
    max_ = max(r, g, b)
    min_ = min(r, g, b)
    chroma = max_ - min_

    if chroma == 0:
        H = 0 # Hue is undefined
    else: 
        if max_ == r:
            H = ((g - b) / chroma) % 6
        elif max_ == g:
            H = ((b - r) / chroma) + 2
        else:
            H = ((r - g) / chroma) + 4
        H *= 60

    L = (.5) * (max_ + min_)
    if chroma == 0:
        S = 0
    else:
        S = chroma / (1 - abs(2 * L - 1))

    return (H, S, L)

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

converter_for_colormodel = {
    'RGB': lambda r, g, b: (r, g, b),
    'XYZ': RGB_to_XYZ,
    'CMY': RGB_to_CMY,
    'YUV': RGB_to_YUV,
    'YIQ': RGB_to_YIQ,
    'YCbCr': RGB_to_YCbCr,
    'Lab': RGB_to_LAB,
    'HSL': RGB_to_HSL,
}

str_to_model = {
    'rgb': 'RGB',
    'xyz': 'XYZ',
    'cmy': 'CMY',
    'yuv': 'YUV',
    'yiq': 'YIQ',
    'ycbcr': 'YCbCr',
    'lab': 'Lab',
    'hsl': 'HSL',
}