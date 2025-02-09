// This file creates a class that is used to create a BLE server and handle the connection and disconnection of the client.

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#ifndef MYSERVERCALLBACKS_H
#define MYSERVERCALLBACKS_H

bool deviceConnected = false;
bool oldDeviceConnected = false;

BLEServer* pServer = NULL;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

#endif 