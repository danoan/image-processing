#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )

INPUT_IMAGE="$1"
EV_STOP_SEQUENCE="$2"
LEVELS="$3"
BASE_OUTPUT_FOLDER="$4"
FLOW="$5" #heat tv curvature
LAMBDA=$6

IMAGE_NAME=$(basename $INPUT_IMAGE)
NUM_RUNS=$( wc -w <<< $EV_STOP_SEQUENCE )
NUM_RUNS=$(( $NUM_RUNS-1 ))

LEVELS_SCRIPT="${PROJECT_PATH}/packages/improc/utils/graph_img_levels.py"
FLOW_SCRIPT=""
OUTPUT_FOLDER=""
ARGS=""

if [ "$LAMBDA" == "" ]
then
	LAMBDA=0
fi
echo $LAMBDA

if [ "$FLOW" == "heat" ]
then
	FLOW_SCRIPT="${PROJECT_PATH}/packages/improc/utils/heat_equation.py"
	ARGS="-i-1 -l1 -t1e-10"
	OUTPUT_FOLDER="${BASE_OUTPUT_FOLDER}/levels/heat/$IMAGE_NAME"
elif [ "$FLOW" == "tv" ]
then
	FLOW_SCRIPT="${PROJECT_PATH}/denoise.py"
	ARGS="rof -i-1 -l$LAMBDA -t1e-10"
	OUTPUT_FOLDER="${BASE_OUTPUT_FOLDER}/levels/tv/$IMAGE_NAME"
elif [ "$FLOW" == "curvature" ]
then
	FLOW_SCRIPT="${PROJECT_PATH}/denoise.py"
	ARGS="rof_curvature -i-1 -l$LAMBDA -t1e-10"
	OUTPUT_FOLDER="${BASE_OUTPUT_FOLDER}/levels/curvature/$IMAGE_NAME"
else
	echo "Unknown flow"
	exit
fi

cn=-1
count=0
color="red"
cur_img="$INPUT_IMAGE"
for ev_stop in $EV_STOP_SEQUENCE
do
	echo "EV_STOP: $ev_stop"
	output_file="${OUTPUT_FOLDER}/$IMAGE_NAME-$count.jpg"
	python3  ${FLOW_SCRIPT} ${cur_img} $ARGS -o $output_file -e $ev_stop -v

	if [ "$count" -eq "$NUM_RUNS" ]
	then
		color="blue"

	elif [ "$cn" -eq "-1" ]	
	then
		color="red"
	
	elif [ $((cn%3)) -eq "0" ]
	then
		color="#444444"
	elif [ $((cn%3)) -eq "1" ]
	then
		color="#666666"
	elif [ $((cn%3)) -eq "2" ]
	then
		color="#888888"
	fi

	python3 $LEVELS_SCRIPT $output_file $OUTPUT_FOLDER/curves/$count.png -l $LEVELS -c $color
	cn=$((cn+1))
	count=$((count+1))
	cur_img=$output_file
done



