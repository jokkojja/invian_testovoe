from fastapi import FastAPI, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from my_utils.model import get_model, get_image_from_bytes, process_image
import io
from PIL import Image
import json
import uuid
import asyncio
from fastapi.middleware.cors import CORSMiddleware


model = get_model()

app = FastAPI(
    title="Invian testovoe API",
    description="Fire detection API",
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_status/{id}")
async def get_status(id):
    pass

@app.get("/get_bbox/{id}")
async def get_bbox(id):
    pass

@app.get("/get_predicted_image{id}")
async def get_predicted_image(id):
    pass

@app.get("/get_bbox_max/{id}")
async def get_bbox_max(id):
    pass

@app.post("/send_image")
async def task_processing(file: bytes = File(...)):
    # TODO: add task to queue and update status: in queue (DB)
    task_id = str(uuid.uuid4())
    # TODO: update task db: processing
    async_task = asyncio.create_task(process_image(file, model, task_id))
    return JSONResponse(content=jsonable_encoder({"task_id": task_id}))