#include <IRrecv.h>

uint16_t RECV_PIN = D6; // pin di ricezione del segnale IR

IRrecv irrecv(RECV_PIN);

decode_results results;

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn();  // inizio a ricevere
}

void loop() {
  if (irrecv.decode(&results)) {
    unsigned int ircode = results.value;
    Serial.println(String(ircode)); //stampo il codice ricevuto
    irrecv.resume();  
    delay(1000);
  }
  delay(2000);
}
