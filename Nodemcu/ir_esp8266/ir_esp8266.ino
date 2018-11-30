#include <IRrecv.h>

// an IR detector/demodulator is connected to GPIO pin 2
uint16_t RECV_PIN = D6;

IRrecv irrecv(RECV_PIN);

decode_results results;

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn();  // Start the receiver
}

void loop() {
  if (irrecv.decode(&results)) {
    unsigned int ircode = results.value;
    Serial.println(String(ircode));
    irrecv.resume();  // Receive the next value
    delay(1000);
  }
  delay(2000);
}
