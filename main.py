import asyncio
from typing import Dict, List

import magic

from bson import ObjectId
from fastapi import FastAPI, File, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import my_utils.config as config
import my_utils.database as database
from my_utils.data_models import Bbox, ProcessedImage, Status, Task
from my_utils.model import get_model, process_image

model = get_model() # upload model
database.set_ttl_index(config.TTL) # set ttl index in database
semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_TASKS)

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

@app.get("/get_status/{task_id}", response_model = Status)
async def get_status(task_id: str) -> JSONResponse:
    """ Get status of task.

    Args:
        task_id (str): Id of task.

    Returns:
        JSONResponse: Response with status of process or details if something went wrong.
    """
    task_id = ObjectId(task_id)
    task_status = database.get_status_of_process(task_id)
    response = {"id": str(task_id), "status": task_status}
    if task_status is None:
         response['detail'] = 'Status for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.get("/get_bbox/{task_id}", response_model=Dict[str, List[Bbox]])
async def get_bbox(task_id: str) -> JSONResponse:
    """ Get all bboxes by ID of task.

    Args:
        task_id (str): Id of task.

    Returns:
        JSONResponse: Response with all bboxes of processed image or details if something went wrong.
    """
    task_id = ObjectId(task_id)
    bbox = database.get_bbox_of_process(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Bbox for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)
    
@app.get("/get_processed_image/{task_id}", response_model = Dict[str, ProcessedImage])
async def get_processed_image(task_id: str) -> JSONResponse:
    """ Get processed image with bboxes and confidence and also width, height and format of image.

    Args:
        task_id (str): Id of task.

    Returns:
        JSONResponse: Response with processed image or details if something went wrong.
    """
    task_id = ObjectId(task_id)
    image = database.get_processed_image(task_id)
    response = {'result': image}
    if image is None:
        response['detail'] = 'Processed image for such ID not found. Check the correctness of the ID or status.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)
# to decode and show image from db do:
# decoded_image = base64.b64decode(new_image_string)
# Image.open(io.BytesIO(decoded_image))

@app.get("/get_bbox_max/{task_id}", response_model=Dict[str, Bbox])
async def get_bbox_max(task_id: str) -> JSONResponse:
    """ Get bbox with max confidence.

    Args:
        task_id (str): Id of task.

    Returns:
        JSONResponse: Response with bbox with max confidence or details if something went wrong.
    """
    task_id = ObjectId(task_id)
    bbox = database.get_max_bbox(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Max bbox for such ID not found. Check the correctness of the ID or status.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.post("/send_image", response_model = Task)
async def task_processing(file: bytes = File(...)) -> JSONResponse:
    """ Recieve file, validate it, create object in database and start async task of detecting fire on image.

    Args:
        file (bytes, optional): File with fire for detecting it. Defaults to File(...).

    Returns:
        JSONResponse: Id of process.
    """
    file_type = magic.from_buffer(file, mime=True)
    if not file_type.startswith('image/'):
        raise HTTPException(status_code=400, detail={"taskId": None, "error": "Invalid file type. Supports only images"}) # check type of file
    
    if len(file) > config.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail={"taskId": None, "error": "Image file is too large"}) # check size of file
    
    task_id = database.create_object()
    async with semaphore:
        asyncio.create_task(process_image(file, model, task_id))

    response = {"taskId": str(task_id)}
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)