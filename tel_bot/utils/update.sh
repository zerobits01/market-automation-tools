#!/bin/bash

cd /home/zerobits01/time-clone;

if [ $? ]
then
        git pull && npm install && sudo systemctl restart batime.service
        if [ $? ]
        then
                exit 0
        else
                exit 1
        fi
fi