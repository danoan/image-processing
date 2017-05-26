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
import tjoints as TJ

INF = 1e20

def are_compatible(tj1,tj2):
    for l1 in tj1["levels"]:
        for l2 in tj2["levels"]:
            if (l1[0]==l2[1] and l1[1]==l2[0]):
                return (True,l1)
    return (False,None)

def geodesic(tj1,tj2):
    flag,level = are_compatible(tj1,tj2)
    if flag:
        p1 = tj1["grid"]
        p2 = tj2["grid"]
        d = (np.abs(p2[0] - p1[0])**2 + np.abs(p2[1] - p1[1])**2)**0.5
        if d < 3:#There is a problem in the gathering of levels. This problem makes likely to connect points that are very close to each other, actually, to connect neighbors.
            return (INF,level)            
        return (d,level)
    else:
        return (INF,None)

def select_energy(tjoints,M,i,length):
    energies = []
    st = lambda x: tjoints[x]

    if length==1:
        value,level = geodesic(st(i),st(i+1))
        energies.append( {"key":[ ( (i,i+1),True,level) ],"value":value} )
    else:
        value,level = geodesic(st(i),st(i+length))
        energies.append( {"key":[ ( (i,i+length),True,level),( (i+1,i+length-1),False,None) ], 
                          "value":value + M[i+1][i+length-1]["value"] } )
        for l in range(1,length,2):
            energies.append( {"key": [ ( (i,i+l),False,None),( (i+l+1,i+length),False,None) ],
                              "value": M[i][i+l]["value"] + M[i+l+1][i+length]["value"] } )

    return min(energies,key=lambda x:x["value"])

def go_deep(M,key):
    if key[1]==True:
        if key[2] is not None:
            return [ (key[0],key[2]) ]
        else:
            return []
    else:
        i,j = key[0]
        connections = []
        for k in M[i][j]["key"]:
            connections.extend( go_deep( M,k ) )

        return connections

def match_tjoints_pairs(tjoints_list):
    n = len(tjoints_list) #it must be pair
    if n%2==1:
        n=n-1

    print(n)
    M = [ [{"key":[ ( (0,0),True,None) ],"value":INF}]*n for i in range(n) ]
    for length in range(1,n,2):            
        for i in range(0,n-length):                        
            M[i][i+length] = select_energy(tjoints_list ,M,i,length)

    solution = M[0][n-1]
    connections = []    
    for k in solution["key"]:
        connections.extend( go_deep(M,k) )

    return connections

def test_match():
    img_file = "img/lena_256.png"
    img = misc.imread(img_file) 

    level_line = LL.compute_level_line(img,120)
    
    rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )
    grid = HI.region_to_half_grid(rect)
    extended_grid = HI.add_level_information(img,grid)

    tjoints_grid = {}
    levels = [ 15*i for i in range(0,18) ]    
    for level in levels:
        level_line = LL.compute_level_line(img,level)
        level_intersection = RI.intersect_region_level_line( rect.extended_boundary,level_line)

        tjoints_grid.update( TJ.compute_level_tjoints(extended_grid,level_intersection) )
    
    extended_tjoints = TJ.create_intermediate_levels(tjoints_grid)     

    for k,v in extended_tjoints.items():
        extended_tjoints[k]["grid"] = k

    tjoints_list = sorted(extended_tjoints.values(),key=lambda x:x["order"])

    connections = match_tjoints_pairs(tjoints_list)
    print(connections)




def main():
    test_match()

if __name__=='__main__':
    main()