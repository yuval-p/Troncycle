import serial
from array import array

Count = 10

Speed1Samples = array("i", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
Speed2Samples = array("i", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

class sensor_input():

    ANGLE1 = 0
    ANGLE2 = 0
    SPEED1 = 0
    SPEED2 = 0
    ser = 0

    def __init__(self):
        self.speed = 1
        self.angle = 0
        self.initSensor()

    def getSpeed1(self):
        return self.SPEED1

    def getAngle1(self):
        return self.ANGLE1

    def getSpeed2(self):
        return self.SPEED2

    def getAngle2(self):
        return self.ANGLE2

    def initSensor(self):
        self.ser = serial.Serial(
            port='COM26',
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

        print("connected to: " + self.ser.portstr)

    def start_sensor(self):

        OldAngle = 1024
        OldSpeed = 0

        ReceivedNumber = 0

        # Angle is received first
        ReceivingSensor = 0
        StartReading = False

        while True:
            char = self.ser.read()
            if (char == b'*'):
                ReceivingSensor = 0
                ReceivedNumber = 0
                StartReading = True
            elif (StartReading):
                if (char != b'\r') & (char != b'\n'):
                    ReceivedNumber = ReceivedNumber * 10 + float(char)
                elif char == b'\n':
                    if ReceivingSensor == 1:
                        self.ANGLE1 = ReceivedNumber
                        print("Real " + (str)(ReceivedNumber))
                    elif ReceivingSensor == 2:
                        self.ANGLE2 = ReceivedNumber
                        print(ReceivedNumber)
                    elif ReceivingSensor == 3:
                        mean = CalcMean(Speed1Samples, ReceivedNumber)
                        #print(Speed1Samples[Count-1])
                        self.SPEED1 = mean
                    elif ReceivingSensor == 4:
                        mean = CalcMean(Speed2Samples, ReceivedNumber)
                        self.SPEED2 = mean
                        #print(ReceivedNumber)
                        StartReading = False

                    # incrementing receiving sensor
                    ReceivingSensor = (ReceivingSensor + 1) % 5
                    ReceivedNumber = 0

def CalcMean(arr, newNum):
    for i in range(0, Count-1):
        arr[i] = arr[i+1]

    arr[Count-1] = (int)(newNum)

    sum = 0;

    for num in arr:
        sum = sum + num

    result = sum/len(arr)

    return result

#def stop(self):
  #  ser.close() TODO
#bla = sensor_input()

#bla.start_sensor()