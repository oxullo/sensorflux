#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

Adafruit_BMP280 bmp; // I2C

void setup() {
  Serial.begin(9600);
  //Serial.println(F("BMP280 test"));
  if (!bmp.begin()) {
    //Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }
  
  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  if (Serial.available() > 0) {
    if (Serial.read() == 'A') {
      Serial.print(bmp.readTemperature());
      Serial.print("\t");

      Serial.print(bmp.readPressure()/100.0);
      Serial.print("\t");

      Serial.print(bmp.readAltitude(1013.25)); /* Adjusted to local forecast! */

      Serial.println();
    }
  }


}
