from fastapi import FastAPI, File, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import magic
from my_utils.model import get_model, process_image, TTL
import uuid
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import my_utils.database as database
from my_utils.data_models import *
from typing import Dict, List
from my_utils.database import set_ttl_index
from my_utils.config import MAX_IMAGE_SIZE

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

@app.get("/get_status/{task_id}", response_model = Status)
async def get_status(task_id: str) -> JSONResponse:
    """ Get status of task

    Args:
        task_id (str): Id of task

    Returns:
        JSONResponse: Response with status of process or details if something went wrong
    """
    task_status = database.get_status_of_process(task_id)
    response = {"id": task_id, "status": task_status}
    if task_status is None:
         response['detail'] = 'Status for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.get("/get_bbox/{task_id}", response_model=Dict[str, List[Bbox]])
async def get_bbox(task_id: str) -> JSONResponse:
    """ Get all bboxes by ID of task

    Args:
        task_id (str): Id of task

    Returns:
        JSONResponse: Response with all bboxes of processed image or details if something went wrong
    """
    bbox = database.get_bbox_of_process(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Bbox for such ID not found. Check the correctness of the ID.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)
    
@app.get("/get_processed_image/{task_id}", response_model = Dict[str, ProcessedImage])
async def get_processed_image(task_id: str) -> JSONResponse:
    """ Get processed image with bboxes and confidence and also width, height and format of image

    Args:
        task_id (str): Id of task

    Returns:
        JSONResponse: Response with processed image or details if something went wrong
    """
    image = database.get_processed_image(task_id)
    response = {'result': image}
    if image is None:
        response['detail'] = 'Processed image for such ID not found. Check the correctness of the ID or status.'
    return response
# to decode and show image from db do:
# decoded_image = base64.b64decode(new_image_string)
# Image.open(io.BytesIO(decoded_image))

@app.get("/get_bbox_max/{task_id}", response_model=Dict[str, Bbox])
async def get_bbox_max(task_id: str) -> JSONResponse:
    """ Get bbox with max confidence

    Args:
        task_id (str): Id of task

    Returns:
        JSONResponse: Response with bbox with max confidence or details if something went wrong
    """
    bbox = database.get_max_bbox(task_id)
    response = {'bbox': bbox}
    if bbox is None:
        response['detail'] = 'Max bbox for such ID not found. Check the correctness of the ID or status.'
    return JSONResponse(content=jsonable_encoder(response), status_code = status.HTTP_200_OK)

@app.post("/send_image", response_model = Task)
async def task_processing(file: bytes = File(...)) -> JSONResponse:
    """ Recieve file, validate it, create object in database and start async task of detecting fire on image

    Args:
        file (bytes, optional): File with fire for detecting it. Defaults to File(...).

    Returns:
        JSONResponse: Id of process
    """
    # TODO: add task to queue and update status: in queue (DB)
    # TODO: add image validation process
    file_type = magic.from_buffer(file, mime=True)
    if not file_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Supports only images") # check type of file
    
    if len(file) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image file is too large") # check size of file
    
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