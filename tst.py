import serial

# ser = serial.Serial("COM3", 115200)

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

print("connected to: " + ser.portstr)

OldAngle = 1024
OldSpeed = 0

ReceivedNumber = 0

# Angle is received first
ReceivingAngle = True

while True:
    char = ser.read()

    if (char != b'\r') & (char != b'\n'):
        ReceivedNumber = ReceivedNumber * 10 + float(char)
    if char == b'\n':
        if ReceivingAngle:
            # if (abs(ReceivedNumber - OldAngle) < 100):
            # print("angle: ", line)

            # if (abs(ReceivedNumber - OldAngle) > 100):
            # print("bad angle")
            # exit()
            old_angle = ReceivedNumber
        else:
            if (abs(ReceivedNumber - OldSpeed) < 100):
                print("speed: ", ReceivedNumber)
                x = 0
            # if (abs(ReceivedNumber - OldSpeed) > 100):
            #    print("bad speed")
            #    exit()
            old_speed = ReceivedNumber

        # Toggling the received parameter
        ReceivingAngle = not ReceivingAngle
        ReceivedNumber = 0
ser.close()
