/*
  Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
  Ported to Arduino ESP32 by Evandro Copercini
  updated by chegewara and MoThunderz
*/
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>
#include <sensors.h>
#include <bleserver.h>
#include <array>
#include <map>
#include <esp_sleep.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>


// Globals & pointers
// Create pointers for the BLE objects
//BLEServer* pServer = NULL;
BLECharacteristic* pTemperatureCharacteristic = NULL;
BLECharacteristic* pHumidityCharacteristic = NULL;
BLECharacteristic* pLuxCharacteristic = NULL;
BLECharacteristic* pSoilMoistureCharacteristic = NULL;
BLE2902 *pBLE2902;


uint32_t value = 0;


// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID "8aff4410-808a-4ce2-af5c-4122e0e05860"
#define TEMPERATURE_CHARACTERISTIC_UUID "c4d834e5-008d-4591-a977-351cc4c0b370"
#define HUMIDITY_CHARACTERISTIC_UUID "240e3b5b-c64e-44c8-b466-fdd4fa16e112"
#define LUX_CHARACTERISTIC_UUID "6264ad6f-193a-468d-b5b0-b687835a4495"
#define SOIL_MOISTURE_CHARACTERISTIC_UUID "9620b346-71ad-4469-8896-afe218d5cc9b"

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


void setup() {
  Serial.begin(115200);

  // Create the BLE Device
  BLEDevice::init("ESP32");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);



  // Create a BLE Characteristic
    // Create characteristics with descriptions
  pTemperatureCharacteristic = createCharacteristic(pService, 
      TEMPERATURE_CHARACTERISTIC_UUID, "Temperature Characteristic");
  pHumidityCharacteristic = createCharacteristic(pService, 
      HUMIDITY_CHARACTERISTIC_UUID, "Humidity Characteristic");
  pLuxCharacteristic = createCharacteristic(pService,
      LUX_CHARACTERISTIC_UUID, "Lux Characteristic");
  pSoilMoistureCharacteristic = createCharacteristic(pService,
      SOIL_MOISTURE_CHARACTERISTIC_UUID, "Soil moisture Characteristic");
  

  // Initialize the analog pins
  pinMode(analogPin1, INPUT);
  pinMode(analogPin2, INPUT);

  // Initialize the DHT sensor
  dht.begin();

  setupTsl(tsl);

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting for a client connection to notify...");
}

void loop() {
    // fetch the temperature and humidity values
    stringFloatMap dht_map = readAndPrintDht(dht);
    float temperature = dht_map["temperature"];
    float humidity = dht_map["humidity"];

    // fetch analog reads
    float rainDropValue = analogRead(analogPin1);
    float soilMoistureValue = analogRead(analogPin2);

    Serial.print(F("%  Soil Moisture: "));
    Serial.println(soilMoistureValue);

    // Read and print tsl value 
    stringFloatMap tsl_map = readAndPrintTsl(tsl);
    float lux = tsl_map["visibility"];

    // notify changed values
    if (deviceConnected) {
      notifyCharacteristic(pTemperatureCharacteristic, temperature);
      notifyCharacteristic(pHumidityCharacteristic, humidity);
      notifyCharacteristic(pLuxCharacteristic, lux);
      notifyCharacteristic(pSoilMoistureCharacteristic, soilMoistureValue);
    }
    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }

    delay(10000);
}