#!/bin/bash
#
# Author: <Zurdi>

# Navigation Bot  

# Parameters:
#  - $script: script file 
#  - $mode: execute/compile mode
#  - $debug: disable/enable debug
######

# Structure:
#  - Parameters
#  - Remove trash files and Kill processes functions
#  - Initialize virtual display
#  - Launch navigation bot
######


function show_help {
	echo "Navigation bot v1.0 - (C) 2017-2018 Zurdi Zurdo"
	echo "Released under the GNU GLP"
	echo ""
	echo "Navigation bot is a tool to automate navigation and data extraction on the internet."
	echo "It is configured by little scripts coded with nbz-script language. You can find the"
	echo "documentation in the github wiki: https://www.github.com/zurdi15/navigation_bot/wiki"
	echo ""
	echo "Options:"
	echo " -s    set the .nbz script"
	echo " -m    set the compilation/execution mode; cx is set by default"
	echo "         c: compile only"
	echo "         x: execute only"
	echo "         cx: compile and execute only"
	echo " -d    enable debug mode; it is disabled by default"
}


#  - Parameters

script=""
mode="cx"
debug="false"

if [ $# = 0 ]
then
	show_help
	exit 0
else
	while getopts ":s:m:hd" opt
	do
		case $opt in
			h)
				show_help
				exit 0			
				;;
			s)
				ext="${OPTARG##*.}"
				if [ $ext = "nbz" ]
				then
					script=$OPTARG >&2
				else
					echo "Error: Not compatible script (.${ext}). Extension must be .nbz"
					exit 1
				fi
				;;
			m)
				mode=$OPTARG >&2
				;;
			d)
				debug="true" >&2
				;;
			\?)
				echo "Error: invalid option -$OPTARG" >&2
				exit 1
				;;
			:)
				echo "Error: option -$OPTARG requires an argument" >&2
				exit 1
				;;
		esac
	done
fi

if [ -z $script ]
then
	echo "Error: Script required."
	exit 1
else
	if [ ! -f $script ]
	then
		echo -e "Error: script \"${script}\" does not exist."
		exit 1
	fi
fi

NB_PATH=$(dirname $0)

YELLOW='\e[33m'
RED='\e[31m'
NC='\e[0m'

#  - Remove trash files and Kill processes functions
function remove_trash {	
	if [ -f $(pwd)/server.log ]
	then
		rm $(pwd)/server.log
	fi
	if [ -f $(pwd)/bmp.log ]
	then
		rm $(pwd)/bmp.log
	fi
	if [ -f $(pwd)/geckodriver.log ]
	then
		rm $(pwd)/geckodriver.log
	fi
}

function kill_processes {
	pidsProcess=$(pstree $$ -p|egrep -o '[0-9]+')
	for pid in ${pidsProcess}
	do
		kill -15 -${pid}
	done
}

#  - Initialize virtual display
# If you do not have desktop enviroment, you should use this:
#Xvfb :99 -ac 1>/dev/null 2>&1 &
#export DISPLAY=:99

#  - Launch navigation bot
echo
echo -e "${YELLOW}########################## STARTING NAVIGATION BOT ##########################${NC}"
echo

python ${NB_PATH}/navigation_bot.py -script ${script} -mode ${mode} -debug ${debug}

if [[ $? != 0 ]]; then
    echo
	echo -e "${RED}************************ ERROR ENDING NAVIGATION BOT ************************${NC}"
	remove_trash
	kill_processes
        exit 1
fi

remove_trash
echo
echo -e "${YELLOW}############################# END NAVIGATION BOT ############################${NC}"
kill_processes


exit 0
