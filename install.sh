#!/bin/bash
#
# Author: <Zurdi>

# NBZ installer

# To let the NBZ work, it is necesary to install three python libraries:
#	- selenium
#	- browsermob-proxy
# 	- ply
#
# Also we need to install some web browser drivers in /opt/nbz:
# 	- chromedriver (Google Chrome / Chromium)
#	- geckodriver (Firefox)


PYTHON=$(which python)
JAVA=$(which java)
PIP=$(which pip)
NBZ_INST_PATH="/opt/nbz"
NBZ_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRIVERS_PATH=${NBZ_PATH}/lib/drivers
RED="\e[91"
BLUE="\e[36m"
GREEN="\e[92m"
NC="\e[0m"

if [ -z "$PYTHON" ]
then
	echo -e "${RED}NBZ - Error: Python is not installed. Please install python 2.7 in your system.${NC}"
	echo -e "${RED}NBZ - Error: (sudo apt install python2.7)${NC}"
	exit 1
fi

if [ -z "$JAVA" ]
then
	echo -e "${RED}NBZ - Error: Java is not installed. Please install it in your system.${NC}"
	echo -e "${RED}NBZ - Error: (sudo apt install openjdk-9-jdk)${NC}"
	exit 1
fi

if [ -z "$PIP" ]
then
	echo -e "${RED}NBZ - Error: Python-pip is not installed. Please install it in your system.${NC}"
	echo -e "${RED}NBZ - Error: (sudo apt install python-pip)${NC}"
	exit 1
fi

if [ ! -d $NBZ_INST_PATH ]
then
	sudo mkdir $NBZ_INST_PATH
fi


for element in $(ls ${NBZ_PATH})
do
	sudo cp -r $element $NBZ_INST_PATH 
done

sudo chown -R $(whoami):$(whoami) $NBZ_INST_PATH

# Installing libraries
echo -e "${BLUE}Installing dependencies...${NC}"
sudo -H pip install ply
sudo -H pip install selenium
sudo -H pip install browsermob-proxy

# Copying drivers into /usr/bin
echo -e "${BLUE}Installing drivers...${NC}"
sudo cp ${DRIVERS_PATH}/geckodriver /usr/bin
echo "Geckodriver installed in /usr/bin!"
sudo cp ${DRIVERS_PATH}/chromedriver /usr/bin
echo "Chromedriver installed in /usr/bin!"

# Creating menu entry
menu_entry="[Desktop Entry]\nVersion=1.0\nType=Application\nName=NBZ\nGenericName=NBZ\nIcon=${NBZ_INST_PATH}/nbz_icon.png\nExec=${NBZ_INST_PATH}/nbz_launcher.sh -s ${NBZ_INST_PATH}/scripts/bdfutbol.nbz\nPath=${NBZ_INST_PATH}\nNoDisplay=False\nCategories=Development;\nStartupNotify=false\nTerminal=true"

echo -e $menu_entry > ~/.local/share/applications/nbz.desktop

echo "Menu entry created!"

echo -e "\n${GREEN}NBZ installed succesfully!!${NC}\n"
