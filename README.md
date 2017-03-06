Implementation of classical algorithms on image processing.

# Denoise Package:
* rof.py:	ROF model implementation for image denoising.
* chambolle.py: Chambolle's algorithm implementation for image denoising.
* denoise.py: Denoise image tool.

	denoise.py INPUT_IMG OUTPUT_IMG -a [algorithm] -l [lambda] -i [maxIt] -e [errorTolerance]

	-a, Algorithm to be used (rof,chambolle).

	-l, Smoothness level (1.0).

	-i, Maximum number of iterations (200).

	-e, Error tolerance stop condition (1e-4). 

* experiments.py: Comparison between algorithms.

	experiments.py INPUT_IMG OUTPUT_DIR EXPERIMENT_NUMBER

# Dependencies:
1. scipy, numpy, matplotlib

# External libraries:
1. TerminalColors: https://github.com/dennishafemann/python-TerminalColors

# References
1.	Nonlinear total variation based noise removal algorithms. Rudin,Osher,Fatemi.
1.	An algorithm for total variation mimimization and applications. Chambolle.