'''
Created on Sep 20, 2012

@author: wes
'''

from operator import itemgetter, attrgetter
import os
import sys
from PIL import Image
import colormodel as cm
import itertools as it

def largest_box (boxes):
    big_b=boxes[0]
    for b in boxes:
        if len(b)>len(big_b):
            big_b=b
    return big_b
    
def biggest_range(box):
    '''
    given a list of pixel values, figures out if the range of r,g, or b is biggest
    '''

def split_r(box):
    '''
    given a list of pixel 3-tuples, median-split based on red and return 2 lists
    '''
    sorted_box = sorted(box,key=itemgetter(0))
    box1 = sorted_box[:(len(sorted_box)/2)]
    box2 = sorted_box[(len(sorted_box)/2):]
    return box1, box2

def split_g(box):
    sorted_box = sorted(box,key=itemgetter(1))
    box1 = sorted_box[:(len(sorted_box)/2)]
    box2 = sorted_box[(len(sorted_box)/2):]
    return box1, box2

def split_b(box):
    sorted_box = sorted(box,key=itemgetter(2))
    box1 = sorted_box[:(len(sorted_box)/2)]
    box2 = sorted_box[(len(sorted_box)/2):]
    return box1, box2

def range_r(box):
    '''
    given a box (list of pixel 3-tuples) find the range of the red values of the pixels
    '''
    r,g,b = zip(*box)
    return max(r)-min(r)

def range_g(box):
    r,g,b = zip(*box)
    return max(g)-min(g)

def range_b(box):
    r,g,b = zip(*box)
    return max(b)-min(b)


def median_cut(boxes,n):
    '''
    given a list of lists of unique color instances, cut the number of instances to n
    '''
    while len(boxes)<n:
        big_box = largest_box(boxes)
        range_list = [range_r(big_box),range_g(big_box),range_b(big_box)]
        max_range = max(range_list)
        if max_range == range_list[0]: # red has biggest range
            box1,box2 = split_r(big_box)
        elif max_range == range_list[1]:
            box1,box2 = split_g(big_box)
        elif max_range == range_list[2]:
            box1,box2 = split_b(big_box)
        i = boxes.index(big_box)
        del boxes[i]
        boxes.insert(i,box2)
        boxes.insert(i,box1)
        #print boxes#
        #define split
        #print "else"#
        #print boxes#
    return boxes
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def pixel_info_to_int(p_list):
    '''
    given a pixel list, return the list with all values converted to int
    '''
    
    for pixel in p_list:
        i = p_list.index(pixel)
        l_pixel = list(pixel)
        for val in l_pixel:
            int_val = int(val)
            l_pixel[l_pixel.index(val)]=int_val
        p_list[i]=tuple(l_pixel)
    return p_list
    

def reduce_instances(img,n,):
    '''
    take an image and a number, reduce the color. Return a 7-list of image objects, one for each color space
    '''
    im = img.copy()
    pixList = list(im.getdata())
    unique_list = list(set(pixList))
    reduced_list = [] # A list of 3-tuple pixel lists in RGB that have been reduced.# Actually, a list of Image objects?
    converted_pixList = list(it.starmap(cm.converter_for_colormodel['XYZ'],pixList))
    #converted_pixList = pixel_info_to_int(converted_pixList)
   # print converted_pixList#
    #pix1 = converted_pixList[1]#
    #val1 = pix1[1]#
    #print val1#
    #val1 = int(val1)#
    #print val1#
    '''
    for pixel in converted_pixList:
        i = converted_pixList.index(pixel)
        l_pixel = list(pixel)
        for val in l_pixel:
            int_val = int(val)
            l_pixel[l_pixel.index(val)]=int_val
        converted_pixList[i]=l_pixel
    print converted_pixList
    '''
        
    #converted_pixList = pixel_info_to_int(converted_pixList)#
    #print pixel_info_to_int(converted_pixList)#
    #print "pixList:"#
    #print pixList#
    #print "pixListLength:"#
    #print len(pixList)#
    #print "uniqueListLength:"#
    #print len(unique_list)#
    
    for model in cm.converter_for_colormodel:
        converted_pixList = list(it.starmap(cm.converter_for_colormodel[model],pixList))
        #converted_pixList = pixel_info_to_int(converted_pixList)
        converted_unique = list(it.starmap(cm.converter_for_colormodel[model], unique_list))
        #converted_unique = pixel_info_to_int(converted_unique)
        instance_box = []
        instance_box.append(converted_unique)
        box_list = median_cut(instance_box,n)
        for p in converted_pixList:
            for box in box_list:
                if p in box:
                    converted_pixList[converted_pixList.index(p)] = box[0]
        converted_pixList = list(it.starmap(cm.convert_back_for_colormodel[model],converted_pixList))
        converted_pixList = pixel_info_to_int(converted_pixList)
        #print converted_pixList#
        im.putdata(converted_pixList)# want to put converted_pixList I think
        #print im.getdata()#
        reduced_list.append(im)
    #print "new pixListLength:"#
    #print len(pixList)#
    #print "new pixList vals:"#
    #print pixList#
    #print "box_list:"#
    #print len(box_list)#
    #Image.frombuffer('RGB', im.size, pixList)
    #im.putdata(pixList)
    #return im
    return reduced_list
    

## Testing:
#start_im = Image.open('blue_gradient.jpg')#
#new_list = reduce_instances(start_im,2)
#new_im_RGB = new_list[0]
#new_im_RGB.save('testRGBreduced.jpg')
#newer_im.save('testIm.jpg') 
#new_list = list(new_im.getdata())
#print "new_list:"
#print new_list
#new_im.save('testIm.jpg')