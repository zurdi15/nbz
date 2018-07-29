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
#
#   - Bash:
#       · toilet


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
    echo -e "${RED}NBZ - Error: Python is not installed. Please install python 3.6.5 in your system.${NC}"
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
pip install -r requirements.txt