from fastapi import FastAPI, File, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from my_utils.model import get_model, get_image_from_bytes, process_image
import io
from PIL import Image
import json
import uuid
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from my_utils.database import *
import logging

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

@app.get("/get_status/{task_id}")
async def get_status(task_id):
    try:
        task_status = get_status_of_process(task_id)
    except Exception as e:
        response = {"errors": [e]}
        return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_400_BAD_REQUEST)
    response = {"status": task_status}
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.get("/get_bbox/{task_id}")
async def get_bbox(task_id):
    pass

@app.get("/get_predicted_image{task_id}")
async def get_predicted_image(task_id):
    pass

@app.get("/get_bbox_max/{task_id}")
async def get_bbox_max(task_id):
    pass

@app.post("/send_image")
async def task_processing(file: bytes = File(...)):
    # TODO: add task to queue and update status: in queue (DB)
    # TODO: add image validation process
    task_id = str(uuid.uuid4())
    try:
        create_object(task_id, str(file))
    # TODO: update task db: processing
        asyncio.create_task(process_image(file, model, task_id))
    except Exception as e:
        response = {"errors": [e]}
        return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_400_BAD_REQUEST)
    response = {"task_id": task_id}
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)