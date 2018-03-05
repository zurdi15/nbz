#!/bin/bash
#
# Author: <Zurdi>

# Navigation Bot uninstaller

echo -e "\e[36mUninstalling dependencies...\e[0m"
sudo -H pip uninstall -y selenium
sudo -H pip uninstall -y ply
sudo -H pip uninstall -y browsermob-proxy

echo -e "\e[36mUninstalling drivers...\e[0m"
sudo rm /usr/bin/geckodriver
echo "Geckodriver removed!"
sudo rm /usr/bin/chromedriver
echo "Chromedriver removed!"

rm ~/.local/share/applications/navigation-bot.desktop
echo "Menu entry removed!"

echo -e "\n\e[92mNavigation Bot succesfully uninstalled!!\e[0m\n"
