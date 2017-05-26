#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt


def compute_upper_level_set(img,gray_level):
    return img >= gray_level

def compute_level_line(img,gray_level):
    uls = np.array( compute_upper_level_set(img,gray_level), dtype='int8' )

    w = np.array( [ [0,1,0],[1,1,1],[0,1,0] ] )
    uls_temp = ndimage.convolve(uls,w,origin=np.array( (1,1) ))

    uls_boundary = np.logical_and( uls_temp >=1, uls_temp<=4)

    return uls_boundary

def test_draw_level_set():
    img_file = "img/gradient.png"
    img = misc.imread(img_file)

    uls = compute_upper_level_set(img,115)	
    img[uls] = 0
    img[np.invert(uls)] = 255

    plt.imshow(img,cmap="gray")
    plt.show()

def test_draw_level_line():
    img_file = "img/lena_256.png"
    img = misc.imread(img_file)	

    level_line = compute_level_line(img,150)
    img[level_line] = 0
    img[np.invert(level_line)] = 255

    plt.imshow(img,cmap="gray")
    plt.show()	

def test_draw_five_level_lines():
    img_file = "img/gradient.png"
    img = misc.imread(img_file)

    l1=compute_level_line(img,130)
    l2=compute_level_line(img,145)
    l3=compute_level_line(img,160)
    l4=compute_level_line(img,175)
    l5=compute_level_line(img,190)

    img[l1] = 0; img[np.invert(l1)] = 255
    img[l2] = 0
    img[l3] = 0
    img[l4] = 0
    img[l5] = 0

    plt.imshow(img,cmap="gray")
    plt.show()

def test_intersection_level_lines():
    img_file = "img/gradient.png"
    # img_file = "img/lena_256.png"
    img = misc.imread(img_file)

    gl1,gl2 = random.sample( range(256),2 )

    ll1=compute_level_line(img,130)
    ll2=compute_level_line(img,131)

    print( gl1,gl2,np.logical_and( img[ll1]==0, img[ll2]==0 ).any() )


def main():
    # test_draw_level_set()
    # test_draw_level_line()
    test_draw_five_level_lines()
    # test_intersection_level_lines()

if __name__=='__main__':
    main()

