#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h> // Include Arduino core for String type and Serial
#include <time.h>    // Include time library for struct tm and getLocalTime
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>
#include <SPI.h>
#include <array>
#include <map>
#include <WiFi.h>
#include <HTTPClient.h>

typedef std::map<std::string, float> stringFloatMap;

//Provision TSL
void setupTsl (Adafruit_TSL2591 tsl){
    
  sensor_t sensor;
  tsl.getSensor(&sensor);

  Serial.println(F("Starting Adafruit TSL2591 Test!"));
  
  if (tsl.begin()) 
  {
    Serial.println(F("Found a TSL2591 sensor"));
  } 
  else 
  {
    Serial.println(F("No sensor found ... check your wiring?"));
    while (1);
  }

}

// Read and print DHT values

stringFloatMap readAndPrintDht (DHT dht){
  
  stringFloatMap dhtValues; //Map values

  dhtValues["temperature"] = dht.readTemperature();
  dhtValues["humidity"] = dht.readHumidity();

  // Check if any reads failed and exit early (to try again).
  if (isnan(dhtValues["humidity"]) || isnan(dhtValues["temperature"])) {
  Serial.println(F("Failed to read from DHT sensor!"));
  return stringFloatMap();
  
  }

// print the temperature and humidity
  Serial.print(F("Humidity: "));
  Serial.println(dhtValues["humidity"]);
  Serial.print(F("%  Temperature: "));
  Serial.println(dhtValues["temperature"]);

  return dhtValues;
}


stringFloatMap readAndPrintTsl (Adafruit_TSL2591 tsl){
    // Simple data read . Just read the infrared, fullspecrtrum diode 
  // and 'visible' (difference between the two) channels.
  // This can take 100-600 milliseconds! Uncomment whichever of the following you want to read
    
  std::map<std::string, float> tslValues; //Map values
    tslValues["visibility"] = (float)tsl.getLuminosity(TSL2591_VISIBLE);
    tslValues["fullspec"] = (float)tsl.getLuminosity(TSL2591_FULLSPECTRUM);
    tslValues["infrared"] = (float)tsl.getLuminosity(TSL2591_INFRARED);

  Serial.print(F("[ ")); Serial.print(millis()); Serial.print(F(" ms ] "));
  Serial.print(F("Visibility: "));
  Serial.println(tslValues["visibility"], DEC);
  Serial.print(F("Full Spectrum: "));
  Serial.println(tslValues["fullspec"], DEC);
  Serial.print(F("Infrared: "));
  Serial.println(tslValues["infrared"], DEC);

  return tslValues;
}

#endif // SENSORS_H