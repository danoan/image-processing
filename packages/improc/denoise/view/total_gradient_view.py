import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.util import random_noise
from utils import finite_differences as U

class TotalGradient:
    def __init__(self,img):
        self.shape = img.shape
        self.nchannels = img.shape[2]

        self.gradX = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )
        self.gradY = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )

        self.grad2X = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )
        self.grad2Y = np.zeros( (img.shape[0],img.shape[1],self.nchannels ) )

        for c in range(self.nchannels):
            fd = U.forward_differences(img[:,:,c])
            self.gradX[:,:,c] += fd[0] #dx
            self.gradY[:,:,c] += fd[1] #dy

            fd2 = U.forward_differences_second(img[:,:,c])
            self.grad2X[:,:,c] += fd2[0] #dx
            self.grad2Y[:,:,c] += fd2[1] #dy


    def norm(self):
        rows,cols,channels = self.shape

        n=np.zeros( (rows,cols) )
        for c in range(self.nchannels):
            n+=self.gradX[:,:,c]**2 + self.gradY[:,:,c]**2

        return n


img=data.astronaut()
fimg = np.asarray(img,float)
fimg/=255

sigma = 0.155
noisy=fimg.copy()
for c in range(fimg.shape[2]):
    noisy[:,:,c] = random_noise(fimg[:,:,c], var=sigma**2)

TG=TotalGradient(fimg)
TGn=TotalGradient(noisy)

fig,axs = plt.subplots(2,2)
axO,axTG = axs[0,:]
axN,axTGN = axs[1,:]

axTG.invert_yaxis()
axTGN.invert_yaxis()

axO.imshow(fimg)
axN.imshow(noisy)

pcmO = axTG.pcolormesh( TG.norm(),cmap='RdBu_r')
fig.colorbar(pcmO,ax=axTG)

pcmN = axTGN.pcolormesh( TGn.norm(),cmap='RdBu_r')
fig.colorbar(pcmN,ax=axTG)


plt.show()




