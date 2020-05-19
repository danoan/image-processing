#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )
EXP_PATH=${PROJECT_PATH}/exp
BASE_SCRIPTS_FOLDER="${EXP_PATH}/base-scripts"

FOLDERS="curvature heat tv"

BASE_INPUT_FOLDER="${SCRIPT_PATH}/output/levels/with-noise/levels"
OUTPUT_FOLDER="${SCRIPT_PATH}/output/surfaces"
FILETYPE="jpg"

for folder in $FOLDERS
do
	cp ${PROJECT_PATH}/input/img/coala_noise_2.jpg ${BASE_INPUT_FOLDER}/$folder/coala_noise_2.jpg/coala_noise_2.jpg_0.jpg
	${BASE_SCRIPTS_FOLDER}/surfaces.sh "${BASE_INPUT_FOLDER}/$folder/coala_noise_2.jpg" "${OUTPUT_FOLDER}/$folder/coala_noise_2.jpg" "$FILETYPE"
done



