#include <IRremoteInt.h>

#include <IRremote.h> 
int receiver = 11;          // pin di ricezione del segnale IR
IRrecv irrecv(receiver); 
decode_results results;

void setup()
{
  Serial.begin(9600); 
  irrecv.enableIRIn(); // inizio a ricevere
}
void loop()
{
  if (irrecv.decode(&results)) // se ricevo un segnale IR stampo quello che ho ricevuto
  {
    Serial.println(results.value, HEX); 
    irrecv.resume();
    delay(1000);
  }
   delay(2000);
}
