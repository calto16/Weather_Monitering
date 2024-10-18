from pydantic import BaseModel

class EmailRequest(BaseModel):
    city: str
    temperature: float
    email: str

class AlertThreshold(BaseModel):
    email: str
    city: str
    temperature_threshold: float