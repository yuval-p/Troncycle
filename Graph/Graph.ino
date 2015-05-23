/*
  Graph

 A simple example of communication from the Arduino board to the computer:
 the value of analog input 0 is sent out the serial port.  We call this "serial"
 communication because the connection appears to both the Arduino and the
 computer as a serial port, even though it may actually use
 a USB cable. Bytes are sent one after another (serially) from the Arduino
 to the computer.

 You can use the Arduino serial monitor to view the sent data, or it can
 be read by Processing, PD, Max/MSP, or any other program capable of reading
 data from a serial port.  The Processing code below graphs the data received
 so you can see the value of the analog input changing over time.

 The circuit:
 Any analog input sensor is attached to analog in pin 0.

 created 2006
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe and Scott Fitzgerald

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/Graph
 */
 
const int ozPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

int ozState = 0;
int ozlastState = 0;
float WheelRpm;
float PreviousTime = 0;
float MinutesForRound = 0;
float sec_since_last_change;
float TimeSinceStart;

void setup() 
{
    // Initialize Parameters
    WheelRpm = 0;
    TimeSinceStart = 0;
    PreviousTime = 0;
    
    MinutesForRound = 0;
    sec_since_last_change=0;
    
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    
    // Initialize the pushbutton pin as an input:
    pinMode(ozPin, INPUT);
}

void loop() 
{   
    // send the value of analog input 0:
    ozState = digitalRead(ozPin);
    Serial.println(analogRead(A0));
    
    // wait a bit for the analog-to-digital converter
    // to stabilize after the last reading:
    
    TimeSinceStart = millis();
    
    if (ozState != ozlastState)
    {  
        MinutesForRound = (TimeSinceStart - PreviousTime) / (60.0 * 1000);
        
        // Multiple by 2 since we have 2 magnets
        MinutesForRound = MinutesForRound * 2;
        
        WheelRpm = 1/MinutesForRound;
        PreviousTime = TimeSinceStart;
        ozlastState = ozState;
    }
    else 
    {
       sec_since_last_change = (TimeSinceStart - PreviousTime)/(60.0*1000);
       
       if (sec_since_last_change>MinutesForRound * 3)
       {
           WheelRpm = 0;
       }
     }
 
    Serial.println((int)WheelRpm);

    if (ozState == HIGH) 
    {
        // turn LED on:
        digitalWrite(ledPin, HIGH);
    }
    else 
    {
        // turn LED off:
        digitalWrite(ledPin, LOW);
    }
}

