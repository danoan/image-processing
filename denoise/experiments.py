import os,sys,getopt
import matplotlib.pyplot as plt

import rof,chambolle
from TerminalColors import *

def save_img(img,fname):
	plt.imshow(img,cmap="gray")
	plt.savefig(fname)	


def experiment_1(imgFile,outputDir):
	imgName = imgFile.split(os.path.sep)[-1].split(".")[0]

	rof_dir = os.path.join(outputDir,"rof")
	chamb_dir = os.path.join(outputDir,"chamb")
	diff_dir = os.path.join(outputDir,"diff")
	if not os.path.exists(rof_dir):
		os.makedirs(rof_dir)
	if not os.path.exists(chamb_dir):
		os.makedirs(chamb_dir)
	if not os.path.exists(diff_dir):
		os.makedirs(diff_dir)

	rof_instances = [ 	{'lbda':1,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False},
						{'lbda':0.5,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False},
						{'lbda':0.1,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False},
						{'lbda':0.05,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False},
						{'lbda':0.01,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False},
						{'lbda':0.005,'error_tol':1e-4,'max_it':1000,'max_alpha_it':20,'print_output':False}
					]	

	chamb_instances = [ {'lbda':1,'error_tol':1e-4,'max_it':1000,'print_output':False},
						{'lbda':2,'error_tol':1e-4,'max_it':1000,'print_output':False},
						{'lbda':10,'error_tol':1e-4,'max_it':1000,'print_output':False},
						{'lbda':20,'error_tol':1e-4,'max_it':1000,'print_output':False},
						{'lbda':40,'error_tol':1e-4,'max_it':1000,'print_output':False},
						{'lbda':80,'error_tol':1e-4,'max_it':1000,'print_output':False}
					  ]						

	counter = 0
	for rof_inst,chamb_inst in zip(rof_instances,chamb_instances):
		fname = os.path.join(rof_dir,"%s_%d.png" % (imgName,counter) )
		dimg_rof = rof.denoise_image(imgFile,**rof_inst)
		save_img(dimg_rof,fname)

		fname = os.path.join(chamb_dir,"%s_%d.png" % (imgName,counter) )
		dimg_chamb = chambolle.denoise_image(imgFile,**chamb_inst)
		save_img(dimg_chamb,fname)		

		fname = os.path.join(diff_dir,"%s_%d.png" % (imgName,counter) )
		diff_img = (dimg_rof - dimg_chamb)%256
		save_img(diff_img,fname)	

		counter+=1


def main(argv):
	try:
		img_file,outputDir,experiment = argv
	except:
		cprint("denoise-experiments.py ",UNDERLINE,"IMG_FILE",RESET, "   ", UNDERLINE, "OUTPUT_DIR", RESET, "   ", UNDERLINE, "EXPERIMENT_NUMBER")
		cprint("\nRuns experiment ",UNDERLINE,"EXPERIMENT_NUMBER",RESET," on file ",UNDERLINE,"IMG_FILE", RESET, " and outputs results in ",UNDERLINE,"OUTPUT_DIR")
		return

	if experiment=="1":
		experiment_1(img_file,outputDir)
	else:
		cprint(RED,"Experiment does not exist.")				

if __name__=="__main__":
	main(sys.argv[1:])