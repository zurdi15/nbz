#!/usr/bin/env bash
#
# Author: <Zurdi>
#
# NBZ installer
#
# Dependencies:
#   - Python:
#	    · selenium
#	    · browsermob-proxy
# 	    · ply
#       · psutil
#
#   - Bash:
#       · toilet
#       · xvfb


PYTHON=$(which python)
JAVA=$(which java)
PIP=$(which pip)

NBZ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RED="\e[91"
BLUE="\e[36m"
GREEN="\e[92m"
NC="\e[0m"

if [ -z "${PYTHON}" ]
then
    echo -e "${RED}NBZ - Error: Python is not installed. Please install python 2.7 in your system.${NC}"
    exit 1
fi

if [ -z "$JAVA" ]
then
	echo -e "${RED}NBZ - Error: Java is not installed. Please install it in your system.${NC}"
	exit 1
fi

if [ -z "${PIP}" ]
then
	echo -e "${RED}NBZ - Error: Python-pip is not installed. Please install it in your system.${NC}"
	exit 1
fi

# Installing libraries
echo -e "${BLUE}Installing dependencies...${NC}"
sudo apt-get install toilet
sudo apt-get install xvfb
sudo -H pip install ply
sudo -H pip install selenium
sudo -H pip install browsermob-proxy
sudo -H pip install psutil