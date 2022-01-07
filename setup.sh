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
YELLOW="\e[93m"
NC="\e[0m"

sudo apt install toilet -y &> /dev/null
sudo apt install xvfb -y &> /dev/null
toilet -t -f mono12 -F gay "  NBZ  "

echo -e "${GREEN}########################## INSTALLING NBZ ##########################${NC}"
echo

if [ -z "${PYTHON3}" ]
then
	echo -e "${YELLOW}Python3 is not installed in your system. Do you want to install it?${NC}"
	read -p "(Y/N) " response
	if [ $response == 'Y' ] || [ $response == 'y' ]; then
		echo -e "${GREEN}Installing python3${NC}"
		sudo apt install python3 -y
	else
		echo -e "${RED}Exiting installer${NC}"
	fi
fi

sudo apt install python3-pip -y
echo -e "Installing python3 library requeriments"
sudo pip3 install -r requirements.txt

if [ -z "$JAVA" ]
then
	echo -e "${YELLOW}Java is not installed in your system. Do you want to install it?${NC}"
	read -p "(Y/N) " response
	if [ $response == 'Y' ] || [ $response == 'y' ]; then
		echo -e "${GREEN}Installing openjdk-11-jre${NC}"
		sudo apt install openjdk-11-jre -y
	else
		echo -e "${RED}Exiting installer${NC}"
	fi
fi

if [ ! -d ~/bin ];then
	mkdir ~/bin
fi
ln -s $NBZ_PATH/nbz.sh ~/bin/nbz
PATH="$HOME/bin:$PATH"

echo -e "\n${GREEN}########################## INSTALATION FINISHED NBZ ##########################${NC}"

exit 0
