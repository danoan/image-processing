#!/usr/bin/env bash


SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )

DENOISE_APP="${PROJECT_PATH}/denoise.py"
INPUT_IMAGE="${PROJECT_PATH}/input/img/coala_noise_2.jpg"
OUTPUT_FOLDER="${SCRIPT_PATH}/output/denoise-2"

echo "Executing Tikhonov"
python3 ${DENOISE_APP} ${INPUT_IMAGE} tikhonov -i300 -l10 -o ${OUTPUT_FOLDER}/coala-tikhonov.jpg

echo "Executing ROF"
python3 ${DENOISE_APP} ${INPUT_IMAGE} rof -i-1 -t0.01 -l8.0 -o ${OUTPUT_FOLDER}/coala-rof.jpg -v

echo "Executing Chambolle"
python3 ${DENOISE_APP} ${INPUT_IMAGE} chambolle -i-1 -t0.01 -l0.2 -o ${OUTPUT_FOLDER}/coala-chambolle.jpg -v

echo "Executing Fista"
python3 ${DENOISE_APP} ${INPUT_IMAGE} fista -i540 -l0.25 -o ${OUTPUT_FOLDER}/coala-fista.jpg -v

echo "Executing ROF_curvature"
python3 ${DENOISE_APP} ${INPUT_IMAGE} rof_curvature -i-1 -t0.001 -l0.1 -o ${OUTPUT_FOLDER}/coala-rof-curvature-01.jpg -v

