import json
import time
import requests
import yaml
import serial

try:
    print
    file_configurazione = "/home/pi/telecomando/config.yaml"
    with open(file_configurazione, 'r') as ymlfile:
        configurazione = yaml.load(ymlfile)
except:
    print ("File di configurazione non trovato")
    exit()
print ("File di configurazione impostato " + file_configurazione)
print


# LEGGO LE VARIABILI DI STATO DI HOME ASSISTANT
# E APRO IL COLLEGAMENTO SERIALE CON ARDUINO
host_ha = configurazione['host_ha']['host']
tocken = 'Bearer ' + configurazione['host_ha']['tocken']
porta_seriale = configurazione['node_arduino']['porta_seriale']

arduino = serial.Serial(porta_seriale, 9600)


# ROUTINE DA ESEGUIRE CON LA CONFIGURAZIONE "COMANDO"
def comando_HA(nome_entita, servizio):
    print ("entita ricevuta " + nome_entita + " servizio ricevuto " + servizio)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': tocken,
    }
    data = '{"entity_id": "%s" }' % nome_entita
    try:
        response = requests.post( host_ha + '/api/services/' + servizio.split('.')[0] + '/' + servizio.split('.')[1], headers=headers, data=data)
        print ("azione requests.post eseguita correttamente")
    except:
        print "errore requests"



# ROUTINE PER LEGGERE IL VALORE DELLA LUMINOSITA DA HA
# IN CASO DI ERRORE RITORNA 10
def stato_luminosita(nome_entita):
    try:
        headers = {'Authorization' : tocken, 'Content-Type':'application/json' }
        statoj = json.loads((requests.get((host_ha + '/api/states/' + entita), headers=headers)).text)
        stato = str(statoj['attributes']['brightness'])
        print ("stato luminosita lettura da HA " + stato)
        return stato
    except:
        print "errore lettura Json, imposto la luminosita a 10 "
        stato = "10"
        return stato


# ROUTINE PER ATTRIBUIRE ALLA LUCE I DATI IMPOSTATI DA CONFIGURAZIONE
def controllo_luce(nome_entita, servizio, lum, colore):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': tocken,
    }
    if (servizio == "light.turn_on"):
        if (lum == " "):
            lum = stato_luminosita(nome_entita)
            print ("lettura luce da HA " + str(lum))

        data = '{"entity_id": "%s","brightness":"%s"' % (nome_entita, lum)
        if (colore != " "):
            data = data + ', "color_name":"%s" }' % (colore)
        else: data = data + '}'
    elif (servizio == "light.turn_off"):
        data = '{"entity_id": "%s" }' % nome_entita

    try:
        response = requests.post( host_ha + '/api/services/' + servizio.split('.')[0] + '/' + servizio.split('.')[1], headers=headers, data=data)
        print ("comando luce inviato correttamente ")
    except:
        print "errore requests"

print "----------------------------------------"


while True:
    if(arduino.inWaiting()>0):
        # LEGGO I CARATTERI CHE MI INVIA ARDUINO
        dati = (arduino.readline()).split('\r')[0]
        print (" ")
        print ("codice ricevuto da Arduino %s") %(dati)

        # VADO A LEGGERE I DATI DEL FILE DI CONFIGURAZIONE
        with open(file_configurazione, 'r') as ymlfile:
            configurazione = yaml.load(ymlfile)

        for leggi in (configurazione['pulsanti_telecomando']):
            tipo_azione = ((leggi.keys()[0]))
            codice = (leggi[tipo_azione]['codice'])

            # SE IL CODICE LETTO DALLA CONFIGURAZIONE = DATI LETTI DA ARDUINO
            if (codice == dati):

                if tipo_azione == 'comando':
                    bottone = leggi[tipo_azione]['nome_pulsante']
                    entita = leggi[tipo_azione]['entita']
                    print ("tipo azione configurata: " + str(tipo_azione))
                    print ("hai premuto il pulsante: " + str(bottone))
                    print ("entita configurata: " + str(entita))

                    servizio = leggi[tipo_azione]['servizio']
                    print ("servizio configurato " + str(servizio))

                    if (servizio == "light.turn_on"):
                        try:
                            colore = leggi[tipo_azione]['dati']['colore']
                            print ("colore configurato " + str(colore))
                        except:
                            print ("colore non settato")
                            colore = " "
                        try:
                            luminosita = leggi[tipo_azione]['dati']['luminosita']
                            print ("luminosita settata " + str(luminosita))
                        except:
                            print ("luminosita non settata")
                            luminosita = " "
                        controllo_luce( entita, servizio, luminosita, colore)

                    else: comando_HA( entita, servizio)

                if tipo_azione == 'dimmer':
                    bottone = leggi[tipo_azione]['nome_pulsante']
                    entita = leggi[tipo_azione]['entita']
                    print ("tipo azione configurata: " + str(tipo_azione))
                    print ("hai premuto il pulsante: " + str(bottone))
                    print ("entita configurata: " + str(entita))

                    direzione = leggi[tipo_azione]['direzione']
                    skip = str(leggi[tipo_azione]['skip'])
                    print ("intervallo dimmer impostato: " + skip)

                    luminosita = str(stato_luminosita(entita))
                    if (direzione == "+"): luminosita = int(luminosita) + int(skip)
                    if (direzione == "-"): luminosita = int(luminosita) - int(skip)
                    print "luminosita inviata: " + str(luminosita)
                    controllo_luce(entita, "light.turn_on", luminosita, " ")


                if tipo_azione == 'comando_alternato':
                    bottone = leggi[tipo_azione]['nome_pulsante']
                    prossimo_servizio = str(leggi[tipo_azione]['servizio_da_eseguire'])
                    print "prossimo servizio " + str(prossimo_servizio)
                    entita = leggi[tipo_azione][prossimo_servizio]['entita']
                    servizio = leggi[tipo_azione][prossimo_servizio]['servizio']

                    print ("tipo azione configurata: " + str(tipo_azione))
                    print ("hai premuto il pulsante: " + str(bottone))
                    print ("entita configurata: " + str(entita))
                    print ("servizio impostato " + str(servizio))

                    comando_HA(entita, servizio)

                    if prossimo_servizio == 'servizio_uno': prossimo_servizio = 'servizio_due'
                    else: prossimo_servizio = 'servizio_uno'
                    leggi[tipo_azione]['servizio_da_eseguire'] = prossimo_servizio

                    with open(file_configurazione, "w") as ymlfile:
                        yaml.dump(configurazione, ymlfile, default_flow_style=False, allow_unicode=True)


        print " "
        print "----------------------------------------"
        print " "
