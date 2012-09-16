def RGB_to_XYZ(r, g, b):
    """Get a tuple of the X, Y, Z component of the color."""

    #       [ 0.3935 0.3653 0.1916 ]
    # T =   [ 0.2124 0.7011 0.0866 ]
    #       [ 0.0187 0.1119 0.9582 ]
    # [X; Y; Z] = T * [R; G; B]

    x = 0.3935 * r + 0.3653 * g + 0.1916 * b
    y = 0.2124 * r + 0.7011 * g + 0.0866 * b
    z = 0.0187 * r + 0.1119 * g + 0.9582 * b
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