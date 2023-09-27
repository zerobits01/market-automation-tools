#!/bin/bash

cd /home/zerobits01/time-clone;

if [ $? ]
then
	[[ $(cd /home/zerobits01/time-clone; git pull)=="Already up to date." ]] || do_changes=0 
        [[ $do_changes -eq 0 ]] && npm install && npm run build && sudo systemctl restart kit365.service
	echo `date` site update do_changes is '$do_changes' > /tmp/update.log
        if [ $? ]
        then
                exit 0
        else
                exit 1
        fi
fi
