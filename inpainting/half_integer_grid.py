#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt

import rectangular_region as RR


def grid_neighbors(x,y):
    eight_neigh_step = [ ( (-0.5,-0.5),{"out":(0,1),"in":(-1,0)} ),
                         ( (-0.5,0),{"out":(0,1),"in":(0,1)}),
                         ( (-0.5,0.5),{"out":(1,0),"in":(0,1)}),
                         ( (0,0.5),{"out":(1,0),"in":(1,0)}), 
                         ( (0.5,0.5),{"out":(0,-1),"in":(1,0)}), 
                         ( (0.5,0),{"out":(0,-1),"in":(0,-1)}), 
                         ( (0.5,-0.5),{"out":(-1,0),"in":(0,-1)}), 
                         ( (0,-0.5),{"out":(-1,0),"in":(-1,0)}) ] #Counterclockwise

    for i in eight_neigh_step:
        yield ( (x+i[0][0],y+i[0][1]),i[1] )

def pixel_neighbors(x,y,direction):
    '''
    0 7 6
    1   5
    2 3 4
    '''
    if direction==(-1,1):   #TOP-LEFT-CORNER
        pixels = [ (x-0.5,y-0.5), (x+0.5,y-0.5), (x+0.5,y+0.5), (x-0.5,y+0.5)]
    elif direction==(1,1):  #BOTTOM-LEFT-CORNER
        pixels = [ (x-0.5,y-0.5), (x+0.5,y-0.5), (x+0.5,y+0.5), (x-0.5,y+0.5)]
    elif direction==(1,-1): #BOTTOM-RIGHT-CORNER
        pixels = [ (x-0.5,y-0.5), (x+0.5,y-0.5), (x+0.5,y+0.5), (x-0.5,y+0.5)]
    elif direction==(-1,-1):#TOP-RIGHT-CORNER
        pixels = [ (x-0.5,y-0.5), (x+0.5,y-0.5), (x+0.5,y+0.5), (x-0.5,y+0.5)]
    elif direction==(0,2):#LEFT-SIDE
        pixels = [ (x-0.5,y),(x+0.5,y) ]
    elif direction==(2,0):#BOTTOM-SIDE
        pixels = [ (x,y-0.5), (x,y+0.5) ]
    elif direction==(0,-2):#RIGHT-SIDE
        pixels = [ (x-0.5,y),(x+0.5,y) ]
    elif direction==(-2,0):#TOP-SIDE
        pixels = [ (x,y-0.5), (x,y+0.5) ]
    else:
        print(x,y)
        pixels = [ (x,y), (x,y) ]

    # print(x,y,direction)
    for i in range(len(pixels)):
        pixels[i] = ( int(pixels[i][0]), int(pixels[i][1]) )

    return pixels

def skip_grid_neighbors(direction):
    '''
    0 7 6
    1   5
    2 3 4
    '''
    if direction==(-1,1):   #TOP-LEFT-CORNER
        return [3,4,5]
    elif direction==(1,1):  #BOTTOM-LEFT-CORNER
        return [5,6,7]
    elif direction==(1,-1): #BOTTOM-RIGHT-CORNER
        return [0,1,7]
    elif direction==(-1,-1):#TOP-RIGHT-CORNER
        return [1,2,3]
    elif direction==(0,2):#LEFT-SIDE
        return [3,4,5,6,7]
    elif direction==(2,0):#BOTTOM-SIDE
        return [0,1,5,6,7]
    elif direction==(0,-2):#RIGHT-SIDE
        return [0,1,2,3,7]
    elif direction==(-2,0):#TOP-SIDE
        return [1,2,3,4,5]

    print(direction)


def region_to_half_grid(region):    
    grid = {}
    order=0
    for p in region.extended_boundary:
        x,y = p
        p_tuple = tuple(p)
        
        d1 = region.directions[p_tuple]["in"]
        d2 = region.directions[p_tuple]["out"]
        direction = (d1[0] + d2[0],d1[1] + d2[1])

        neigh_filter = filter(lambda x: x not in skip_grid_neighbors(direction), range(8) )
        neighborhood = list(grid_neighbors(x,y))
        neighbors = [ neighborhood[i] for i in neigh_filter] 
        
        for n,d in neighbors:
            if n in grid:
                # grid[n]["in"] = d["in"]
                # grid[n]["out"] = d["out"]
                pass
            else:
                grid[n] = {"in":d["in"],"out":d["out"],"order":order}
                grid[n]["pixels"] = [ (x,y) ]

            order+=1

    for k,v in grid.items():
        x,y = k
        d1,d2 = v["in"],v["out"]
        direction = (d1[0] + d2[0],d1[1] + d2[1])        

        grid[k]["pixels"].extend( pixel_neighbors(x,y,direction) )

    return grid

def add_level_information(img,grid):
    for k,v in grid.items():
        levels = []
        for p in v["pixels"][1:]:
            px_level = img[p[1],p[0]]
            levels.append(px_level)

        grid[k].update( {"levels":levels} )

    return grid

def test_region_grid():
    rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )
    grid = region_to_half_grid(rect)

    x = [ k[0] for k in grid.keys() ]
    y = [ k[1] for k in grid.keys() ]

    plt.plot(x,y,'ro')
    plt.show()

def test_directions():
    rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )
    grid = region_to_half_grid(rect)  
    # print(grid)

    x = [ k[0] for k in grid.keys() ]
    y = [ k[1] for k in grid.keys() ]

    plt.plot(x[::3],y[::3],'ro')

    i=0
    for k,v in grid.items():
        i+=1
        if i%3!=0:
            continue
        x,y = k
        direction = v["out"]
        plt.arrow( x,y,direction[0]*0.2,direction[1]*0.2,color='g',head_width=0.5,head_length=0.5 )

    plt.show()




def main():
    # test_region_grid()
    test_directions()

if __name__=='__main__':
    main()
