import os,sys
import argparse

import numpy as np
from skimage.io import imread

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def set_plot_no_axes():
	plt.gca().set_axis_off()
	plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
		    hspace = 0, wspace = 0)
	plt.margins(0,0)
	plt.gca().xaxis.set_major_locator(plt.NullLocator())
	plt.gca().yaxis.set_major_locator(plt.NullLocator())

def read_input():
	parser = argparse.ArgumentParser(description="Denoising tools")

	parser.add_argument("input_image",type=str,action="store",help="Image to be denoised.")
	parser.add_argument("output_image",type=str,action="store",help="Output image filepath.")
	parser.add_argument("-l",dest="levels",type=int,nargs='*',default=[], action="store",help="List of levels to plot.")
	parser.add_argument("-c",dest="colors",type=str,nargs='*',action="store",help="Level set color sequence.")


	args = parser.parse_args()
	return args

def graph_img_plot(image_filepath, output_filepath,levels=[],colors=None):
	img = imread(image_filepath,as_gray=True)
	
	levels = [ i/255.0 for i in levels ]

	h,w = img.shape
	X=np.arange(0,w,1)
	Y=np.arange(0,h,1)
	X,Y = np.meshgrid(X,Y)
	Z=img

	fig,ax = plt.subplots()
	plt.gca().invert_yaxis()

	if colors is None:
		ax.contour(X,Y,Z,levels,cmap=cm.viridis)
	else:
		ax.contour(X,Y,Z,levels,colors=colors)

	dirname = os.path.dirname(output_filepath)
	if not os.path.exists(os.path.dirname(output_filepath)):
		os.makedirs(dirname)

	set_plot_no_axes()
	plt.savefig(output_filepath,bbox_inches = 'tight',pad_inches = 1)	


def main():
	inp = read_input()
	graph_img_plot(inp.input_image,inp.output_image,inp.levels,inp.colors)

		


if __name__=="__main__":
	main()
