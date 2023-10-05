#!/bin/bash

cd /home/zerobits01/time-clone;

if [ $? ]
then
	do_changes=1; echo date; date > /tmp/update_changes.log; [[ $(cd /home/zerobits01/time-clone; git pull)=="Already up to date." ]] || do_changes=0 
        [[ $do_changes -eq 0 ]] && echo install; npm install >> /tmp/update_changes.log && echo build; npm run build >> /tmp/update_changes.log && echo restart; sudo systemctl restart kit365.service >> /tmp/update_changes.log
	echo `date` site update do_changes is $do_changes >> /tmp/update.log
        if [ $? ]
        then
                exit 0
        else
                exit 1
        fi
fi
