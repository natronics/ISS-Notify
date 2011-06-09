#!/bin/sh

rm -f /usr/local/bin/ISS-notify-applet.py
rm -f /usr/share/pixmaps/iss_blank.png
rm -f /usr/share/pixmaps/iss_pass.png
rm -f /usr/lib/bonobo/servers/GNOME_ISS_notify.server

killall gnome-panel
