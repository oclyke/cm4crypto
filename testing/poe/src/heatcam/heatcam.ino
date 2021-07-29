#include <Wire.h>
#include <SparkFun_GridEYE_Arduino_Library.h>

#define WIRE_PORT Wire
#define SERIAL_PORT Serial
#define BAUD_RATE 115200
GridEYE grideye;

long start_ms = 0;

void setup() {
  WIRE_PORT.begin();
  grideye.begin(DEFAULT_ADDRESS, WIRE_PORT);
  SERIAL_PORT.begin(BAUD_RATE);

  SERIAL_PORT.println("waiting to start test.\nsend any ccharacter to begin\n");
  while(!SERIAL_PORT.available()){
  }

  start_ms = millis();
}

void loop() {

  long elapsed = millis() - start_ms;

  SERIAL_PORT.print("{\"elapsed_ms\": ");
  SERIAL_PORT.print(elapsed);
  SERIAL_PORT.print(", \"pixels\": [");

  for(uint8_t i = 0; i < 64; i++){
    SERIAL_PORT.print(grideye.getPixelTemperature(i));
    if(i != 63){
      SERIAL_PORT.print(",");
    }
  }

  SERIAL_PORT.print("]}\n");
}
