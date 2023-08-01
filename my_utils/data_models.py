from pydantic import BaseModel, Field

class Task(BaseModel):
    taskId: str
    
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
    taskId: str
    status: str

class ProcessedImage(BaseModel):
    processedImage: str
    width: int
    height: int
    format: str