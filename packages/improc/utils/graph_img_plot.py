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

	parser.add_argument("-s",dest="show",action="store_true",help="Show plot")


	args = parser.parse_args()
	return args

def graph_img_plot(image_filepath, output_filepath,show_plot=False):
	img = imread(image_filepath,as_gray=True)

	h,w = img.shape
	X=np.arange(0,w,1)
	Y=np.arange(0,h,1)
	X,Y = np.meshgrid(X,Y)
	Z=img

	fig = plt.figure()
	ax = Axes3D(fig,azim=60,elev=60)

	ax.set_zlim(0,1)
	ax.plot_surface(X,Y,Z,cmap=cm.viridis)

	dirname = os.path.dirname(output_filepath)
	if not os.path.exists(os.path.dirname(output_filepath)):
		os.makedirs(dirname)

	plt.savefig(output_filepath,bbox_inches = 'tight',pad_inches = 1)	

	if show_plot:
		plt.show()



def main():
	inp = read_input()
	graph_img_plot(inp.input_image,inp.output_image,inp.show)

		


if __name__=="__main__":
	main()
