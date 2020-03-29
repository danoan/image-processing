import os,sys
PROJECT_FOLDER=os.path.dirname(os.path.realpath(__file__))
sys.path.append( "{}/packages".format(PROJECT_FOLDER) )

import argparse

import numpy as np
from scipy import misc

import matplotlib.pyplot as plt
from improc.denoise import chambolle,rof,tikhonov,fista

def read_input():
	parser = argparse.ArgumentParser(description="Denoising tools")

	parser.add_argument("input_image",type=str,action="store",help="Image to be denoised.")
	parser.add_argument("algorithm",type=str,action="store", help="Choose among {tikhonov, rof, chambolle, fista}.")

	parser.add_argument("-l",dest="lbda",type=float,action="store",default=0.12,help="Regularization weight.")
	parser.add_argument("-t",dest="tolerance",type=float,action="store",default=1e-5,help="Stop if the new energy value differs of less than [tolerance].")
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

def main():
	id = read_input()

	noisy_img = np.asfarray( misc.imread(id.input_image) )
	noisy_img /= 255.0
	noisy_img = make3channel(noisy_img)


	if id.algorithm=="chambolle":
		dimg = chambolle.denoise_image(noisy_img, id.lbda, id.tolerance, id.max_iterations,id.verbose)
	elif id.algorithm=="rof":
		dimg = rof.denoise_image(noisy_img, id.lbda, id.tolerance, id.max_iterations, id.verbose)
	elif id.algorithm=="fista":
		dimg = fista.denoise_image(noisy_img, id.lbda, id.max_iterations)
	elif id.algorithm=="tikhonov":
		dimg = tikhonov.denoise_image(noisy_img, id.lbda, id.max_iterations,id.verbose)

	fig,axs=plt.subplots(1,2)
	axNoisy,axDenoise = axs

	axNoisy.imshow(noisy_img)
	axDenoise.imshow(dimg)
	plt.show()

	if id.output_image:
		if not os.path.exists(os.path.dirname(id.output_img)):
			os.makedirs(os.path.dirname(output_img))
		axDenoise.savefig(output_img)


if __name__=="__main__":
	main()