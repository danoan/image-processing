#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )
EXP_PATH=${PROJECT_PATH}/exp
BASE_SCRIPTS_FOLDER="${EXP_PATH}/base-scripts"

FOLDERS="curvature heat tv"

BASE_INPUT_FOLDER="${SCRIPT_PATH}/output/levels"
OUTPUT_FOLDER="${SCRIPT_PATH}/output/surfaces"
FILETYPE="jpg"

for folder in $FOLDERS
do
	mkdir -p ${BASE_INPUT_FOLDER}/$folder/stars-mini.png
	cp ${PROJECT_PATH}/input/img/stars-mini.png ${BASE_INPUT_FOLDER}/$folder/stars-mini.png/stars-mini.png_0.jpg
	${BASE_SCRIPTS_FOLDER}/surfaces.sh "${BASE_INPUT_FOLDER}/$folder/stars-mini.png" "${OUTPUT_FOLDER}/$folder/stars-mini.png" "$FILETYPE"
done



