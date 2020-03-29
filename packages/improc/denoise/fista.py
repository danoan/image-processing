import sys,getopt,datetime

import numpy as np
from scipy import misc

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

def denoise_image(img,lbda,max_it,print_output=False):
    shape = img.shape
    nchannels = shape[2]

    w0 = np.zeros( (2,) + shape, dtype=np.float64 )
    z0 = np.zeros( (2,) + shape, dtype=np.float64 )

    w1 = np.zeros( (2,) + shape, dtype=np.float64 )
    z1 = np.zeros( (2,) + shape, dtype=np.float64 )

    t0 = 1.0
    A = 1.0/(8*lbda)

    for i in range(max_it):
        t1 = (1 + np.sqrt(1+4*t0**2) )/2.0
        for c in range(nchannels):
            L = compute_linear_operator_L( z0[:,:,:,c] )
            LT = compute_linear_operator_LT( project_on_C( img[:,:,c] - lbda*L ) )

            w1[:,:,:,c] = project_on_P( z0[:,:,:,c] + A*LT )
            z1[:,:,:,c] = w1[:,:,:,c] + (t0-1)/(t1)*(w1[:,:,:,c]-w0[:,:,:,c])

        t0 = t1
        w0 = w1
        z0 = z1

    dimg = np.zeros( shape, dtype=np.float64 )
    for c in range(nchannels):
        dimg[:,:,c] = project_on_C( img[:,:,c] - lbda*compute_linear_operator_L( w0[:,:,:,c] )	)

    return dimg

