#!/usr/bin/env bash
#
# Author: <Zurdi>

# NBZ Launcher

# Parameters:
#  - $script: script file
#  - $debug: disable/enable debug mode
#  - $screen: disable/enable screen emulation
######

# Structure:
#  - Parameters
#  - Initialize virtual display (optional)
#  - Launch NBZ
######


function show_help {
	echo "NBZ-1 v1.0.1 - (C) 2017-2018 Zurdi Zurdo"
	echo "Released under the GNU GLP"
	echo ""
	echo "NBZ is a tool to automate navigation and data extraction on the internet."
	echo "It is configured by little scripts coded with nbz-script language. You can find the"
	echo "documentation in the github wiki: https://github.com/zurdi15/NBZ-1/wiki"
	echo ""
	echo "-h    Show this help"
	echo "-v    Show the version"
	echo "-s    Set the .nbz script"
	echo "-x    Enable screen emulation (server) / hide browser screen (desktop)"
	echo "-d    Enable debug mode"
}

function show_version {
	echo "NBZ-1 v1.0.1"
}

#  - Parameters

script=""
debug="false"
display="false"

if [ ${#} = 0 ]; then
	show_help
	exit 0
else
	while getopts ":s:hvxd" opt
	do
		case ${opt} in
			h)
				show_help
				exit 0
				;;
			v)
				show_version
				exit 0
				;;
			s)
				ext="${OPTARG##*.}"
				if [ ${ext} = "nbz" ]
				then
					script=${OPTARG} >&2
				else
					echo "Error: Not compatible script (.${ext}). Extension must be .nbz"
					exit 1
				fi
				;;
			d)
				debug="true" >&2
				;;
			x)
				display="true" >&2
				;;
			\?)
				echo "Error: invalid option -${OPTARG}" >&2
				exit 1
				;;
			:)
				echo "Error: option -${OPTARG} requires an argument" >&2
				exit 1
				;;
		esac
	done
fi

if [ -z ${script} ]; then
	echo "Error: Script required."
	exit 1
else
	if [ ! -f ${script} ]; then
		echo -e "Error: script \"${script}\" does not exist."
		exit 1
	fi
fi

NBZ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON3=$(which python3)
PYTHON=$(which python)
YELLOW='\e[33m'
RED='\e[31m'
NC='\e[0m'
if [ -z "${PYTHON3}" ] && [ -z "${PYTHON}" ]; then
	echo -e "${RED}NBZ - Error: Python is not installed. Please install python 3.6.5 in your system.${NC}"
	exit 1
fi

#  - Launch NBZ
clear
TOILET=$(which toilet)
if [ -z "${TOILET}" ]; then
	header=""
else
	header=$(toilet -t -f mono12 -F gay "  NBZ  ")
fi

echo -e "${header}"

if [ -z "${PYTHON3}" ]; then
	python -W ignore ${NBZ_PATH}/nbz_interface.py -script ${script} -debug ${debug} -display ${display}
else
	python -W ignore ${NBZ_PATH}/nbz_interface.py -script ${script} -debug ${debug} -display ${display}
fi
