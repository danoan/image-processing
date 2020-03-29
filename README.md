Implementation of classical algorithms on image processing.

# Denoise package:
* tikhonov.py: Tikhonov regularization.
* rof.py:	ROF model implementation for image denoising.
* chambolle.py: Chambolle's algorithm implementation for image denoising.
* fista.py: Fista algorithm implementation for image denoising.

	denoise.py INPUT_IMG ALGORITHM -l [lambda] -i [maxIt] -e [tolerance]

	-a, Algorithm to be used (tikhonov,rof,chambolle,fista).

	-l, Smoothness strength.

	-i, Maximum number of iterations.

	-e, Stop condition tolerance. 

# Inpainting package
To be done.

# Dependencies:
1. scipy, numpy, matplotlib

# External libraries:
1. TerminalColors: https://github.com/dennishafemann/python-TerminalColors

# References
1.	Nonlinear total variation based noise removal algorithms. Leonid I. Rudin; Stanley Osher; Emad Fatemi.
1.	An algorithm for total variation mimimization and applications. Antonin Chambolle.
1.	A fast iterative shrinkage-thresholding algorithm for linear inverse problems. Amir Beck; Marc Teboulle.