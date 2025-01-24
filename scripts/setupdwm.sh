#!/bin/sh

slstatus  &
redshift  &
flameshot &

while true; do
	dwm 2> ~/.dwm.log
done
