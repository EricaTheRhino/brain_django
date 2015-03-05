#!/bin/bash
d=`dirname $0`
restart_olad(){
	sudo service olad stop
        sleep 1
        sudo service olad start
        sleep 1
}
if [ $# -ne 2 ]; then
	echo "you need to specify a theme type (horn or body) and theme name."
	exit 1
fi
echo "Setting $1 theme to $2"
if [ "$2" == "random" ]; then
	if [ "$1" == "body" ]; then
		colours=($(echo "red green blue yellow white" | tr " " "\n" | shuf | tr "\n" " "))
		for c in ${colours[@]}; do
			restart_olad
			$d/set_theme.py $1 $c
		done
	elif  [ "$1" == "horn" ]; then
		colours=($(echo "red green blue ice christmas pink aqua" | tr " " "\n" | shuf | tr "\n" " "))
		cur_theme="cat $d/tmp/horn_theme"
		for c in ${colours[@]}; do
			if [ "$c" != "$cur_theme" ]; then
				restart_olad
				$d/set_theme.py $1 $c
				break;
			fi
		done
	fi
else
	restart_olad
	$d/set_theme.py $1 $2
fi
echo "Done"
exit 0
