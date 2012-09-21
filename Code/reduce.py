'''
Created on Sep 20, 2012

@author: wes
'''

from operator import itemgetter, attrgetter
import os
import sys
from PIL import Image

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
    if len(boxes)<n:
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
        return median_cut(boxes,n) #define split
    else:
        #print "else"#
        #print boxes#
        return boxes
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def reduce_instances(img,n):
    '''
    take an image and a number, reduce the color
    '''
    im = img.copy()
    pixList = list(im.getdata())
    unique_list = list(set(pixList))
    #print "pixListLength:"#
    #print len(pixList)#
    #print "uniqueListLength:"#
    #print len(unique_list)#
    instance_box = []
    instance_box.append(unique_list)
    box_list = median_cut(instance_box,n)
    for p in pixList:
        for box in box_list:
            if p in box:
                pixList[pixList.index(p)] = box[0]
    #print "new pixListLength:"#
    #print len(pixList)#
    #print "new pixList vals:"#
    #print pixList#
    #print "box_list:"#
    #print len(box_list)#
    #Image.frombuffer('RGB', im.size, pixList)
    im.putdata(pixList)
    return im

## Testing:
#new_im = Image.open('blue_gradient.jpg')
#newer_im = reduce_instances (new_im,2)
#newer_im.save('testIm.jpg') 
#new_list = list(new_im.getdata())
#print "new_list:"
#print new_list
#new_im.save('testIm.jpg')