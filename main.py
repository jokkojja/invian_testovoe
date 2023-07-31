from fastapi import FastAPI, File, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import RequestValidationError
from my_utils.model import get_model, get_image_from_bytes, process_image, TTL
from PIL import Image
import uuid
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import my_utils.database as database
from my_utils.data_models import *
from typing import Dict, List
from my_utils.exception_handlers import validation_exception_handler
from my_utils.database import set_ttl_index

model = get_model()
set_ttl_index(TTL)
# TODO: add semaphore as queue?

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
async def get_status(task_id: str) -> JSONResponse:
    task_status = database.get_status_of_process(task_id)
    response = {"status": task_status}
    if task_status is None:
         response['detail'] = 'Status for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.get("/get_bbox/{task_id}", response_model=Dict[str, List[Bbox]])
async def get_bbox(task_id: str) -> JSONResponse:
    bbox = database.get_bbox_of_process(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Bbox for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)
    
@app.get("/get_processed_image/{task_id}")
async def get_processed_image(task_id: str) -> JSONResponse:
    image = database.get_processed_image(task_id)
    response = {'processedImage': image}
    if image is None:
        response['detail'] = 'Processed image for such ID not found. Check the correctness of the ID or status.'
    return response

@app.get("/get_bbox_max/{task_id}", response_model=Dict[str, Bbox])
async def get_bbox_max(task_id: str) -> JSONResponse:
    bbox = database.get_max_bbox(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Max bbox for such ID not found. Check the correctness of the ID or status.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.post("/send_image")
async def task_processing(file: bytes = File(...)) -> JSONResponse:
    # TODO: add task to queue and update status: in queue (DB)
    # TODO: add image validation process
    task_id = str(uuid.uuid4())
    try:
        database.create_object(task_id)
# TODO: update task db: processing
        asyncio.create_task(process_image(file, model, task_id))
    except Exception as e:
        response = {"errors": [e]}
        return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_400_BAD_REQUEST)
    response = {"task_id": task_id}
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)