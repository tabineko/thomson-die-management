
import serial
import time
 
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '//./COM3'
ser.parity = serial.PARITY_ODD
ser.open()
ser.close()
ser.parity = serial.PARITY_NONE
ser.open()
 
print('Serial warming up...')
time.sleep(2)
 
while True:
    line = ser.readline()
    print(line)