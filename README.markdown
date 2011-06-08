# Python Gnome-Panel Applet for the International Space Station

This is a quick and dirty python app that runs in the Gnome panel and acts as an alarm for when the Internations Space Station is overhead.

When loaded it downloads a list of upcoming passes from [heavens-above.com](http://heavens-above.com).  It then goes to sleep and the next time the ISS is overhead it turns red and, optionally, lights LED's on an ardruino.


## To install:

    $ sudo ./install.sh

## To uninstall:

    $ sudo ./uninstall.sh

## To test:

    $ ./ISS-notify-applet.py run-in-window
    
## Setting your location:

Find this line in ISS-notify-applet.py

    # Get Pass:
    ha = HeavensAbove(45.47361, -122.64931)

and change the latitude and longitude to your location.

    ha = HeavensAbove(latitude, longitude)

## Connection to notification lamp

See the circuit diagram and firmware in the arduino folder. You might have to set some udev rules to get a predictable name for the python app.

Find this line in ISS-notify-applet.py

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)

Make `/dev/ttyACM0` the right thing (`dmesg | tail` is often useful). Example of the udev rule that worked for me

    SUBSYSTEMS=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789]?", MODE:="0666"
    KERNEL=="ttyACM*", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789]?", SYMLINK+="ttyUSB00%n", MODE:="0666", ENV{ID_MM_DEVICE_IGNORE}="1"

## License

&copy; 2011 [Nathan Bergey](http://twitter.com/natronics)

This program is free software; you can redistribute it and/ormodify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details at <http://www.gnu.org/copyleft/gpl.html>
