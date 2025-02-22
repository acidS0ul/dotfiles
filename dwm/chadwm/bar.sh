#!/bin/dash

# ^c$var^ = fg color
# ^b$var^ = bg color

interval=3600

black=#222526
green=#89b482
white=#c7b89d
grey=#2b2e2f
blue=#6f8faf
red=#ec6b64
darkblue=#6080a0

cpu() {
  cpu_val=$(grep -o "^[^ ]*" /proc/loadavg)

  printf "^c$green^ ^b$black^   "
  printf "^c$green^$cpu_val%%"
}

pkg_updates() {
  #updates=$({ timeout 20 doas xbps-install -un 2>/dev/null || true; } | wc -l) # void
  updates=$({ timeout 20 checkupdates 2>/dev/null || true; } | wc -l) # arch
  # updates=$({ timeout 20 aptitude search '~U' 2>/dev/null || true; } | wc -l)  # apt (ubuntu, debian etc)

  if [ -z "$updates" ]; then
    printf "  ^c$green^    Fully Updated"
  else
    printf "  ^c$green^    $updates"" updates"
  fi
}

battery() {
  get_capacity="$(cat /sys/class/power_supply/BAT1/capacity)"
  printf "^c$blue^   $get_capacity"
}

brightness() {
  printf "^c$red^   "
  printf "^c$red^%.0f\n" $(cat /sys/class/backlight/*/brightness)
}

mem() {
  printf "^c$blue^^b$black^  "
  printf "^c$blue^ $(free -h | awk '/^Mem/ { print $3 }' | sed s/i//g)"
}

wlan() {
	case "$(cat /sys/class/net/wl*/operstate 2>/dev/null)" in
	up) printf "^c$black^ ^b$blue^ 󰤨 ^d^%s" " ^c$blue^Connected" ;;
	down) printf "^c$black^ ^b$blue^ 󰤭 ^d^%s" " ^c$blue^Disconnected" ;;
	esac
}

showip() {
    printf "^c$red^^b$black^ 󰈀 "
    printf "^c$red^$(ip addr show enp3s0 | grep -o 'inet\s.*/24' | awk '{print $2}' | cut -d'/' -f1)"
}

showusediskmem() {
    printf "^c$blue^^b$black^  "
    printf "^c$blue^%3d%%" $(df -h / | awk '{print $5}' | grep .*%)  
}

clock() {
	printf "^c$black^ ^b$darkblue^ 󱑆 "
	printf "^c$black^^b$blue^ $(date '+%H:%M')  "
}

while true; do

  [ $interval = 0 ] || [ $(($interval % 3600)) = 0 ] && updates=$(pkg_updates)
  interval=$((interval + 1))

  sleep 1 && xsetroot -name "$updates $(showusediskmem) $(showip) $(cpu) $(mem) $(clock)"
done
