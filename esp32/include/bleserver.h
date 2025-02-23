#ifndef BLE_SERVER_H
#define BLE_SERVER_H

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>


bool deviceConnected = false;
bool oldDeviceConnected = false;

BLEServer* pServer = NULL;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Device connected");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Device disconnected");
    }
};

BLECharacteristic* createCharacteristic(BLEService *pService, const char* uuid, const char* description) {
  BLECharacteristic* pCharacteristic = pService->createCharacteristic(
      uuid,
      BLECharacteristic::PROPERTY_NOTIFY |
      BLECharacteristic::PROPERTY_READ |
      BLECharacteristic::PROPERTY_INDICATE
  );
  
  // Add the BLE2902 descriptor for notifications
  pCharacteristic->addDescriptor(new BLE2902());
  
  // Add the description descriptor
  BLEDescriptor* pDescriptor = new BLEDescriptor(BLEUUID((uint16_t)0x2901));
  pDescriptor->setValue(description);
  pCharacteristic->addDescriptor(pDescriptor);
  
  return pCharacteristic;
}

// Helper function to notify characteristic value
void notifyCharacteristic(BLECharacteristic* pCharacteristic, float value) {
  uint8_t bytes[4];
  memcpy(bytes, &value, sizeof(value));
  pCharacteristic->setValue(bytes, sizeof(bytes));
  pCharacteristic->notify();
}

#endif 