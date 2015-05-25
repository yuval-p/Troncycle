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
 
const int HallEffectPin1 = 2;         // the number of the pushbutton pin
const int HallEffectPin2 = 4;         // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

float TimeSinceStart;

int Magnet1State = 0;
int PrevMagnet1State = 0;
float Wheel1Rpm;
float PreviousTime1 = 0;
float MinutesForRound1 = 0;
float SecondsSinceLastChange1 = 0;


int Magnet2State = 0;
int PrevMagnet2State = 0;
float Wheel2Rpm;
float PreviousTime2 = 0;
float MinutesForRound2 = 0;
float SecondsSinceLastChange2 = 0;

void setup() 
{
    // Initialize Parameters
    Wheel1Rpm = 0;
    TimeSinceStart = 0;
    PreviousTime1 = 0;
    
    MinutesForRound1 = 0;
    SecondsSinceLastChange1 = 0;
    
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    
    // Initialize the pushbutton pin as an input:
    pinMode(HallEffectPin1, INPUT);
    
    pinMode(HallEffectPin2, INPUT);
}

void loop() 
{   
    // send * to signal header of sensors values
    Serial.println("*");
  
    // send the value of analog input 0 (potentiometer 1)
    Serial.println(analogRead(A0));
    
    // send the value of analog input 0 (potentiometer 2)
    Serial.println(analogRead(A2));
//    Serial.println((int)512);
    
    Magnet1State = digitalRead(HallEffectPin1);    
    Magnet2State = digitalRead(HallEffectPin2);    
    delay(2);
    
    TimeSinceStart = millis();
    
   CalcMagnet1Speed();
    CalcMagnet2Speed();
    
    Serial.println((int)Wheel1Rpm);
    
    //Serial.println((int)15);
    Serial.println((int)Wheel2Rpm);

    if (Magnet1State == HIGH) 
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

void CalcMagnet1Speed()
{
    if (Magnet1State != PrevMagnet1State)
    {  
        if (Magnet1State == HIGH)
        {
            MinutesForRound1 = (TimeSinceStart - PreviousTime1) / (60.0 * 1000);
        
            // Multiple by 2 since we have 2 magnets
             //MinutesForRound1 = MinutesForRound1 * 2;
        
            Wheel1Rpm = 1/MinutesForRound1;
            PreviousTime1 = TimeSinceStart;
        }
        
        PrevMagnet1State = Magnet1State;
    }
    else 
    {
       SecondsSinceLastChange1 = (TimeSinceStart - PreviousTime1)/(60.0 * 1000);
       
       if (SecondsSinceLastChange1 > MinutesForRound1 * 2)
       {
           Wheel1Rpm = 0;
       }
    }
}

void CalcMagnet2Speed()
{
    if (Magnet2State != PrevMagnet2State)
    {  
        if (Magnet2State == HIGH)
        {
          
          MinutesForRound2 = (TimeSinceStart - PreviousTime2) / (60.0 * 1000);
        
        // Multiple by 2 since we have 2 magnets
//        MinutesForRound2 = MinutesForRound2 * 2;
        
          Wheel2Rpm = 1/MinutesForRound2;
          PreviousTime2 = TimeSinceStart;
        }
        PrevMagnet2State = Magnet2State;
    }
    else 
    {
       SecondsSinceLastChange2 = (TimeSinceStart - PreviousTime2)/(60.0 * 1000);
       
       if (SecondsSinceLastChange2 > MinutesForRound2 * 2)
       {
           Wheel2Rpm = 0;
       }
    }
}

