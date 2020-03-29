import sys, getopt

import numpy as np
from scipy import misc

from improc.utils import finite_differences as FD

def compute_gradient(A):
    return FD.forward_differences(A)

def compute_divergence(p):
    shape = p.shape[1:]

    sum_x = np.zeros( shape )
    sum_y = np.zeros( shape )

    sum_y[1:-1] = p[0][1:-1,:] - p[0][0:-2,:]
    sum_y[0] = p[0][0]
    sum_y[-1] = -p[0][-2]

    sum_x[:,1:-1] = p[1][:,1:-1] - p[1][:,0:-2]
    sum_x[:,0] = p[1][:,0]
    sum_x[:,-1] = -p[1][:,-2]

    return sum_x + sum_y

def compute_objective_function(lbda,p,g):
    nchannels = p.shape[3]

    n=0
    for c in range(nchannels):
        n += lbda*compute_divergence(p[:,:,:,c]) - g[:,:,c]

    return np.sum(n*n)

def solve_projection(img,lbda,error_tol,max_it,print_output):
    shape = img.shape
    nchannels = shape[2]

    g = img
    p0 = np.zeros( (2,) + shape )
    it = 1
    ONE = np.ones( shape )

    t = 1/4.0

    while it < max_it:
        val_p0 = compute_objective_function(lbda,p0,g)

        div_p = np.zeros( shape )
        p = np.zeros( (2,) + shape )
        for c in range(nchannels):
            div_p[:,:,c] = compute_divergence(p0[:,:,:,c])
            f1 = compute_gradient(div_p[:,:,c] - g[:,:,c]/lbda)

            p[:,:,:,c] += ( p0[:,:,:,c] + t*(f1) ) / (ONE[:,:,c] + t*(np.sqrt(f1**2)).sum(axis=0))

        val_p = compute_objective_function(lbda,p,g)
        p0 = p

        if print_output:
            print("it: {0} ; fn: {1:.5f} ; diff: {2:.5f}".format (it,val_p,val_p-val_p0) )

        if ( np.abs( val_p-val_p0) < error_tol ):
            break
        it+=1


    return lbda*compute_divergence(p)

def denoise_image(img,lbda,error_tol,max_it,print_output=False):
    if print_output:
        print("Executiong Chambolle...")

    p = solve_projection(img,lbda,error_tol,max_it,print_output)
    denoised_img = img - p

    return denoised_img


