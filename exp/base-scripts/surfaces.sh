#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$( cd $SCRIPT_PATH && cd ../../ && pwd)

INPUT_FOLDER=$1
OUTPUT_FOLDER=$2
FILETYPE=$3

mkdir -p $OUTPUT_FOLDER

for img in $(cd $INPUT_FOLDER && ls *.${FILETYPE})
do
	echo "$img"
	imgname=$( basename $img )
	python3 ${PROJECT_PATH}/packages/improc/utils/graph_img_plot.py $INPUT_FOLDER/$img ${OUTPUT_FOLDER}/$imgname
done



