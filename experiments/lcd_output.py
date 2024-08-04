from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import board
import adafruit_dht
import time

#Configure devices
lcd = LCD()
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio = False)

def safe_exit(signum, frame):
    exit(1)
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

while(True):
    try:
     
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        lcd.text(f"Temp: {temperature} C", 1)
        lcd.text(f"Humidity: {humidity} %", 2)
        time.sleep(5)
    


    except Exception as e:
        print(f"Exception encountered:\n{e}")
 
