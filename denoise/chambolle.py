import sys, getopt

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

def forward_differences(u):
	'''
		u: Image matrix of dimensions (y,x)
		returns matrix fu of dimensions (2,y,x)
	'''
	fu = np.zeros( [2] + list(u.shape) )

	fu[0,:-1,:] = u[1:,:] - u[:-1,:]	#y differences
	fu[1,:,:-1] = u[:,1:] - u[:,:-1]	#x differences

	return fu

def backward_differences(u):
	'''
		u: Image matrix of dimensions (y,x)
		returns matrix fu of dimensions (2,y,x)
	'''
	fu = np.zeros( [2] + list(u.shape) )

	fu[0,1:,:] = u[1:,:] - u[:-1,:]	#y differences
	fu[1,:,1:] = u[:,1:] - u[:,:-1]	#x differences

	return fu	

def compute_gradient(A):
	return forward_differences(A)

def compute_divergence(p):
	n,m = p.shape[1:]

	sum_x = np.zeros( (n,m) )
	sum_y = np.zeros( (n,m) )

	sum_y[1:-1] = p[0][1:-1,:] - p[0][0:-2,:]
	sum_y[0] = p[0][0]
	sum_y[-1] = -p[0][-2]

	sum_x[:,1:-1] = p[1][:,1:-1] - p[1][:,0:-2]
	sum_x[:,0] = p[1][:,0]
	sum_x[:,-1] = -p[1][:,-2]

	return sum_x + sum_y

def compute_objective_function(lbda,p,g):
	n = lbda*compute_divergence(p) - g
	return np.sum(n*n)

def solve_projection(img,lbda,error_tol,max_it,print_output):
	n,m = img.shape
	
	g = img
	p0 = np.zeros( (2,n,m) )
	it = 1
	ONE = np.ones( (n,m) )

	t = 1/4.0

	while it < max_it:
		val_p0 = compute_objective_function(lbda,p0,g)

		div_p = compute_divergence(p0)
		f1 = compute_gradient(div_p - g/lbda)

		p = ( p0 + t*(f1) ) / (ONE + t*(np.sqrt(f1**2)).sum(axis=0))
		val_p = compute_objective_function(lbda,p,g)

		p0 = p

		if print_output:
			print("it: %d ; diff: %.2f ; t: %.6f\n" % (it,val_p-val_p0,t) )				

		if ( np.abs( val_p-val_p0) < error_tol ):
			break
		it+=1

	
	return lbda*compute_divergence(p)

def denoise_image(img_path,lbda,error_tol,max_it,print_output=False):
	img = np.asfarray( misc.imread(img_path) )
	p = solve_projection(img,lbda,error_tol,max_it,print_output)
	
	denoised_img = img - p
	denoised_img = np.asarray( np.trunc(denoised_img), dtype='uint8' )

	return denoised_img


