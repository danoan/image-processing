#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )

HEAT_APP="${PROJECT_PATH}/packages/improc/utils/heat_equation.py"
DENOISE_APP="${PROJECT_PATH}/denoise.py"
GRAPH_IMG_LINE_APP="${PROJECT_PATH}/packages/improc/utils/graph_img_line.py"
INPUT_IMAGE="${PROJECT_PATH}/input/img/gradual-tiny.png"

tolerance="500 10 1.0 0.5 0.1 0.01 0.001 0.0001 0.00005" 

OUTPUT_FOLDER="${SCRIPT_PATH}/output"
for tol in $tolerance
do
	python3 ${HEAT_APP} ${INPUT_IMAGE} -i-1 -l1 -t$tol -o${OUTPUT_FOLDER}/tikhonov/tikhonov_$tol.png && python3 $GRAPH_IMG_LINE_APP ${OUTPUT_FOLDER}/tikhonov/tikhonov_$tol.png ${OUTPUT_FOLDER}/tikhonov/graph/tikhonov_$tol.png &

	python3 ${DENOISE_APP} ${INPUT_IMAGE} rof_curvature -i-1 -l0 -t$tol -o${OUTPUT_FOLDER}/rof_curvature/rof_$tol.png -v  && python3 ${GRAPH_IMG_LINE_APP} ${OUTPUT_FOLDER}/rof_curvature/rof_$tol.png ${OUTPUT_FOLDER}/rof_curvature/graph/rof_$tol.png &

	python3 ${PROJECT_PATH}/denoise.py ${INPUT_IMAGE} rof -i-1 -l0 -t$tol -o${OUTPUT_FOLDER}/rof/rof_$tol.png  && python3 ${GRAPH_IMG_LINE_APP} ${OUTPUT_FOLDER}/rof/rof_$tol.png ${OUTPUT_FOLDER}/rof/graph/rof_$tol.png
done

