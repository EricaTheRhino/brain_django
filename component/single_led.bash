#!/bin/bash
led="0"
if [ $# -eq 1 ]; then
	led="$1"
fi
sudo service olad stop
sleep 1
sudo service olad start
sleep 1
echo "Turning on LED $led"
./turn_on_led.py $led &
pid=$!
echo "Turn on LED has PID $pid"
sleep 10
kill -9 $pid 
