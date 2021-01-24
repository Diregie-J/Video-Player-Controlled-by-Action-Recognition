/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int channelOne = analogRead(A0);
  int channelTwo = analogRead(A1);
  int channelThree = analogRead(A2);
  // print out the value you read:
  String blank = " ";
  Serial.println(channelOne + blank + channelTwo + blank + channelThree);
  delay(1);        // delay in between reads for stability
}
