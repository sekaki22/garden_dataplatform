import asyncio
from bleak import BleakScanner, BleakClient
import struct
from dataclasses import dataclass
from typing import Dict, Optional, Callable

@dataclass
class BLECharacteristic:
    uuid: str
    name: str
    value: float = 0.0

class BLEHandler:
    def __init__(self, device_name: str, characteristics: Dict[str, str]):
        self.device_name = device_name
        self.characteristics = {
            uuid: BLECharacteristic(uuid=uuid, name=name)
            for uuid, name in characteristics.items()
        }
        self.client: Optional[BleakClient] = None

    def notification_handler(self, characteristic_uuid: str) -> Callable:
        def handle_notification(sender, data):
            if len(data) == 4:
                float_value = struct.unpack('<f', data)[0]
                self.characteristics[characteristic_uuid].value = float_value
                print(f"{self.characteristics[characteristic_uuid].name}: {float_value}")
            else:
                print(f"Raw data for {self.characteristics[characteristic_uuid].name}: {data}")
        return handle_notification

    async def scan_for_device(self):
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Found device: {device.name} ({device.address})")
            if device.name and self.device_name in device.name:
                return device
        return None

    async def connect_and_subscribe(self):
        device = await self.scan_for_device()
        if not device:
            print("Target device not found")
            return

        print(f"Connecting to {device.name}...")
        async with BleakClient(device.address) as client:
            try:
                if client.is_connected:
                    print("Connected successfully!")
                    
                    # Subscribe to all characteristics
                    for uuid in self.characteristics:
                        print(f"Subscribing to {self.characteristics[uuid].name}...")
                        await client.start_notify(
                            uuid, 
                            self.notification_handler(uuid)
                        )
                    
                    print("Waiting for notifications...")
                    while True:
                        await asyncio.sleep(1)
                        
            except Exception as e:
                print(f"Error: {str(e)}")

    async def run(self):
        while True:
            await self.connect_and_subscribe()
            await asyncio.sleep(5)

def main():
    # Define characteristics with their UUIDs and names
    characteristics = {
        "240e3b5b-c64e-44c8-b466-fdd4fa16e112": "Temperature",
        "c4d834e5-008d-4591-a977-351cc4c0b370": "Humidity"
    }
    
    handler = BLEHandler("ESP32", characteristics)
    asyncio.run(handler.run())

if __name__ == "__main__":
    main()