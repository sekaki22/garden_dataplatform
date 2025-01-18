#include <Arduino.h>
#include <WiFi.h>
//#include <time.h>
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
#include <esp_sleep.h>

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
const int analogPin3 = 34; // Analog input pin for battery voltage read (GPIO34)


DHT dht(digitalPin1, DHTTYPE);

 // Define tsl2591 object 
Adafruit_TSL2591  tsl = Adafruit_TSL2591(2591);

// Define enpoints
String dht_endpoint = "/sensors/dht22";
String tsl_endpoint = "/sensors/tsl2591";
String analog_endpoint = "/sensors/analog_inputs";


void setup() {
    // Configure the pins
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);
  Serial.begin(115200);
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
  setupTsl(tsl);

  // Initialize time
  // configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  delay(10000);

}

void loop() {
  // Read and print the date and time
  // String dateTimeNow = getFormattedLocalTime();
  // Serial.print("Current datetime:  ");
  // Serial.println(dateTimeNow);

  std::map<std::string, float> dht_map = readAndPrintDht(dht);

  // Read and print tsl value 
  std::map<std::string, uint16_t> tsl_map = readAndPrintTsl(tsl);

  // Send data over http to raspberry for dht
  String temperature = String(dht_map["temperature"], 2);
  String humidity = String(dht_map["humidity"], 2);
  String dhtUrl = "http://"+privateIpPi+portnumber+dht_endpoint;
  String dhtPayLoad = "{\"temperature\":" + temperature +",\"humidity\":" + humidity +"}";
  Serial.println(dhtUrl);
  Serial.println(dhtPayLoad);

  sendHttpPostRequest(dhtUrl, dhtPayLoad);

  // Send data over http to raspberry for tsl
  String lux = String(tsl_map["fullspec"]);
  String visibility = String(tsl_map["visibility"]);
  String infrared = String(tsl_map["infrared"]);
  String tslUrl = "http://"+privateIpPi+portnumber+tsl_endpoint;
  String tslPayLoad = "{\"lux\":" + lux +",\"visibility\":" + visibility +
                       ", \"infrared\":"+infrared+"}";
  Serial.println(tslUrl);
  Serial.println(tslPayLoad);

  sendHttpPostRequest(tslUrl, tslPayLoad);

  // Send analog signals to raspberry 
  float rainDropValue = analogRead(analogPin1);
  float soilMoistureValue = analogRead(analogPin2);
  String rainDropUrl = "http://"+privateIpPi+portnumber+analog_endpoint+"?table_name=raindrop_sens";
  String soilMoistureUrl = "http://"+privateIpPi+portnumber+analog_endpoint+"?table_name=soil_moisture_sens";
  String rainDropPL = "{\"analog_value\":" + String(rainDropValue) + "}";
  String soilMoisturePL = "{\"analog_value\":" + String(soilMoistureValue) + "}";

  sendHttpPostRequest(rainDropUrl, rainDropPL);
  sendHttpPostRequest(soilMoistureUrl, soilMoisturePL);

  // voltage read experiment
  // float adcMillivolts =  analogRead(analogPin3);
  // String voltageUrl = "http://"+privateIpPi+portnumber+analog_endpoint+"?table_name=voltage_sens";
  // String voltagePL = "{\"battery_voltage\":" + String(adcMillivolts) + "}";
  // sendHttpPostRequest(voltageUrl, voltagePL);

  // Go into deep sleep mode to save costs
  // esp_sleep_enable_timer_wakeup(60 * 1000000);  // 60 seconds (1 minute) in microseconds
  // Serial.println("Going to sleep for 60 seconds...");
  // esp_deep_sleep_start();

  delay(60000);


}

