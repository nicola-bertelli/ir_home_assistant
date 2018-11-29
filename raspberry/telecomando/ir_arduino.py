import serial
import time
time.sleep(2)
arduino = serial.Serial('/dev/ttyUSB1',9600)

while 1:
	if(arduino.inWaiting()>0):
		dati = str((arduino.readline()).split("\n")[0])
		print dati
