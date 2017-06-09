#/usr/bin/python3
#coding:utf-8

import random

import numpy as np
from scipy import misc,ndimage
import matplotlib.pyplot as plt
from skimage.draw import line

import rectangular_region as RR
import region_intersection as RI
import half_integer_grid as HI
import level_lines as LL
import tjoints as TJ
import match_tjoints as MT

OPEN = 1
CLOSE = 2

def paint_line(img,x0,y0,x1,y1,color):
	#Remember rows means Y and collumns means X
	rows,columns = line( y0,x0,y1,x1)
	if color is not None:
		img[rows,columns] = color
	return list( zip(columns,rows) )

def fill_in_colors(img,tj_open,tj_close,last_line):
	x0,y0 = tj_open["pixels"][0]
	x1,y1 = tj_close["pixels"][0]
	color = tj_open["levels"][0]
	print(x0,y0,x1,y1,color)
	curr_line = paint_line(img,x0,y0,x1,y1,color)	
	# fill_between_lines(img,last_line,curr_line,color)
	return curr_line

def fill_between_lines(img,lower_line,upper_line,color):
    i,j=0,0
    upper_y = 49
    bottom_y = 71
    # upper_y = 29
    # bottom_y = 51    

    while i < len(lower_line) and j < len(upper_line):      
        p = (p_x,p_y) = lower_line[i]
        q = (q_x,q_y) = upper_line[j]

        r = (r_x,r_y) = (p_x,p_y-1)
        while (r_y >= q_y) and (r_y >= upper_y) :
            print(p,r)
            img[r[1],r[0]] = color
            # return
            r_y = r_y-1
            r = (r_x,r_y)

            if r_x == q_x and r_y==q_y:
                break

        if r_x == q_x:
            j+=1
        i+=1

    
    while j < len(upper_line):      
        q = (q_x,q_y) = upper_line[j]

        r = (r_x,r_y) = (q_x,q_y+1)
        while (r_y <= bottom_y):
            img[r[1],r[0]] = color
            r_y = r_y+1
            r = (r_x,r_y)

        j+=1    

def draw_connections(img,connections,tjoints_list):
	dict_connections = {}
	for i,(indexes,levels) in enumerate(connections):
		c1,c2 = indexes
		l1,l2 = levels
		dict_connections.update( {tjoints_list[c1]["grid"]:{"conn_index":i,"type":OPEN,"levels":levels,"pixels":tjoints_list[c1]["pixels"]} })
		dict_connections.update( {tjoints_list[c2]["grid"]:{"conn_index":i,"type":CLOSE, "levels":levels,"pixels":tjoints_list[c2]["pixels"]} })
		

	stack = []
	last_line = [(50,70)]
	for tj in tjoints_list:
		if tj["grid"] in dict_connections:
			if dict_connections[tj["grid"]]["type"]==OPEN:
				stack.append(dict_connections[tj["grid"]])
			else:
				tj_open = stack.pop()
				tj_close = dict_connections[tj["grid"]]
				last_line = fill_in_colors(img,tj_open,tj_close,last_line)	


def test_draw_connections(img_file,rect=None,levels=None):
    img = misc.imread(img_file) 
    
    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    if levels is None:
        levels = [ 1*i for i in range(0,256) ]        


    grid = HI.region_to_half_grid(rect)
    extended_grid = HI.add_level_information(img,grid)

    tjoints_grid = {}
    
    for level in levels:
        level_line = LL.compute_level_line(img,level)
        level_intersection = RI.intersect_region_level_line( rect.extended_boundary,level_line)

        tjoints_grid.update( TJ.compute_level_tjoints(extended_grid,level_intersection) )
    
    extended_tjoints = TJ.create_intermediate_levels(tjoints_grid) 	

    for k,v in extended_tjoints.items():
        extended_tjoints[k]["grid"] = k

    tjoints_list = sorted(extended_tjoints.values(),key=lambda x:x["order"])

    connections = MT.match_tjoints_pairs(tjoints_list)
    # print(connections)

    img[rect.closure[:,1],rect.closure[:,0]] = 255

    draw_connections(img,connections,tjoints_list)

    plt.imshow(img,cmap='gray')
    plt.show()    

def test_paint_lines(img_file,lines=None,rect=None):
    img = misc.imread(img_file)     

    if rect is None:
        rect = RR.RectangularRegion( (50,50), (50,70), (70,70), (70,50) )

    if lines is None:
        lines = [ [52,71,55,71,107],[60,71,63,71,154],[59,71,64,71,143],[50,71,66,71,102],[49,51,67,71,102],[70,71,71,71,104],[69,71,71,70,104],[71,67,71,66,100],[71,68,71,65,109],[68,71,71,63,105],[71,62,71,59,108],[49,50,71,58,105],[49,50,71,57,105],[71,53,71,52,103],[65,49,64,49,122] ]
    
    img[rect.closure[:,1],rect.closure[:,0]] = 255
        
    colors = np.linspace(0,180,len(lines))
    for i,line in enumerate(lines):
        paint_line(img,line[0],line[1],line[2],line[3],colors[i])

    plt.imshow(img,cmap='gray')
    plt.show()    


def main():
    img_gradient = "img/gradient.png"    
    img_lena = "img/lena_256.png"     
    test_draw_connections(img_lena)
    # test_paint_lines(img_lena)

if __name__=='__main__':
    main()