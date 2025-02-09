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
#include <utils.h>
#include <classes.h>
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
//BLECharacteristic* pHumidityCharacteristic = NULL;
BLEDescriptor *pTemperatureDescriptor;
BLE2902 *pBLE2902;


uint32_t value = 0;


// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID "8aff4410-808a-4ce2-af5c-4122e0e05860"
#define TEMPERATURE_CHARACTERISTIC_UUID "c4d834e5-008d-4591-a977-351cc4c0b370"
//#define HUMIDITY_CHARACTERISTIC_UUID "240e3b5b-c64e-44c8-b466-fdd4fa16e112"

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

  pBLE2902 = new BLE2902();
  pBLE2902->setNotifications(true);

  // Create a BLE Characteristic
  pTemperatureCharacteristic = pService->createCharacteristic(
                                TEMPERATURE_CHARACTERISTIC_UUID,
                                BLECharacteristic::PROPERTY_NOTIFY |
                                BLECharacteristic::PROPERTY_READ |
                                BLECharacteristic::PROPERTY_INDICATE
                              );  

  // Create a BLE Descriptor and add it to the characteristic
  pTemperatureCharacteristic->addDescriptor(pBLE2902);
  

  // Create a BLE Descriptor
  // BLEDescriptor* pDescriptor = new BLEDescriptor(BLEUUID((uint16_t)0x2901));
  // // pTemperatureDescriptor->setValue("Temperature Characteristic");
  // pTemperatureCharacteristic->addDescriptor(pDescriptor);

  // Create a BLE Characteristic for humidity
  // pHumidityCharacteristic = pService->createCharacteristic(
  //                             HUMIDITY_CHARACTERISTIC_UUID,
  //                             BLECharacteristic::PROPERTY_NOTIFY |
  //                             BLECharacteristic::PROPERTY_READ |
  //                             BLECharacteristic::PROPERTY_INDICATE
  //                           );

  // Create a BLE Descriptor for humidity
  // BLEDescriptor* pHumidityDescriptor = new BLEDescriptor(BLEUUID((uint16_t)0x2901));
  // pHumidityDescriptor->setValue("Humidity Characteristic");
  // pHumidityCharacteristic->addDescriptor(pHumidityDescriptor);
  
  // pBLE2902 = new BLE2902();
  // pBLE2902->setNotifications(true);

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
    std::map<std::string, float> dht_map = readAndPrintDht(dht);
    float temperature = dht_map["temperature"];
    float humidity = dht_map["humidity"];

    // fetch analog reads
    float rainDropValue = analogRead(analogPin1);
    float soilMoistureValue = analogRead(analogPin2);

    // Read and print tsl value 
    std::map<std::string, uint16_t> tsl_map = readAndPrintTsl(tsl);

    // notify changed value
    if (deviceConnected) {
        uint8_t tempBytes[4];
        memcpy(tempBytes, &temperature, sizeof(temperature));
        // single precision
        pTemperatureCharacteristic->setValue(tempBytes, sizeof(tempBytes));
        pTemperatureCharacteristic->notify();

        // uint8_t humidityBytes[4];
        // memcpy(humidityBytes, &humidity, sizeof(humidity));
        // // single precision
        // pHumidityCharacteristic->setValue(humidityBytes, sizeof(humidityBytes));
        // pHumidityCharacteristic->notify();

        delay(10000);
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
}