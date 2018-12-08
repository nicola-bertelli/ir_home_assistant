import serial
import time
import getpass
import yaml

utente = getpass.getuser()
if (utente == "root"):
    print
    print ("esci da modalita ROOT e riavvia lo script")
    print ("GRAZIE")
    print
    exit()

try:
    print
    file_configurazione = "/home/" + utente + "/telecomando/config.yaml"
    with open(file_configurazione, 'r') as ymlfile:
        configurazione = yaml.load(ymlfile)
except:
    print ("File di configurazione non trovato")
    exit()
print ("File di configurazione impostato " + file_configurazione)
print

# LEGGO LA PORTA SERIALE
porta_seriale = configurazione['node_arduino']['porta_seriale']
print ('porta seriale utilizzata ' + str(porta_seriale))

arduino = serial.Serial(porta_seriale, 9600)


while 1:
	if(arduino.inWaiting()>0):
		dati = (arduino.readline()).split('\r')[0]
		print dati
