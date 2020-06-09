#!/usr/bin/env bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
PROJECT_PATH=$(cd $SCRIPT_PATH && cd ../../ && pwd )
EXP_PATH=${PROJECT_PATH}/exp
BASE_SCRIPTS_FOLDER="${EXP_PATH}/base-scripts"

IMAGE="${PROJECT_PATH}/input/img/stars-mini.png"
EV_STOP_SEQUENCE="150 100 70 55 50 45 40 35 30 25 20 15"
LEVELS="70"
BASE_OUTPUT_FOLDER="${SCRIPT_PATH}/output"
FLOW="heat"


${BASE_SCRIPTS_FOLDER}/exp-levels.sh "$IMAGE" "$EV_STOP_SEQUENCE" "$LEVELS" "$BASE_OUTPUT_FOLDER" "$FLOW"
