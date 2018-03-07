#!/bin/bash
#
# Author: <Zurdi>

# NBZ uninstaller

RED="\e[91"
BLUE="\e[36m"
GREEN="\e[92m"
NC="\e[0m"

echo -e "${BLUE}Uninstalling dependencies...${NC}"
sudo -H pip uninstall -y selenium
sudo -H pip uninstall -y ply
sudo -H pip uninstall -y browsermob-proxy

echo -e "${BLUE}Uninstalling drivers...${NC}"
sudo rm /usr/bin/geckodriver
echo "Geckodriver removed!"
sudo rm /usr/bin/chromedriver
echo "Chromedriver removed!"

rm ~/.local/share/applications/nbz.desktop
echo "Menu entry removed!"

echo -e "\n${GREEN}NBZ succesfully uninstalled!!${NC}\n"
