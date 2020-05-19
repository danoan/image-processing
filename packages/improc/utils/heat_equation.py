#!/usr/bin/python3

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from skimage.io import imread
from skimage.util import img_as_ubyte

from graph_img_line import graph_img_line

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

	parser.add_argument("-l",dest="lbda",type=float,action="store",default=0.12,help="Regularization weight.")
	parser.add_argument("-s",dest="step",type=float,action="store",default=0.1,help="Time step.")
	parser.add_argument("-t",dest="tolerance",type=float,action="store",default=1e-5,help="Stop if the new energy value differs of less than [tolerance].")
	parser.add_argument("-e",dest="ev_stop",type=float,action="store",default=None,help="Stop energy equal this value.")
	parser.add_argument("-i",dest="max_iterations",type=int,action="store",default=100,help="Stop after the i-th iteration.")
	parser.add_argument("-o",dest="output_image",type=str,action="store",help="Output image filepath.")
	parser.add_argument("-v",dest="verbose",action="store_true",help="Print algorithms outputs.")

	args = parser.parse_args()
	return args


def flow(u,step,lbda,epsilon):
	w,h=u.shape
	z=np.array(u,dtype=np.float32)

	z[1:-1,:] += step*lbda*(u[2:,:] - 2*u[1:-1,:]  + u[0:-2,:])
	z[:,1:-1] += step*lbda*(u[:,2:] - 2*u[:,1:-1]  + u[:,0:-2])


	diff = u-z
	sdiff=np.sum(diff**2)
	if(sdiff<epsilon):
		return (z,True,sdiff)
	return (z,False,sdiff)

def compute_gradient_square_norm(u):
	#return | grad u |^2
	dux=np.zeros(u.shape)
	duy=np.zeros(u.shape)

	dux[0:-1,:] += ( u[1:,:] - u[0:-1,:] )
	duy[:,0:-1] += ( u[:,1:] - u[:,0:-1] )

	return np.sum(dux**2 + duy**2)

def main():
	inp = read_input()
	#u=np.array( img_as_ubyte( imread(inp.input_image,as_gray=True) ),dtype=np.float32 )
	u=np.array( imread(inp.input_image,as_gray=True),dtype=np.float32 )

	print("Initial energy: ", compute_gradient_square_norm(u))

	nit=0
	while True:
		u,flag,sdiff=flow(u,inp.step,inp.lbda,inp.tolerance)
		if flag:
			break

		nit+=1
		if nit%1==0:
			if inp.verbose:
				print(nit,":",sdiff,compute_gradient_square_norm(u))

		if inp.ev_stop is not None and compute_gradient_square_norm(u) <= inp.ev_stop:
			break
		
		if inp.max_iterations>=0 and nit>inp.max_iterations:
			break

	plt.imshow(u,cmap="gray")

	if inp.output_image is not None:
		dirname=os.path.dirname(inp.output_image)
		if not os.path.exists(os.path.dirname(inp.output_image)):
			os.makedirs(dirname)

		set_plot_no_axes()
		plt.savefig(inp.output_image,bbox_inches = 'tight',pad_inches = 0)
	else:
		plt.show()
	

if __name__=='__main__':
	main()
