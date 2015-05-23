import serial

#ser = serial.Serial("COM3", 115200)

ser = serial.Serial(
	port='COM3',
	baudrate=115200,
	parity=serial.PARITY_ODD,
	stopbits=serial.STOPBITS_TWO,
	bytesize=serial.SEVENBITS
)
old_angle=1024
old_speed=0
print("connected to: " + ser.portstr)
line=0
flag_angle=True
while True:
    c=ser.read()
    #print(c)
    if (c!=b'\r')&(c!=b'\n'):
        line=line*10+float(c)
    if c==b'\n':
        if flag_angle:
            #if (abs(line-old_angle)<100):
                #print("angle: ", line)

            #if (abs(line-old_angle)>100):
                #print("bad angle")
                #exit()
            old_angle=line
        else:
            if (abs(line-old_speed)<100):
                print("speed: ", line)
                x = 0
            #if (abs(line-old_speed)>100):
            #    print("bad speed")
            #    exit()
            old_speed=line
        flag_angle=not flag_angle
        line=0
ser.close()