from pydantic import BaseModel, Field
from fastapi import File

class Task(BaseModel):
    id: str
    
class Bbox(BaseModel):
    index: int
    xcenter: float = Field(ge=0)
    ycenter: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)
    confidence: float = Field(ge=0)
    class_: int
    name: str    

class Status(BaseModel):
    status: str

class ProcessedImage(BaseModel):
    pass