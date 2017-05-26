#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt

class RectangularRegion:
    def __init__(self,p0,p1,p2,p3):
        self.corners = np.array( [p0,p1,p2,p3] )
        self.closure = rectangular_closure_points(self.corners)
        self.boundary = counterclockwise_rectangular_boundary(*self.corners)
        self.extended_boundary = extended_boundary(p0,p1,p2,p3)

        self.directions = compute_directions(self.extended_boundary)


def extended_boundary(p0,p1,p2,p3):
    np0 = (p0[0]-1,p0[1]-1)
    np1 = (p1[0]-1,p1[1]+1)
    np2 = (p2[0]+1,p2[1]+1)
    np3 = (p3[0]+1,p3[1]-1)
    return counterclockwise_rectangular_boundary(np0,np1,np2,np3)

def compute_directions(boundary):
    dict_directions = { tuple(p):{"in":(0,0),"out":(0,0)} for p in boundary}
    
    boundary_list = boundary.tolist()
    for p,q in zip(boundary_list,boundary_list[1:] + boundary_list[0:1]):
        dict_directions[tuple(p)]["out"] = ( q[0]-p[0],q[1]-p[1] )
        dict_directions[tuple(q)]["in"] =  (  q[0]-p[0],q[1]-p[1] ) 

    return dict_directions   

def rectangular_closure_points(corners):
    INF = 1e20
    min_x,min_y = INF,INF
    max_x,max_y = 0,0
    for coords in corners:
        x,y = coords
        min_x = x if x < min_x else min_x
        min_y = y if y < min_y else min_y

        max_x = x if x > max_x else max_x
        max_y = y if y > max_y else max_y       
    return np.array( [ [x,y] for x in range(min_x,max_x+1) for y in range(min_y,max_y+1) ], dtype='int64' )
    

def counterclockwise_rectangular_boundary(p0,p1,p2,p3):
    sorted_points = [p0,p1,p2,p3]
    boundary_points = []
    for p,q in zip(sorted_points,sorted_points[1:] + sorted_points[0:1]):
        x0,y0 = p
        x1,y1 = q

        x,y = x0,y0
        sx = 0 if (x1-x0)==0 else (x1-x0)/(np.abs(x1-x0))
        sy = 0 if (y1-y0)==0 else (y1-y0)/(np.abs(y1-y0)) 
        while not(x==x1 and y==y1):
            x+= sx
            y+= sy

            boundary_points.append( (x,y) )

    return np.array( boundary_points, dtype='int64' )


def test_paint_boundary():
    img_file = "img/lena_256.png"
    img = misc.imread(img_file)     
    rect = RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    img[rect.boundary[:,1],rect.boundary[:,0]] = 255
    plt.imshow(img,cmap="gray")
    plt.show()

def test_paint_closure():
    img_file = "img/lena_256.png"
    img = misc.imread(img_file)     
    rect = RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    img[rect.closure[:,1],rect.closure[:,0]] = 255
    plt.imshow(img,cmap="gray")
    plt.show()

def test_paint_extended_boundary():
    img_file = "img/lena_256.png"
    img = misc.imread(img_file)     
    rect = RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    img[rect.closure[:,1],rect.closure[:,0]] = 255
    img[rect.extended_boundary[:,1],rect.extended_boundary[:,0]] = 200
    plt.imshow(img,cmap="gray")
    plt.show()  

def test_compute_directions():
    rect = RectangularRegion( (50,50), (50,70), (70,70), (70,50) )      
    for k,v in rect.directions.items():
        if v["in"]==(0,0) or v["out"]==(0,0):
            print(k)

def main():
    # test_paint_boundary()
    # test_paint_closure()
    # test_paint_extended_boundary()
    test_compute_directions()

if __name__=='__main__':
    main()
