#!/bin/bash

runningPID=$(ps -ef | grep openconnect | grep -v grep | awk '{print $2}');
if [ "$runningPID" == "" ]; then
   echo 'pnq1o17q' | sudo openconnect -u -c -b --background --servercert pin-sha256:BmrY  --passwd-on-stdin --user=pereirlo https://vpn.informatik.uni-stuttgart.de
   sleep 5
   python3 /home/pi/reconfigureDevice.py
fi
sleep 30
