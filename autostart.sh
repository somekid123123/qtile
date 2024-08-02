#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

feh --bg-fill ~/Pictures/wallpapers/minimal-backgrounds/buildings.jpg &
nm-applet &
xfce4-power-manager &
picom --config ~/.config/qtile/picom.conf &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
