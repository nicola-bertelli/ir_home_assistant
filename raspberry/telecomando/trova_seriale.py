import serial
import yaml
import getpass

porte = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
porta = ' '

for porta in porte:
    try:
        arduino = serial.Serial(porta, 9600)
        porta_seriale = porta
        break
    except:
        porta = ' '

print (' ')
if porta != ' ':
    print ('porta seriale utilizzata ' + str(porta))
else:
	exit()



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
	configurazione ['node_arduino']['porta_seriale'] = porta
	print ('Vuoi che aggiorni il file di configurazione con la porta seriale ' + str(porta) + ' ?')
	risposta = raw_input()
	if (risposta=='s' or risposta=='S'):
		with open(file_configurazione, "w") as ymlfile:
			yaml.dump(configurazione, ymlfile, default_flow_style=False, allow_unicode=True)
		print (' ')
		print ("file di configurazione modificato")

	else:
		print (' ')
		print ("file di configurazione non modificato")
except:
    print ("File di configurazione non trovato")
    exit()

print
