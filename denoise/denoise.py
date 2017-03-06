import os,sys,getopt

import matplotlib.pyplot as plt
from TerminalColors import *
import rof,chambolle

def help():
	cprint("\ndenoise.py ", UNDERLINE, "INPUT_IMG", RESET, " ", UNDERLINE, "OUTPUT_IMG", RESET, "   -a <algorithm> -l <lambda> -e <errorTolerance> -i <maxIt>.")
	cprint("\nDenoises ", UNDERLINE, "INPUT_IMG", RESET, " and saves the denoised version at ", UNDERLINE, "OUTPUT_IMG",RESET,"." )
	cprint("\n\n-a,  algorithm to be used (chambolle,rof)\n-l,  smoothness intensity (1.0)\n-e,  error tolerance (1e-4)\n-i, maximum number of iterations (200)")

def main(argv):
	lbda = 1.0
	error_tol=1e-4
	max_it=200	
	max_alpha_it=20	
	
	input_img=False
	output_img=False

	try:
		input_img,output_img = argv[0:2]
		argv = argv[2:]
		opts,args = getopt.getopt(argv,"h:a:l:e:i:",["algorithm=","lambda=","errorTol=","maxIt="])		
	except:
		cprint(RED,"Bad arguments")
		help()		
		sys.exit(2)
	for opt,arg in opts:
		if opt =='-h':
			help()
			sys.exit()
		elif opt in("-a","--algorithm"):
			alg = str(arg)
		elif opt in ("-l","--lambda"):
			lbda = float(arg)
		elif opt in ("-e","--errorTolerance"):
			error_tol = float(arg)			
		elif opt in ("-i","--maxIt"):
			max_it = float(arg)	


	if alg=="chambolle":
		dimg = chambolle.denoise_image(input_img,lbda,error_tol,max_it)	
	elif alg=="rof":
		dimg = rof.denoise_image(input_img,lbda,error_tol,max_it,max_alpha_it)	

	plt.imshow(dimg,cmap="gray")
	if not os.path.exists(output_img):
		os.makedirs(os.path.dirname(output_img))
	plt.savefig(output_img)			

	

if __name__=="__main__":
	main(sys.argv[1:])