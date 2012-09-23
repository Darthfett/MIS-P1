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

def XYZ_to_RGB (X,Y,Z):
    '''
    given X,Y,Z values for a pixel, return corresponding R,G,B values
    Equations adapted from easyrgb.com
    '''
    var_X = X/100
    var_Y = Y/100
    var_Z = Z/100
    var_R = var_X*3.2406 + var_Y *-1.5372 + var_Z*-.4986
    var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
    var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570
    if var_R > 0.0031308: 
        var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_R = 12.92 * var_R
    if var_G > 0.0031308:
        var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_G = 12.92 * var_G
    if var_B > 0.0031308:
        var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_B = 12.92*var_B
    R = var_R *255
    G = var_G *255
    B = var_B *255
    return (R,G,B)

def LAB_to_XYZ(L,A,B):
    '''
    convert pixels from L*a*b to XYZ
    code adapted from easyrgb.com
    '''
    var_Y = ( L + 16 )/116
    var_X = A/500 + var_Y
    var_Z = var_Y - B/200
    
    if var_Y**3 > 0.008856:
        var_Y = var_Y**3
    else:
        var_Y = ( var_Y - 16 / 116 ) / 7.787
    if var_X**3 > 0.008856:
        var_X = var_X**3
    else:
        var_X = ( var_X - 16 / 116 ) / 7.787
    if var_Z**3 > 0.008856:
        var_Z = var_Z**3
    else:
        var_Z = ( var_Z - 16 / 116 ) / 7.787
    ref_X = 95.047
    ref_Y = 100.000
    ref_Z = 108.883
    X = ref_X * var_X
    Y = ref_Y * var_Y
    Z = ref_Z * var_Z
    return (X,Y,Z)

def LAB_to_RGB(L,A,B):
    X,Y,Z = LAB_to_XYZ(L,A,B)
    R,G,B = XYZ_to_RGB(X,Y,Z)
    return (R,G,B)

def YIQ_to_RGB(Y,I,Q):
    R = 1*Y + .9563*I + .6210*Q
    G = 1*Y + -.2721*I + -.6474*Q
    B = 1*Y + -1.1070*I + 1.7064*Q
    return (R,G,B)

def CMY_to_RGB(C,M,Y):
    R = 1-C
    G = 1-M
    B = 1-Y
    return (R,G,B)

def YUV_to_RGB(Y,U,V):
    R = 1*Y + 0*U + 1.14*V
    G = 1*Y + -.394*U + -.581*U
    B = 1*Y + 2.028*U + 0*V
    return (R,G,B)

def YCbCr_to_RGB(Y,Cb,Cr):
    R = Y + 1.402*(Cr-128)
    G = Y - .034414*(Cb-128) - .71414*(Cr-128)
    B = Y + 1.772*(Cb-128)
    return (R,G,B)

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

convert_back_for_colormodel = {
    'RGB': lambda r, g, b: (r, g, b),
    'XYZ': XYZ_to_RGB,
    'CMY': CMY_to_RGB,
    'YUV': YUV_to_RGB,
    'YIQ': YIQ_to_RGB,
    'YCbCr': YCbCr_to_RGB,
    'Lab': LAB_to_RGB,
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