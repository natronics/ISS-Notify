#!/bin/sh

chmod +x ISS-notify-applet.py

cp ISS-notify-applet.py     /usr/local/bin/
cp pixmaps/*.png            /usr/share/pixmaps/
cp GNOME_ISS_notify.server  /usr/lib/bonobo/servers/


killall gnome-panel
