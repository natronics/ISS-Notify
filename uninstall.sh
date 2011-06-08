#!/bin/sh

rm /usr/local/bin/ISS-notify-applet.py
rm /usr/share/pixmaps/iss_blank.png
rm /usr/share/pixmaps/iss_pass.png
rm /usr/lib/bonobo/servers/GNOME_ISS_notify.server

killall gnome-panel
