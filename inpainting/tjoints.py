#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt

import rectangular_region as RR
import region_intersection as RI
import half_integer_grid as HI
import level_lines as LL

def compute_level_tjoints(region_grid, level_intersection):
    h,w = level_intersection.shape
    pixel_map = np.array( [ [ (j,i) for i in range(w) ] for j in range(h) ] )
    candidates = pixel_map[level_intersection]
    # print(candidates)
    tjoints = {}
    for p in candidates:
        x,y = p
        for g,d in HI.grid_neighbors(x,y):
            if g in region_grid:                
                # print( region_grid[g]["pixels"],region_grid[g]["levels"] )
                if len(region_grid[g]["levels"])>1:
                    # print("OK")
                    tjoints.update( {g:region_grid[g]} )

    return tjoints

def create_intermediate_levels(tjoints):
    for grid,data in tjoints.items():        
        levels = list(data["levels"])
        for l1,l2 in zip(levels,levels[1:]):
            step = 1 if l2>l1 else -1
            sum_flag = 0 if l2==l1 else 1

            fill_in_levels = []
            fill_in_levels.extend( list( range(l1,l2+step*sum_flag, step) ) )
            data["levels"] = list( zip( fill_in_levels,fill_in_levels[1:] ) )
            
        data["grid"] = grid
        

    return tjoints


def test_tjoints_levels(img_file,rect=None,levels=None):
    img = misc.imread(img_file) 

    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )            

    if levels is None:
        levels = [ 5*i for i in range(0,51) ]    

    grid = HI.region_to_half_grid(rect)
    extended_grid = HI.add_level_information(img,grid)

    tjoints_grid = {}
    
    for level in levels:
        level_line = LL.compute_level_line(img,level)
        level_intersection = RI.intersect_region_level_line( rect.extended_boundary,level_line)

        tjoints_grid.update( compute_level_tjoints(extended_grid,level_intersection) )

    # print( len(tjoints_grid.keys()) )

    x=[];y=[]
    for k,v in tjoints_grid.items():
        x.append( k[0] )
        y.append( k[1] )
    

    plt.plot(x,y,'bo')
    plt.show()    

def test_intermediate_levels(img_file,level,rect=None):
    img = misc.imread(img_file) 

    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    level_line = LL.compute_level_line(img,level)
    
    grid = HI.region_to_half_grid(rect)
    extended_grid = HI.add_level_information(img,grid)

    level_intersection = RI.intersect_region_level_line( rect.extended_boundary,level_line)
    
    tjoints_grid = compute_level_tjoints(extended_grid,level_intersection)
    extended_tjoints = create_intermediate_levels(tjoints_grid)    

    for k,v in extended_tjoints.items():
        print(v["levels"])

def test_all_intermediate_levels(img_file,rect=None,levels=None):
    img = misc.imread(img_file) 
   
    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    if levels is None:
        levels = [ 5*i for i in range(0,51) ]            

    grid = HI.region_to_half_grid(rect)
    extended_grid = HI.add_level_information(img,grid)

    tjoints_grid = {}    
    for level in levels:
        level_line = LL.compute_level_line(img,level)
        level_intersection = RI.intersect_region_level_line( rect.extended_boundary,level_line)

        tjoints_grid.update( compute_level_tjoints(extended_grid,level_intersection) )

    extended_tjoints = create_intermediate_levels(tjoints_grid)    

    list_tjoints = extended_tjoints.values()
    list_tjoints = sorted(list_tjoints,key=lambda x: x["order"])
    for data in list_tjoints:
        print(data["grid"]," : ",data["levels"])        

def main():
    img_gradient = "img/gradient.png"    
    img_lena = "img/lena_256.png"     
    # test_all_levels(img_lena)
    # test_intermediate_levels(img_lena,120)
    test_all_intermediate_levels(img_lena)

if __name__=='__main__':
    main()
