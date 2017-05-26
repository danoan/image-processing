import sys,getopt,datetime

import numpy as np
from scipy import misc

import matplotlib.pyplot as plt


#Helper Functions
def normalize_img(img):	
	return img/255.0

def pre_processing_img(img,noise):
	img = normalize_img(img)
	img = add_noise(img,noise/2.0)
	return img

def pos_processing_img(img):
	return img*255	

def add_noise(img,lbda):
	m,n = img.shape
	img += np.random.normal(0,lbda,(m,n))

	return project_on_C(img)
#-------------






#FISTA Routines
def project_on_C(x):
	m,n = x.shape

	x[ x > 1 ] = 1
	x[ x < 0 ] = 0

	return x


def project_on_P(el):
	"""
		Return the projection of el on P.

		The space P is defined by:

		P = { x | x in R^{(m,n)x(m,n)} and |x| <= 1}

		Params:
		el: An element of the ambiance space, [R^{m,n},R^{m,n}].	
	"""
	
	p,q = el[0],el[1]
	m,n = p.shape

	ONES = np.ones( (m,n), dtype=np.float64)

	#From i=1...m-1 and j=1...n-1
	ew_norm_1 = (p[:-1,:-1]**2 + q[:-1,:-1]**2)**0.5
	ew_norm_1_p_max = np.maximum(ONES[:-1,:-2],ew_norm_1[:,:-1])

	#From i=1...m-1 and j=n (Border case)
	ew_norm_2_p = np.absolute(p[:-1,n-2])
	ew_norm_2_p_max = np.maximum(ONES[:-1,0],ew_norm_2_p)

	p[:-1,:-2] = p[:-1,:-2]/ew_norm_1_p_max
	p[:-1,n-2] = p[:-1,n-2]/ew_norm_2_p_max

	ew_norm_1_q_max = np.maximum(ONES[:-2,:-1],ew_norm_1[:-1,:])

	#From i=m and j=1...n-1 (Border case)
	ew_norm_2_q = np.absolute(q[m-2,:-1])
	ew_norm_2_q_max = np.maximum(ONES[0,:-1],ew_norm_2_q)



	q[:-2,:-1] = q[:-2,:-1]/ew_norm_1_q_max
	q[m-2,:-1] = q[m-2,:-1]/ew_norm_2_q_max

	w = np.zeros( (2,m,n), dtype=np.float64 )
	w[0] = p
	w[1] = q

	return w

def compute_linear_operator_LT(x):
	"""
		Return (p,q), each belonging to R^{(m,n)x(m,n)}.

		Params:
		x: R^{(m,n)x(m,n)}
	"""	

	m,n = x.shape

	p,q = np.zeros( (m,n),dtype=np.float64 ),np.zeros( (m,n),dtype=np.float64 )
	p[:-1,:] = x[:-1,:] - x[1:,:]
	q[:,:-1] = x[:,:-1] - x[:,1:]

	w = np.zeros( (2,m,n),dtype=np.float64 )

	w[0] = p
	w[1] = q

	return w

def compute_linear_operator_L(el):

	p,q = el
	m,n = p.shape

	r = np.zeros( (m,n), dtype=np.float64 )

	r[1:-1,:] = p[1:-1,:] - p[:-2,:] 
	r[:,1:-1] += q[:,1:-1] - q[:,:-2]
	
	r[0,:] += p[0,:]
	r[:,0] += q[:,0]

	return r

def denoise_image(img_path,lbda,max_it,print_output=False):
	img = np.asfarray( misc.imread(img_path) )	

	img = normalize_img(img)
	img = add_noise(img,lbda/2.0)

	m,n = img.shape
	w0 = np.zeros( (2,m,n), dtype=np.float64 )
	z0 = np.zeros( (2,m,n), dtype=np.float64 )

	t0 = 1.0
	A = 1.0/(8*lbda)

	for i in range(max_it):
		L = compute_linear_operator_L( z0 ) 
		LT = compute_linear_operator_LT( project_on_C( img - lbda*L ) )
		w1 = project_on_P( z0 + A*LT ) 

		t1 = (1 + np.sqrt(1+4*t0**2) )/2.0
		z1 = w1 + (t0-1)/(t1)*(w1-w0)

		t0 = t1
		w0 = w1
		z0 = z1


	dimg = project_on_C( img - lbda*compute_linear_operator_L( w0 )	)	
	dimg = pos_processing_img(dimg)

	plt.imshow(dimg,cmap="gray")
	plt.show()	

	
if __name__=='__main__':
	img_path = 'img/lena_256.png'
	lbda = 0.12

	denoise_image(img_path,lbda,500)
