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
	echo -e "${RED}NBZ - Error: Python3 is not installed in your system. Do you want to install it?${NC}"
	read -p "(Y/N) " response
	if [ $response == 'Y' ] || [ $response == 'y' ]; then
		echo -e "${GREEN} NBZ - Log: Installing python3{NC}"
		sudo apt-get install python3 -y
	else
		echo -e "${RED} NBZ - Log: Exiting installer${NC}"
	fi
fi

sudo apt-get install python3-pip -y
echo -e "${GREEN} NBZ - Log: Installing python3 library requeriments{NC}"
sudo pip3 install -r requirements.txt

if [ -z "$JAVA" ]
then
	echo -e "${RED}NBZ - Error: Java is not installed in your system. Do you want to install it?${NC}"
	read -p "(Y/N) " response
	if [ $response == 'Y' ] || [ $response == 'y' ]; then
		echo -e "${GREEN} NBZ - Log: Installing openjdk-11-jre${NC}"
		sudo apt-get install openjdk-11-jre -y
	else
		echo -e "${RED} NBZ - Log: Exiting installer${NC}"
	fi
fi

echo -e "\n${GREEN}  ########################## INSTALATION FINISHED NBZ ##########################${NC}"

exit 0
