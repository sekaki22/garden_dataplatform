#include <Arduino.h>
#include <WiFi.h>
#include <time.h>
#include <environment_var.h>
#include <DHT.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>
#include <SPI.h>
#include <utils.h>
#include <array>
#include <map>

// Wi-Fi credentials from build flags
// const char* ssid = WIFI_SSID;
// const char* password = WIFI_PASSWORD;

// Define DHT version
#define DHTTYPE DHT22



// Read digital pins
const int digitalPin1 = 18;

// Read analog pins
const int analogPin1 = 32; // Analog input pin 1 (GPIO32)
const int analogPin2 = 33; // Analog input pin 2 (GPIO33)

// Time configuration
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 7200;
const int   daylightOffset_sec = 0;

DHT dht(digitalPin1, DHTTYPE);

 // Define tsl2591 object 
//Adafruit_TSL2591  tsl = Adafruit_TSL2591(2591);



void setup() {
    // Configure the pins
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);
  Serial.begin(921600);
  Serial.println("Hello from setup");
  Serial.println(ssid);
  Serial.println(password);

    // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected to Wi-Fi");

  // begin dht stream
  dht.begin();

  // setup tsl
  //setupTsl(tsl);

  // Initialize time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  delay(2000);

}

void loop() {
  delay(2000);

  // Read and print the date and time
  String dateTimeNow = getFormattedLocalTime();
  Serial.print("Current datetime:  ");
  Serial.println(dateTimeNow);

  std::map<std::string, float> dht_map = readAndPrintDht(dht);

  // Read analog values
  float rainDropValue = analogRead(analogPin1);
  float soilMoistureValue = analogRead(analogPin2);


  // Print the values to the Serial Monitor
  Serial.print("Analog Value for raindrop module: ");
  Serial.println(rainDropValue/1000);
  Serial.print("Analog Value for soil moisture module: ");
  Serial.println(soilMoistureValue/1000);

  // Read and print tsl value 
  //std::map<std::string, uint16_t> tsl_ma = readAndPrintTsl(tsl);

  // Send data over http to raspberry
  String temperature = String(dht_map["temperature"], 2);
  String humidity = String(dht_map["humidity"], 2);
  String dhtUrl = "http://"+privateIpPi+portnumber+"/sensors/dht_22";
  String payLoad = "{\"temperature\":" + temperature +",\"humidity\":" + humidity +"}";
  Serial.println(dhtUrl);
  Serial.println(payLoad);

  sendHttpPostRequest(dhtUrl, payLoad);

  // Add a small delay for stability
  delay(2000);

}
