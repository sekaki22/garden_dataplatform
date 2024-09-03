#ifndef UTILS_H
#define UTILS_H

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

String getFormattedLocalTime() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        return "Failed to obtain time"; // Return an error message if time is not available
    }
    
    // Format: yyyy-mm-dd hh:mm:ss
    char timeString[20]; // Buffer to hold the formatted time string
    snprintf(timeString, sizeof(timeString), "%04d-%02d-%02d %02d:%02d:%02d",
             timeinfo.tm_year + 1900,  // Years since 1900
             timeinfo.tm_mon + 1,      // Months since January [0, 11], so +1
             timeinfo.tm_mday,         // Day of the month [1, 31]
             timeinfo.tm_hour,         // Hours since midnight [0, 23]
             timeinfo.tm_min,          // Minutes after the hour [0, 59]
             timeinfo.tm_sec);         // Seconds after the minute [0, 60]

    return String(timeString); // Convert the C-style string to a String object and return it
}

// Read and print DHT values

std::map<std::string, float> readAndPrintDht (DHT dht){
    
    std::map<std::string, float> dhtValues; //Map values

    dhtValues["temperature"] = dht.readTemperature();
    dhtValues["humidity"] = dht.readHumidity();

    // Check if any reads failed and exit early (to try again).
    if (isnan(dhtValues["humidity"]) || isnan(dhtValues["temperature"])) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return std::map<std::string, float>();
    
  }

// print the temperature and humidity
  Serial.print(F("Humidity: "));
  Serial.println(dhtValues["humidity"]);
  Serial.print(F("%  Temperature: "));
  Serial.println(dhtValues["temperature"]);

  return dhtValues;
}



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

std::map<std::string, uint16_t> readAndPrintTsl (Adafruit_TSL2591 tsl){
    // Simple data read . Just read the infrared, fullspecrtrum diode 
  // and 'visible' (difference between the two) channels.
  // This can take 100-600 milliseconds! Uncomment whichever of the following you want to read
    
  std::map<std::string, uint16_t> tslValues; //Map values
    tslValues["visibility"] = tsl.getLuminosity(TSL2591_VISIBLE);
    tslValues["fullspec"] = tsl.getLuminosity(TSL2591_FULLSPECTRUM);
    tslValues["infrared"] = tsl.getLuminosity(TSL2591_INFRARED);
//   uint16_t visibility = tsl.getLuminosity(TSL2591_VISIBLE);
//   uint16_t fullspec = tsl.getLuminosity(TSL2591_FULLSPECTRUM);
//   uint16_t fullspec = tsl.getLuminosity(TSL2591_INFRARED);

  Serial.print(F("[ ")); Serial.print(millis()); Serial.print(F(" ms ] "));
  Serial.print(F("Visibility: "));
  Serial.println(tslValues["visibility"], DEC);
  Serial.print(F("Full Spectrum: "));
  Serial.println(tslValues["fullspec"], DEC);
  Serial.print(F("Infrared: "));
  Serial.println(tslValues["infrared"], DEC);
  delay(2000);

  return tslValues;
}

void sendHttpPostRequest(const String& url, const String& jsonPayload) {
    if (WiFi.status() == WL_CONNECTED) { // Check WiFi connection status
        HTTPClient http;

        http.begin(url);                 // Specify the URL
        http.addHeader("Content-Type", "application/json"); // Specify content-type header

        int httpResponseCode = http.POST(jsonPayload);  // Send the POST request

        if (httpResponseCode > 0) {
            String response = http.getString();          // Get the response to the request
            Serial.println(httpResponseCode);            // Print return code
            Serial.println(response);                    // Print the response
        } else {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }

        http.end();  // Free resources
    } else {
        Serial.println("WiFi not connected");
    }
}

#endif // UTILS_H