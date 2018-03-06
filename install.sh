#!/bin/bash
#
# Author: <Zurdi>

# Navigation Bot installer

# To let the NB work, it is necesary to install three python libraries:
#	- selenium
#	- browsermob-proxy
# 	- ply
#
# Also we need to install some web browser drivers in /opt/navigation_bot:
# 	- chromedriver (Google Chrome / Chromium)
#	- geckodriver (Firefox)


PYTHON=$(which python)
JAVA=$(which java)
PIP=$(which pip)
NB_INST_PATH="/opt/navigation_bot"
NB_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRIVERS_PATH=${NB_PATH}/lib/drivers
RED="\e[91"
BLUE="\e[36m"
GREEN="\e[92m"
NC="\e[0m"

if [ -z "$PYTHON" ]
then
	echo -e "${RED}Navigation Bot - Error: Python is not installed. Please install python 2.7 in your system.${NC}"
	echo -e "${RED}Navigation Bot - Error: (sudo apt install python2.7)${NC}"
	exit 1
fi

if [ -z "$JAVA" ]
then
	echo -e "${RED}Navigation Bot - Error: Java is not installed. Please install it in your system.${NC}"
	echo -e "${RED}Navigation Bot - Error: (sudo apt install openjdk-9-jdk)${NC}"
	exit 1
fi

if [ -z "$PIP" ]
then
	echo -e "${RED}Navigation Bot - Error: Python-pip is not installed. Please install it in your system.${NC}"
	echo -e "${RED}Navigation Bot - Error: (sudo apt install python-pip)${NC}"
	exit 1
fi

if [ ! -d $NB_INST_PATH ]
then
	sudo mkdir $NB_INST_PATH
fi


for element in $(ls ${NB_PATH})
do
	sudo cp -r $element $NB_INST_PATH 
done

sudo chown -R $(whoami):$(whoami) $NB_INST_PATH

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
menu_entry="[Desktop Entry]\nVersion=1.0\nType=Application\nName=Navigation Bot\nGenericName=navigation_bot\nIcon=${NB_INST_PATH}/nb_icon.png\nExec=${NB_INST_PATH}/navigation_bot_launcher.sh -s ${NB_INST_PATH}/scripts/bdfutbol.nbz\nPath=${NB_INST_PATH}\nNoDisplay=False\nCategories=Development;\nStartupNotify=false\nTerminal=true"

echo -e $menu_entry > ~/.local/share/applications/navigation-bot.desktop

echo "Menu entry created!"

echo -e "\n${GREEN}Navigation Bot installed succesfully!!${NC}\n"
