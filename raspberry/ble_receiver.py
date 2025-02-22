import asyncio
from bleak import BleakScanner, BleakClient
from constants import BLE_SERVER_UUID
import struct

# Define the service UUID and characteristic UUID you want to read
# TARGET_SERVICE_UUID = "YOUR_SERVICE_UUID_HERE"  # Replace with your service UUID
TARGET_CHARACTERISTIC_UUID = "240e3b5b-c64e-44c8-b466-fdd4fa16e112"  # Replace with your characteristic UUID
TARGET_DEVICE_NAME = "ESP32"  # Replace with your device name

async def scan_and_connect():
    print("Scanning for BLE devices...")
    
    devices = await BleakScanner.discover()
    target_device = None
    
    for device in devices:
        print(f"Found device: {device.name} ({device.address})")
        if device.name and TARGET_DEVICE_NAME in device.name:
            target_device = device
            break
    
    if not target_device:
        print("Target device not found")
        return
    
    print(f"Connecting to {target_device.name}...")
    
    async with BleakClient(target_device.address) as client:
        try:
            if client.is_connected:
                print("Connected successfully!")
                
                # Notification handler
                def notification_handler(sender, data):
                    if len(data) == 4:
                        float_value = struct.unpack('<f', data)[0]
                        print(f"Notification received - Float value: {float_value}")
                    else:
                        print(f"Notification received - Raw data: {data}")

                # Enable notifications
                print("Subscribing to notifications...")
                await client.start_notify(TARGET_CHARACTERISTIC_UUID, notification_handler)
                
                # Keep connection alive to receive notifications
                print("Waiting for notifications...")
                while True:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            print(f"Error: {str(e)}")

async def main():
    while True:
        await scan_and_connect()
        await asyncio.sleep(5)  # Wait 5 seconds before scanning again

if __name__ == "__main__":
    asyncio.run(main())