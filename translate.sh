#!/bin/bash

source scripts/utils.sh

function makemessages {
    if [ -d "$1" ]; then
        cd "$1"
        mkdir -p locale/es

        django-admin makemessages --add-location file -l es -e pug,html,txt,py
        django-admin makemessages --add-location file -d djangojs -l es -e js,jsx,ts,tsx

        cd ..
    else
        color_print $red "folder \"$1\" does not exist"
    fi
}

function translate {
    color_print $green "translating \"$1\""
    if $COMPILE ; then
        cd "$1"
        django-admin compilemessages
        cd ..
    else
        makemessages "$1"
    fi
}

COMPILE=false

while getopts "c" OPTION
do
    case $OPTION in
        c)
            color_print $blue "Compiling"
            COMPILE=true
             ;;
        ?)
             echo "fail"
             exit
             ;;
     esac
done

if [ $1 ] && [ $1 != '-c' ] ; then
    color_print $blue "Only on app \"$1\""
    translate $1
elif [ $2 ] && [ $2 != '-c' ] ; then
    color_print $blue "Only on app \"$2\""
    translate $2
else
    translate "base"
fi
