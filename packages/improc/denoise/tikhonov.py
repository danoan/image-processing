import numpy as np
from scipy import optimize
from scipy import misc

from improc.utils import finite_differences as FD

class TotalGradient:
    def __init__(self,img):
        self.shape = img.shape
        self.nchannels = img.shape[2]

        self.gradX = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )
        self.gradY = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )

        self.grad2X = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )
        self.grad2Y = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )

        for c in range(self.nchannels):
            fd = FD.forward_differences(img[:,:,c])
            self.gradX[:,:,c] += fd[0] #dx
            self.gradY[:,:,c] += fd[1] #dy

            fd2 = FD.forward_differences_second(img[:,:,c])
            self.grad2X[:,:,c] += fd2[0] #dx
            self.grad2Y[:,:,c] += fd2[1] #dy


    def norm(self):
        rows,cols,channels = self.shape

        n=np.zeros( (rows,cols) )
        for c in range(self.nchannels):
            n+=self.gradX[:,:,c]**2 + self.gradY[:,:,c]**2

        return n

class Tikhonov:
    def __init__(self,img,lbda):
        self.fimg = img
        self.lbda = lbda

        self.my_shape=self.fimg.shape
        self.my_size=self.fimg.size

    def fn_jac(self,x):
        _x = x.reshape( self.my_shape )
        TG=TotalGradient(_x)

        S= self.lbda*(TG.grad2X + TG.grad2Y)

        return ( _x - self.fimg -S ).reshape( self.my_size, )

    def tikhonov(self,x):
        _x = x.reshape( self.my_shape )
        TG=TotalGradient(_x)

        v= 0.5*( np.linalg.norm(_x - self.fimg)**2 + self.lbda*np.sum(TG.norm()) )
        return v


def denoise_image(input_image,lbda,max_it,print_output=False):
    if print_output:
        print("Executing Tikhonov...")

    T=Tikhonov(input_image,lbda)
    solution=optimize.minimize(lambda x: T.tikhonov(x),np.zeros(T.fimg.size,),jac=lambda x: T.fn_jac(x),method="CG",options={"maxiter":max_it,"disp":print_output})

    x = solution["x"].reshape( T.my_shape )
    return x