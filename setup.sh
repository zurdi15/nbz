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
JAVA=$(which java)
PIP3=$(which pip3)

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

if [ -z "${PYTHON3}" ]
then
	echo -e "${RED}NBZ - Error: Python is not installed. Please install python3 in your system.${NC}"
	exit 1
fi

if [ -z "$JAVA" ]
then
	echo -e "${RED}NBZ - Error: Java is not installed. Please install it in your system (openjdk-8-jre recommended).${NC}"
	exit 1
fi

if [ -z "${PIP3}" ]
then
	echo -e "${RED}NBZ - Error: Python3-pip is not installed. Please install it in your system.${NC}"
	exit 1
fi

# Installing libraries
if ! [ -z "${PIP3}" ]
then
	pip3 install -r requirements.txt
fi

echo
echo -e "${GREEN}  ########################## INSTALATION FINISHED NBZ ##########################${NC}"
