#!/bin/bash
res=$(xset -q | sed -rn 's/.*LED mask.*(.)[[:xdigit:]]{3}$/\1/p' | awk '{if ($1 == 0) print "en"; else print "ru";}')
echo "$res"
