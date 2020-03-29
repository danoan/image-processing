import numpy as np
from scipy import misc

def forward_differences(u):
    '''
        u: Image matrix of dimensions (y,x)
        returns matrix fu of dimensions (2,y,x)
    '''
    fu = np.zeros( [2] + list(u.shape) )

    fu[0,:-1,:] = u[1:,:] - u[:-1,:]	#y differences (rows-1,cols)
    fu[1,:,:-1] = u[:,1:] - u[:,:-1]	#x differences (rows,cols-1)

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

def forward_differences_second(u):
    fu = np.zeros( [2] + list(u.shape) )

    fu[0,1:-1,:] = u[0:-2,:] - 2*u[1:-1,:] + u[2:,:]	#y differences
    fu[1,:,1:-1] = u[:,0:-2] - 2*u[:,1:-1] + u[:,2:]	#x differences

    return fu
