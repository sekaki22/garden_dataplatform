from pydantic import BaseModel

class DHT22(BaseModel):
    temperature: float
    humidity: float

class TSL2591(BaseModel):
    lux: float
    visibility: float
    infrared: float

class SoilMoisture(BaseModel):
    analog_value: float

class RainDrop(BaseModel):
    analog_value: float