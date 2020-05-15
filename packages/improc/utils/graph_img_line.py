import os,sys
import argparse

import numpy as np
from skimage.io import imread

import matplotlib.pyplot as plt

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

	parser.add_argument("-y",type=int,action="store",default=0,help="Image row to graph.")


	args = parser.parse_args()
	return args

def graph_img_line(image_filepath, row ,output_filepath):
	img = imread(image_filepath,as_gray=True)

	h,w = img.shape
	x=list(range(w))
	y=[ img[row,x] for x in range(w)]

	dirname = os.path.dirname(output_filepath)
	if not os.path.exists(os.path.dirname(output_filepath)):
		os.makedirs(dirname)

	set_plot_no_axes()
	plt.plot(x,y)
	plt.savefig(output_filepath,bbox_inches = 'tight',pad_inches = 1)	


def main():
	inp = read_input()
	graph_img_line(inp.input_image,inp.y,inp.output_image)

		


if __name__=="__main__":
	main()
