'''
Created on Sep 17, 2012

@author: wes
'''
import math


def CompareAverageColor (image_list, index, colorModel):
    """
    Takes a list of images, the index of one image
    in that list, and the color model being used. 
    Outputs the image with the closest average color
    to the image at the index given
    """
    
    # Needs to implement functions for getting average r,g, and b 
    target_image = image_list[index]
    target_red = getAvgRed(target_image)
    target_green = getAvgGreen(target_image)
    target_blue = getAvgBlue(target_image)
    image_list= image_list[:index]+image_list[index+1:] #remove the target image from the list
    closest_d = 10000
    
    #pick which color model desired
    #get average colors for target image in that model
    #get average colors for each image in list, return the one closest
    if colorModel == 'RGB':
        #Get average color in target image
        for i in image_list:
            #Get RGB values for i
            red = getAvgRed(i)
            green = getAvgGreen(i)
            blue = getAvgBlue(i) #these functions need to be implemented
            r_dif = red-target_red
            g_dif = green-target_green
            b_dif = blue-target_blue
            d=math.sqrt(math.pow(r_dif,2)+math.pow(g_dif,2)+math.pow(b_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i       

        return closeImage
        
    elif colorModel == 'XYZ':
        target_x,target_y,target_z = RGB_to_XYZ(target_red,target_green,target_blue)
        for i in image_list:
            #get XYZ values for i
            x,y,z = RGB_to_XYZ(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
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
        target_c,target_m,target_y = RGB_to_CMY(target_red,target_green,target_blue)
        for i in image_list:
            #get XYZ values for i
            c,m,y = RGB_to_CMY(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
            c_dif = c-target_c
            m_dif = m-target_m
            y_dif = y-target_y
            d=math.sqrt(math.pow(c_dif,2)+math.pow(m_dif,2)+math.pow(y_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
                
            return closeImage
    elif colorModel ==  'Lab':
        xn=50 #put in values for white
        yn=50
        zn=50
        target_L,target_a,target_b = RGB_to_LAB(target_red,target_green,target_blue,xn,yn,zn)
        for i in image_list:
            
            L,a,b = RGB_to_LAB(getAvgRed(i),getAvgGreen(i),getAvgBlue(i),xn,yn,zn)
            
            L_dif = L-target_L
            a_dif = a-target_a
            b_dif = b-target_b
            d=math.sqrt(math.pow(L_dif,2)+math.pow(a_dif,2)+math.pow(b_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
        
        return closeImage
        
        
    elif colorModel == 'YUV':
        target_y,target_u,target_v = RGB_to_YUV(target_red,target_green,target_blue)
        for i in image_list:
            
            y,u,v = RGB_to_YUV(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
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
        target_y,target_cb,target_cr = RGB_to_YCbCr(target_red,target_green,target_blue)
        for i in image_list:
            #Get RGB values for i
            y,cb,cr = RGB_to_YCbCr(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
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
        target_y,target_i,target_q = RGB_to_YIQ(target_red,target_green,target_blue)
        for i in image_list:
            #Get RGB values for i
            y,i,q = RGB_to_YIQ(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
            y_dif = y-target_y
            i_dif = i-target_i
            q_dif = q-target_q
            d=math.sqrt(math.pow(y_dif,2)+math.pow(i_dif,2)+math.pow(q_dif,2))
            if d<closest_d:
                closest_d=d
                closeImage = i
        #Compare averages for target images and return
        return closeImage
    
    elif colorModel == "HSL":
        target_h,target_s,target_l = RGB_to_HSL(target_red,target_green,target_blue)
        for i in image_list:
            #Get RGB values for i
            h,s,l = RGB_to_HSL(getAvgRed(i),getAvgGreen(i),getAvgBlue(i))
            
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
        pass #add error catching
    

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
    return (y, cb, cr)

def RGB_to_LAB(r, g, b, xn, yn, zn):
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
    c = chroma
    
    if chroma == 0:
        H = None
    else:
        if max_ == r:
            H = ((g - b) / c) % 6
        elif max_ == g:
            H = ((b - r) / c) + 2
        else:
            H = ((r - g) / c) + 4
        H *= 60
        
    L = (.5) * (max_ + min_)
    if chroma == 0:
        S = 0
    else:
        S = chroma / (1 - abs(2 * L - 1))
    
    return (H, S, L)
    
def getAvgRed(img):
    return 7 #implement this

def getAvgGreen(img):
    return 5 #implement this
def getAvgBlue(img):
    return 5 #implement this
print RGB_to_HSL(5,5,5)
print CompareAverageColor ([1,2,3], 1, 'HSL') #test
        