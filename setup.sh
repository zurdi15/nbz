#!/usr/bin/env bash
#
# Author: <Zurdi>
#
# NBZ installer
#
# Requirements:
#   - Python:
#       · selenium
#       · browsermob-proxy
#       · ply
#       · pyvirtualdisplay
#       · psutil
#
#   - Bash:
#       · toilet
#       · xvfb


PYTHON3=$(which python3)
PYTHON=$(which python)
JAVA=$(which java)
PIP3=$(which pip3)
PIP=$(which pip)

NBZ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RED="\e[91"
BLUE="\e[36m"
GREEN="\e[92m"
NC="\e[0m"

sudo apt-get install toilet -y
sudo apt-get install xvfb -y
toilet -t -f mono12 -F gay "  NBZ  "

echo -e "${GREEN}  ########################## INSTALLING NBZ ##########################${NC}"
echo

if [ -z "${PYTHON3}" ] && [ -z "${PYTHON}" ]
then
	echo -e "${RED}NBZ - Error: Python is not installed. Please install python2 or python3 in your system (python3 recommended).${NC}"
	exit 1
fi

if [ -z "$JAVA" ]
then
	echo -e "${RED}NBZ - Error: Java is not installed. Please install it in your system (openjdk-8-jre recommended).${NC}"
	exit 1
fi

if [ -z "${PIP3}" ] && [ -z "${PIP}" ]
then
	echo -e "${RED}NBZ - Error: Python-pip is not installed. Please install it in your system (python-pip for python2 or python-pip3 for python3).${NC}"
	exit 1
fi

# Installing libraries
if ! [ -z "${PIP3}" ]
then
	pip3 install -r requirements.txt
elif ! [ -z "${PIP}" ]
then
    pip install -r requirements.txt
fi

echo
echo -e "${GREEN}  ########################## INSTALATION FINISHED NBZ ##########################${NC}"
