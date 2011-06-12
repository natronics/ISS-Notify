#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import sys
import gtk, gtk.gdk, gobject
import gnomeapplet
import datetime
import urllib2
import signal
import serial

class lamp():
  """Allows the use of a serial connected lamp as the alarm"""
  
  # Set this to the right name...some testing might be required
  device = '/dev/ttyACM0'
  
  def write_to_device(self, c):
    """Writes a characer out via serial"""
    try:
      ser = serial.Serial(self.device, 9600, timeout=0.5)
      ser.write(c)
      ser.close()
    except:
      print "ISS-Notify: Failed to find lamp, continuing happily"
      pass
  
  def lights_on(self):
    """Send the signal to turn on the lights"""
    self.write_to_device('1')
      
  def lights_off(self):
    """Send the signal to turn off the lights"""
    self.write_to_device('0')

class HeavensAbove:
  """Scrapes data about the ISS from http://heavens-above.com"""
  
  lat = 0
  lon = 0
  alt = 0
  tz  = "GMT"
  
  # These defaults are useful for debuging if you're impatient
  next_pass             = datetime.datetime.today() + datetime.timedelta(0,5)
  seconds_to_next_pass  = 5
  pass_length           = 7

  def __init__(self, lat, lon, alt, tz):
    """Set the postion and altitude information to values"""
    self.lat = lat
    self.lon = lon
    self.alt = alt
    self.tz  = tz

  def get_passes(self):
    """This gets a web page with predictable output from www.heavens-above.com and parses it for all upcoming ISS passes"""
    
    def remove_chars(s, chars):
      """Useful utility, send it a drity string and a string of characters to strip from the dirty string"""
      for c in chars:
        s = s.replace(c,"")
      return s

    today = datetime.datetime.today()
    year = today.year
    passes_dict = []

    # Get the html page from www.heavens-above.com
    url = "http://www.heavens-above.com/AllPass1Sat.asp?satid=25544&lat=%f&lng=%f&alt=%0.0f&tz=%s" % (self.lat, self.lon, self.alt, self.tz)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()

    # Strip out tabs, new lines, and other white space
    data = remove_chars(data, '\t\n\r')

    # Get just the <table> with the data in it from the html
    table = data.split(r'<table BORDER CELLPADDING=5>')[1]
    table = table.split(r'</table>')[0]
    
    # Break out each row in the table, skip the first two (just contains metadata)
    passes = table.split('<tr>')[3:]

    # Go through each row
    for i, apass in enumerate(passes):
      # split the row into cells
      details = apass.split('<td>')
      
      # parse the data out into variables
      date          = details[1][-15:-9].strip()
      begin_time    = details[2][0:8].strip()
      begin_alt     = details[3][0:2].strip()
      begin_az      = details[4][0:3].strip()
      max_time      = details[5][0:8].strip()
      max_alt       = details[6][0:2].strip()
      max_az        = details[7][0:3].strip()
      end_time      = details[8][0:8].strip()
      end_alt       = details[9][0:2].strip()
      end_az        = details[10][0:3].strip()
      
      # further parse the date
      day   = date[0:2]
      month = date[3:]

      #debug
      #print i, date, month, day, begin_time, begin_alt, begin_az, max_time, max_alt, max_az, end_time, end_alt, end_az
      
      # Find the begining and ending dates and turn them into datetime objects
      begin_datetime  = datetime.datetime.strptime("%d-%s-%s %s" % (year, month, day, begin_time), "%Y-%b-%d %H:%M:%S")
      end_datetime    = datetime.datetime.strptime("%d-%s-%s %s" % (year, month, day, end_time),   "%Y-%b-%d %H:%M:%S")
      
      #debug
      #print i, begin_datetime, end_datetime
      
      # Store the data in a list
      passes_dict.append({"begin_time": begin_datetime, "end_time": end_datetime})
    
    # Return all the data 
    return passes_dict

  def get_next_pass(self):
    """This will try and get all the upcoming passes from www.heavens-above.com and store the data for upcoming one"""
    
    now = datetime.datetime.today()
    
    try:
      # Get all passes
      passes = self.get_passes()

      # Loop through the passes and find the first upcoming one
      for apass in passes:
        next_pass = apass["begin_time"]
        timedelta = next_pass - now
        past = timedelta.days
        if past >= 0:
          alarm_sleep_time = timedelta.seconds
          break

      # How long will this pass last?
      duration = apass["end_time"] - next_pass
      
      self.next_pass              = next_pass
      self.seconds_to_next_pass   = alarm_sleep_time
      self.pass_length            = duration.seconds
    except:
      # I don't know what to do here
      print "Time lookup failed!!"

