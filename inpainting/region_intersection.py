#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt

import level_lines as LL
import rectangular_region as RR


def intersect_region_level_line(region_extended_boundary,level_line):
    #region_boundary: all pixes in the boundary
    #level_line: img array. Value equals to one if correspondent pixel belongs to level line
    temp = np.zeros( level_line.shape, dtype="int8")

    temp[region_extended_boundary[:,1],region_extended_boundary[:,0]] = 2
    inters_candidates = temp[level_line]
    
    level_line[level_line] = (inters_candidates == 2)

    return level_line

def test_intersection(img_file,rect=None,levels=None):
    img = misc.imread(img_file)	

    if levels is None:
        levels = [i*5 for i in range(50)]

    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    level_lines = []
    for l in levels:
        level_line = LL.compute_level_line(img,l)   
        level_lines.append(level_line)        


    img[rect.extended_boundary[:,1],rect.extended_boundary[:,0]] = 200	

    for lvl in level_lines:
        intersection = intersect_region_level_line(rect.extended_boundary,lvl)
        print(intersection.any())
        img[intersection] = 100

    plt.imshow(img,cmap="gray")
    plt.show()

def main():
    img_gradient = "img/gradient.png"    
    img_lena = "img/lena_256.png"      
    
    test_intersection(img_lena)

if __name__=='__main__':
    main()    