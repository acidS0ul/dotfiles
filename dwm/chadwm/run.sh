#!/bin/sh

flameshot &
setxkbmap -layout us,ru -option ctrl:swapcaps
setxkbmap -layout us,ru -option grp:win_space_toggle
redshift & 
xrdb merge ~/.Xresources 
xbacklight -set 10 &
feh --bg-fill ~/.wallpaper.png &
xset r rate 200 50 &
picom &

dash ~/.config/chadwm/scripts/bar.sh &
while type chadwm >/dev/null; do chadwm && continue || break; done
