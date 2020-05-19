import os,sys
PROJECT_FOLDER=os.path.dirname(os.path.realpath(__file__))
sys.path.append( "{}/packages".format(PROJECT_FOLDER) )

import argparse

import numpy as np
from scipy import misc

import matplotlib.pyplot as plt
from improc.denoise import chambolle,rof,tikhonov,fista,rof_modified_curvature

def read_input():
	parser = argparse.ArgumentParser(description="Denoising tools")

	parser.add_argument("input_image",type=str,action="store",help="Image to be denoised.")
	parser.add_argument("algorithm",type=str,action="store", help="Choose among {tikhonov, rof, chambolle, fista}.")

	parser.add_argument("-l",dest="lbda",type=float,action="store",default=0.12,help="Regularization weight.")
	parser.add_argument("-t",dest="tolerance",type=float,action="store",default=1e-5,help="Stop if the new energy value differs of less than [tolerance].")
	parser.add_argument("-e",dest="ev_stop",type=float,action="store",default=None,help="Stop if energy reaches this value.")
	parser.add_argument("-i",dest="max_iterations",type=int,action="store",default=100,help="Stop after the i-th iteration.")
	parser.add_argument("-o",dest="output_image",type=str,action="store",help="Output image filepath.")
	parser.add_argument("-v",dest="verbose",action="store_true",help="Print algorithms outputs.")

	args = parser.parse_args()
	return args

def make3channel(img):
	if len(img.shape)==2:
		_img = np.zeros( img.shape + (3,) )

		for c in range(3):
			_img[:,:,c] = img.copy()

		img = _img
	return img

def set_plot_no_axes():
	plt.gca().set_axis_off()
	plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
		    hspace = 0, wspace = 0)
	plt.margins(0,0)
	plt.gca().xaxis.set_major_locator(plt.NullLocator())
	plt.gca().yaxis.set_major_locator(plt.NullLocator())

def main():
	inp = read_input()

	noisy_img = np.asfarray( misc.imread(inp.input_image) )
	noisy_img /= 255.0
	noisy_img = make3channel(noisy_img)
	
	if inp.max_iterations<0:
		inp.max_iterations=1e10


	if inp.algorithm=="chambolle":
		dimg = chambolle.denoise_image(noisy_img, inp.lbda, inp.tolerance, inp.max_iterations,inp.verbose)
	elif inp.algorithm=="rof":
		dimg = rof.denoise_image(noisy_img, inp.lbda, inp.tolerance, inp.max_iterations, inp.verbose,inp.ev_stop)
	elif inp.algorithm=="fista":
		dimg = fista.denoise_image(noisy_img, inp.lbda, inp.max_iterations)
	elif inp.algorithm=="tikhonov":
		dimg = tikhonov.denoise_image(noisy_img, inp.lbda, inp.max_iterations,inp.verbose)
	elif inp.algorithm=="rof_curvature":
		dimg = rof_modified_curvature.denoise_image(noisy_img, inp.lbda,inp.tolerance, inp.max_iterations,inp.verbose,inp.ev_stop)

	if inp.output_image is not None:
		dirname = os.path.dirname(inp.output_image)
		if not os.path.exists(os.path.dirname(inp.output_image)):
			os.makedirs(dirname)
		set_plot_no_axes()

		plt.imshow(dimg)
		plt.savefig(inp.output_image,bbox_inches = 'tight',pad_inches = 0)
	else:
		fig,axs=plt.subplots(1,2)
		axNoisy,axDenoise = axs

		
		axNoisy.imshow(noisy_img)
		axDenoise.imshow(dimg)
		plt.show()


if __name__=="__main__":
	main()
