/**
 * Simple indicator lamp. There are RGB LED's on the pins. This will listen on 
 * the serial port and pulse colors of light when it hears a "1". It will stop
 * pulsing on a "0"
 *
 * @author  Nathan Bergey <nathan.bergey@gmail.com>
 * @version Wednesday, June 08 2011
 *
 * @section LICENSE
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details at
 * http://www.gnu.org/copyleft/gpl.html
 */

static int redPin = 4;
static int grePin = 9;
static int bluPin = 5;

int dly = 300;

int redState = LOW;
int greState = LOW;
int command = 0;

boolean light = false;

void setup()
{
  RESET_PINS();
}

void loop()                     
{
  // Serial Commands
  if (Serial.available()) 
  {
    command = Serial.read();  // will not be -1
    if (command == 49) {     // "1"
      light = true;
    }
    if (command == 48) {     // "0"
      light = false;
    }
  }
  command = 0;

  if (light)
    pulse();
}

void pulse()
{
  // Pulse Up
  for (int i = 0; i < 256; i++)
  {
    analogWrite(grePin, i);
    
    if (i > 85)
      analogWrite(bluPin, i - 85);
    if (i > 170)
      analogWrite(redPin, i - 170);
    delay(10);
  }
  for (int i = 171; i < 256; i++)
  {
    analogWrite(bluPin, i);
    analogWrite(redPin, i - 85);
    delay(10);
  }
  for (int i = 171; i < 256; i++)
  {
    analogWrite(redPin, i);
    delay(10);
  }
  
  delay(1000);
  
  // Pulse Down
  for (int i = 255; i >= 0; i--)
  {
    analogWrite(grePin, i);
    delay(10);
  }
  
  for (int i = 255; i >= 0; i--)
  {
    analogWrite(redPin, i);
    delay(10);
  }
  
    
  for (int i = 255; i >= 0; i--)
  {
    analogWrite(bluPin, i);
    delay(10);
  }

}

void RESET_PINS()
{
  pinMode(redPin, OUTPUT);
  pinMode(grePin, OUTPUT);
  pinMode(bluPin, OUTPUT);
  
  digitalWrite(redPin, LOW);
  digitalWrite(grePin, LOW);
  digitalWrite(bluPin, LOW);
}

