import sys, getopt

import numpy as np
from scipy import misc

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

def minmod(A,B):
	'''
		Let a,b elements of matrics A and B.
		if a and b have different signs then res = 0
		else then the minimum absolute value between both is returned

		It always returns ZERO or a positive value.
	'''
	res = (np.sign(A)+np.sign(B))/2
	res*= np.minimum( np.absolute(A),np.absolute(B) )
	return res

def compute_gradient(u0,u,lbda):
	'''
		u0: Function at step ZERO
		u: Function obtained after the last step of gradient_descent 
		lbda: Lagrange Multiplier. In this implementation it is a parameter instead
			  of a variable. It controls the 'smoothness' of the final image.
	'''
	avoid_div_zero = 1e-5
	
	uf = forward_differences(u)
	ub = backward_differences(u)


	x_den = (uf[1]**2 + minmod(uf[0],ub[0])**2)**0.5 + avoid_div_zero
	gx = backward_differences( uf[1]/x_den )[1]

	y_den = ( uf[0]**2 + minmod(uf[1],ub[1])**2 + avoid_div_zero)**0.5
	gy = backward_differences( uf[0]/y_den)[0]

	return ( gx + gy - lbda*(u-u0) )

def compute_tv(u):
	uf = forward_differences(u)
	return np.sum( uf[1]**2 + uf[0]**2 )**0.5

def gradient_descent(w,lbda,error_tol=1e-4,max_it=1000,
					max_alpha_it=20,min_grad_rate=0.5,min_grad_step=1.0,print_output=False):
	'''
		lbda: Smoothness level of final image
		error_tol: Method stops after difference between two last iterations equal this value
		max_it: Method stops after this number of iterations.
		max_alpha_it(mit): Armijo condition's alpha. If mit = 4, then 1 >= alpha > (0.5)^(mit)
	'''

	u0 = u = w
	it_main = 1
	
	tv=compute_tv(u)
	tv_0 = 10*tv

	alpha_list = [1]*max_alpha_it
	for i in range(0,max_alpha_it):
		alpha_list[i] = alpha_list[i-1]*0.5

	while ( np.abs(tv - tv_0) > error_tol and it_main < max_it):
		g = compute_gradient(w,u,lbda)
		gsum = np.sum(g)

		# print(gsum)

		tv_0 = tv
		u0 = u	
		for alpha in alpha_list:
			d = alpha*g
			u = u0 + d

			tv = compute_tv(u)
			if ( (tv-tv_0) < alpha*gsum ):
				break
		if print_output:
			print("it: %d ; tv0: %.2f ; tv: %.2f ; alpha: %.6f\n" % (it_main,tv_0,tv,alpha) )				
		
	
		it_main+=1

	return u

def denoise_image(img_path,lbda,error_tol,max_it,max_alpha_it,print_output=False):
	img = np.asfarray( misc.imread(img_path) )
	denoised_img = gradient_descent(img,lbda,error_tol,max_it,max_alpha_it,print_output)	
	denoised_img = np.asarray( np.trunc(denoised_img), dtype='uint8' )

	return denoised_img



