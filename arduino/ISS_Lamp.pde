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

