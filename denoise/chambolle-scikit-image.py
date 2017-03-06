# chambolle.py - As it is in scikit-image

from __future__ import division

import numpy as np
import scipy as sp

def denoise_tv_chambolle(im, weight=0.1, eps=2.e-4, n_iter_max=200,
                         multichannel=False):
    im_type = im.dtype
    if not im_type.kind == 'f':
        im = img_as_float(im)
    if multichannel:
        out = np.zeros_like(im)
        for c in range(im.shape[-1]):
            out[..., c] = _denoise_tv_chambolle_nd(im[..., c], weight, eps,
                                                   n_iter_max)
    else:
        out = _denoise_tv_chambolle_nd(im, weight, eps, n_iter_max)
    return out

def _denoise_tv_chambolle_nd(im, weight=0.1, eps=2.e-4, n_iter_max=200):
    ndim = im.ndim
    p = np.zeros((im.ndim, ) + im.shape, dtype=im.dtype)
    g = np.zeros_like(p)
    d = np.zeros_like(im)
    i = 0
    while i < n_iter_max:
        if i > 0:
            # d will be the (negative) divergence of p
            d = -p.sum(0)
            slices_d = [slice(None), ] * ndim
            slices_p = [slice(None), ] * (ndim + 1)
            for ax in range(ndim):
                slices_d[ax] = slice(1, None)
                slices_p[ax+1] = slice(0, -1)
                slices_p[0] = ax
                d[slices_d] += p[slices_p]
                slices_d[ax] = slice(None)
                slices_p[ax+1] = slice(None)
            out = im + d
        else:
            out = im
        E = (d ** 2).sum()
        # g stores the gradients of out along each axis
        # e.g. g[0] is the first order finite difference along axis 0
        slices_g = [slice(None), ] * (ndim + 1)
        for ax in range(ndim):
            slices_g[ax+1] = slice(0, -1)
            slices_g[0] = ax
            g[slices_g] = np.diff(out, axis=ax)
            slices_g[ax+1] = slice(None)
        norm = np.sqrt((g ** 2).sum(axis=0))[np.newaxis, ...]
        E += weight * norm.sum()
        tau = 1. / (2.*ndim)
        norm *= tau / weight
        norm += 1.
        p -= tau * g
        p /= norm
        E /= float(im.size)
        if i == 0:
            E_init = E
            E_previous = E
        else:
            if np.abs(E_previous - E) < eps * E_init:
                break
            else:
                E_previous = E
        i += 1
    print(i)
    return out