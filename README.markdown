This is an old software project that puts an icon on certain linux desktops.

**Looking for the light-up hardware project? See:**

# <https://github.com/open-notify>



### Python Gnome-Panel Applet for International Space Station Passes

This is a quick and dirty python app that runs in the Gnome panel and acts as an alarm for when the [Internations Space Station](http://en.wikipedia.org/wiki/International_Space_Station) is overhead.

When loaded it downloads a list of upcoming passes from [heavens-above.com](http://heavens-above.com).  It then goes to sleep and the next time the ISS is overhead it turns red and, optionally, lights LED's on an ardruino.


### To install:

Make sure you have the right packages installed

    $ sudo apt-get install python python-gnomeapplet python-serial

Then install it

    $ sudo ./install.sh

After the gnome pannel restarts right click and choose "add to panel". ISS-Notify should appear in the list.

### To update:

Get the latest code (`git pull`) then remove the applet from your panel if it's running and try

    $ sudo ./uninstall.sh
    $ sudo ./install.sh

### To uninstall:

    $ sudo ./uninstall.sh

### To test:

    $ ./ISS-notify-applet.py -debug
 
This will run the applet in it's own window and you can see print statements in the terminal you called if from. Great for debuging.  

### Setting your location:

Find this line in ISS-notify-applet.py

    class PyApplet():
      ha = HeavensAbove(45.47361, -122.64931, 100, "PST")

and change the latitude and longitude to your location.

    ha = HeavensAbove(latitude, longitude, altitude, timezone)

### Connection to notification lamp

See the circuit diagram and firmware in the arduino folder. You might have to set some udev rules to get a predictable name for the python app.

Find this line in ISS-notify-applet.py

    class lamp():
      device = '/dev/ttyACM0'

Make `/dev/ttyACM0` the right thing (`dmesg | tail` is often useful). Example of the udev rule that worked for me

    SUBSYSTEMS=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789]?", MODE:="0666"
    KERNEL=="ttyACM*", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789]?", SYMLINK+="ttyUSB00%n", MODE:="0666", ENV{ID_MM_DEVICE_IGNORE}="1"

### License

&copy; 2011 [Nathan Bergey](http://twitter.com/natronics)

This program is free software; you can redistribute it and/ormodify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details at <http://www.gnu.org/copyleft/gpl.html>

