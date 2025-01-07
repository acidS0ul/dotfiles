#!/bin/bash

killall polybar

for m in $(polybar -m :| cut -d":" -f1);  do
	MONITOR=$m polybar --reload example &
done