class PyApplet():
  """A gnome-panel applet that alerts a user if the International Space Station is overhead"""

  alarm       = {}
  ha          = HeavensAbove(45.47361, -122.64931, 100, "PST")
  lamp        = lamp()
  iss_blank   = gtk.image_new_from_file("/usr/share/pixmaps/iss_blank.png")
  iss_pass    = gtk.image_new_from_file("/usr/share/pixmaps/iss_pass.png")

  def __init__(self, applet):
    self.applet=applet

    # Button
    self.button = gtk.Button()
    self.button.set_image(self.iss_blank) 
    self.button.connect('button-press-event', self.showMenu, self.applet)
    self.button.set_relief(gtk.RELIEF_NONE)
    self.applet.add(self.button)

    # Background
    self.applet.set_background_widget(self.applet)
  
    # We've now packed the UI, so show it
    self.applet.show_all()
    
    # Get the next pass
    self.ha.get_next_pass()
    
    # Next event
    self.alarm = gobject.timeout_add_seconds(self.ha.seconds_to_next_pass, self.pass_begin_alarm)

  def pass_begin_alarm(self):
    """Triggered when the begin pass alarm goes off"""
    # Turn on lights
    print "begin pass"
    self.begin_pass()
    
    # Next Event
    gobject.source_remove(self.alarm)
    self.alarm = gobject.timeout_add_seconds(self.ha.pass_length, self.pass_end_alarm) 
    return True
    
  def pass_end_alarm(self):
    """Triggered when the end pass alarm goes off"""
    # Turn lights off
    print "end pass"
    self.end_pass()

    # Get the next pass
    self.ha.get_next_pass()
    
    gobject.source_remove(self.alarm)
    self.alarm = gobject.timeout_add_seconds(self.ha.seconds_to_next_pass, self.pass_begin_alarm) 
    return True
  
  def begin_pass(self):
    self.button.set_image(self.iss_pass)
    self.lamp.lights_on()
  
  def end_pass(self):
    self.button.set_image(self.iss_blank)
    self.lamp.lights_off()
  
  def showMenu(self, button, event, applet):
    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
		  button.emit_stop_by_name("button_press_event")
		  self.create_menu(applet)

  def create_menu(self, applet):
    next_pass_string      = self.ha.next_pass.strftime("%a %H:%M:%S")
    time_to_pass          = self.ha.next_pass - datetime.datetime.today()
    time_to_pass_days     = time_to_pass.days
    time_to_pass_minutes  = int(time_to_pass.seconds / 60.0)
    
    if time_to_pass_days < 0:
      next_pass_string = "Not sure"
    else:
      next_pass_string      = next_pass_string + " - %d days, %d minutes" % (time_to_pass_days, time_to_pass_minutes)
    
    propxml="""
      <popup name="button3">
        <menuitem name="NextPass" verb="next_pass" label="_Next Pass: %s" />
        <menuitem name="Update" verb="update" label="_Update" />
        <menuitem name="LampTest" verb="test_lamp" label="_Test Lamp" />
        <menuitem name="AboutMenu" verb="about" label="_About" pixtype="stock" pixname="gtk-about"/>
      </popup>""" % (next_pass_string)
    
    verbs = [("next_pass", self.showAboutDialog), ("update", self.update_pass_data), ("test_lamp", self.test_lamp), ("about", self.showAboutDialog)]
    
    applet.setup_menu(propxml, verbs, None)
  
  def test_lamp(self, widget, menuname):
    self.lamp.lights_on()
    # short delay
    for i in range(1000):
      k = i + 1
    self.lamp.lights_off()
  
  def update_pass_data(self, widget, menuname):
    self.ha.get_next_pass()
    signal.alarm(0)
    signal.signal(signal.SIGALRM, self.pass_begin_alarm)
    signal.alarm(self.ha.seconds_to_next_pass)
  
  def showAboutDialog(self, widget, menuname):
    #print menuname
    pass

def class_factory(applet, iid):
  PyApplet(applet)
  return True

if len(sys.argv) == 2 and sys.argv[1] == "-debug":  
  print "running in window"
  main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
  main_window.set_title("Python Applet")
  main_window.connect("destroy", gtk.main_quit) 
  app = gnomeapplet.Applet()
  class_factory(app, None)
  app.reparent(main_window)
  main_window.show_all()
  gtk.main()
  sys.exit()

gnomeapplet.bonobo_factory("OAFIID:ISS_Gnome_Panel_Factory", 
                            gnomeapplet.Applet.__gtype__, 
                            "hello", "0", class_factory)
