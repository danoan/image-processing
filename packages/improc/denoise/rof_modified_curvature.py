import numpy as np

from improc.utils import finite_differences as FD

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

class DerivativeData:
	def __init__(self,u):
		self.shape = u.shape
		self.nchannels =u.shape[2]

		self.uf = np.zeros( (2,) + self.shape )
		self.ub = np.zeros( (2,) + self.shape )

		for c in range(self.nchannels):
			self.uf[:,:,:,c] = FD.forward_differences(u[:,:,c])
			self.ub[:,:,:,c] = FD.backward_differences(u[:,:,c])

	def fx(self,c):
		return self.uf[1,:,:,c]

	def fy(self,c):
		return self.uf[0,:,:,c]

	def bx(self,c):
		return self.ub[1,:,:,c]

	def by(self,c):
		return self.ub[0,:,:,c]


def compute_gradient(u0,u,lbda):
	'''
		u0: Function at step ZERO
		u: Function obtained after the last step of gradient_descent 
		lbda: Lagrange Multiplier. In this implementation it is a parameter instead
			  of a variable. It controls the 'smoothness' of the final image.
	'''
	avoid_div_zero = 1e-5

	DD=DerivativeData(u)

	x_den=0
	gx= np.zeros( DD.shape )

	y_den=0
	gy= np.zeros( DD.shape )

	for c in range(DD.nchannels):
		norm_grad=(DD.fx(c)**2 + DD.fy(c)**2)**0.5

		x_den = (DD.fx(c)**2 + minmod(DD.fy(c),DD.by(c))**2 + avoid_div_zero)**0.5
		gx[:,:,c] = norm_grad*FD.backward_differences( DD.fx(c)/x_den )[1]

		y_den = ( DD.fy(c)**2 + minmod(DD.fx(c),DD.bx(c))**2 + avoid_div_zero)**0.5
		gy[:,:,c] = norm_grad*FD.backward_differences( DD.fy(c)/y_den)[0]

	return ( gx + gy - lbda*(u-u0) )

def compute_tv(u):
	shape = u.shape
	uf = np.zeros( (2,) + shape )
	for c in range(shape[2]):
		uf[:,:,:,c] = FD.forward_differences(u[:,:,c])

	tv=0
	for c in range( shape[2] ):
		tv+=np.sum( uf[1,:,:,c]**2 + uf[0,:,:,c]**2 )**0.5

	return tv

def gradient_descent(w,lbda,error_tol=1e-4,max_it=1000,
					max_alpha_it=10,min_grad_rate=0.5,min_grad_step=1.0,print_output=False,ev_stop=None):
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
		if ev_stop is not None:
			if tv <= ev_stop:
				break
		g = compute_gradient(w,u,lbda)
		gsum = np.sum(g)

		tv_0 = tv
		u0 = u	
		for alpha in alpha_list:
			d = alpha*g
			u = u0 + d

			tv = compute_tv(u)

			if ( (tv-tv_0) < 0.1*alpha*gsum ):
				break
		if print_output:
			print("it: {0} ; tv0: {1:.5f}; tv: {2:.5f} ; diff: {3:.5f} ; alpha: {4:.6f}".format (it_main,tv_0,tv,tv_0-tv,alpha) )
		
	
		it_main+=1

	return u

def denoise_image(img,lbda,error_tol,max_it,print_output=False,ev_stop=None):
	if print_output:
		print("Executing ROF Curvature...")
	return gradient_descent(img,lbda,error_tol,max_it,print_output=print_output,ev_stop=ev_stop)



