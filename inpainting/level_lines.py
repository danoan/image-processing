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

def test_draw_level_set(img_file,level):
    img = misc.imread(img_file)

    uls = compute_upper_level_set(img,level)	
    img[uls] = 0
    img[np.invert(uls)] = 255

    plt.imshow(img,cmap="gray")
    plt.show()


def test_draw_level_lines(img_file,levels):
    img = misc.imread(img_file)

    level_lines = [ compute_level_line(img,level) for level in levels]

    img[ level_lines[0] ] = 0; img[np.invert( level_lines[0] )] = 255
    for ll in level_lines[1:]:
        img[ll] = 0

    plt.imshow(img,cmap="gray")
    plt.show()

def test_intersection_level_lines(img_file,l1=None,l2=None):
    img = misc.imread(img_file)

    if l1 is None or l2 is None:
        l1,l2 = random.sample( range(256),2 )


    ll1=compute_level_line(img,l1)
    ll2=compute_level_line(img,l2)

    print( l1,l2,np.logical_and( img[ll1]==0, img[ll2]==0 ).any() )


def main():
    img_gradient = "img/gradient.png"    
    img_lena = "img/lena_256.png"    

    # test_draw_level_set(img_lena,100)
    # test_draw_level_line(img_lena,100)
    test_draw_level_lines(img_lena,[100,200])
    # test_intersection_level_lines(img_lena)

if __name__=='__main__':
    main()

