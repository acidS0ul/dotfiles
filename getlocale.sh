#!/bin/bash

mask=0
locale=("en" "ru" "EN" "RU")

group2=$(xset q | grep -E "Group 2:\s+\w{2,3}" | awk '{print $4}')
capslc=$(xset q | grep -E "Caps .*:\s+\w{2,3}" | awk '{print $4}')

if [[ "$group2" == "on" ]]; then
    mask=$((mask + 1))
fi

if [[ "$capslc" == "on" ]]; then
    mask=$((mask + 2))
fi


echo ${locale[mask]}
