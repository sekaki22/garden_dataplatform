from pydantic import BaseModel

class DHT22(BaseModel):
    temperature: float
    humidity: float

class TSL2591(BaseModel):
    lux: float
    visibility: float
    infrared: float

class BasicAnalogSensor(BaseModel):
    analog_value: float

