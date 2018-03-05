#!/bin/bash
#
# Author: <Zurdi>

# Navigation Bot uninstaller

sudo pip uninstall selenium
sudo pip uninstall ply
sudo pip uninstall browsermob-proxy

sudo rm /usr/bin/geckodriver
sudo rm /usr/bin/chromedriver

rm ~/.local/share/applications/navigation-bot.desktop

echo -e "\n\e[92mNavigation Bot succesfully uninstalled!!\e[0m\n"
