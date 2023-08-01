import base64
import io

import numpy as np
from PIL import Image
import torch

import my_utils.config as config
import my_utils.database as database

def get_model():
    """ Creates a yolov5 model instance.

    Returns:
        models.common.Autoshape: yolov5 model with custom fire weights.
    """
    try:
        model = torch.hub.load('./yolov5', 'custom', path='./models/best.pt', source='local')
        model.conf = config.MIN_TRESHHOLD
        model.iou = config.IOU
    except Exception as e:
        pass
    return model

def get_image_from_bytes(binary_image: bytes, max_size: int = 1024) -> Image.Image:
    """ Prepare image for yolov5 model.

    Args:
        binary_image (bytes): Image.
        max_size (int, optional): Max size if image. Defaults to 1024.

    Returns:
        Image.Image: Image for yolov5 model.
    """
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize((
        int(input_image.width * resize_factor),
        int(input_image.height * resize_factor)
    ))
    return resized_image

def get_processed_image_results(image: np.array) -> dict:
    """ Prepare for storing in database.

    Args:
        image (np.array): Image in np.array.

    Returns:
        dict: Image with params.
    """
    image = Image.fromarray(image)
    buff = io.BytesIO()
    image.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    processed_image_params = {'processedImage': new_image_string, 'width': image.width, 'height': image.height, 'format': 'base64'}
    return processed_image_params

async def process_image(file: bytes, model, task_id: str) -> None:
    """ Processing image using yolov5 model.

    Args:
        file (bytes): Image for processing.
        model (_type_): Model.
        task_id (str): Id of the task.
    """
    try:
        database.change_status(task_id, status='processing')
        input_image = get_image_from_bytes(file)
        results = model(input_image)
        detect_res = results.pandas().xywhn[0].reset_index().to_dict(orient="records") #TODO: speed up, pandas is slow
        detect_res = [{key:value for key,value in one_box.items() if key not in ['class', 'name']} for one_box in detect_res] # delete class and name field from res dict
        processed_image = results.render()[0]
        processed_image_params = get_processed_image_results(processed_image)
        max_confidence_bbox = max(detect_res, key=lambda x: x['confidence'])
        database.add_processing_results(task_id, detect_res, processed_image_params, max_confidence_bbox)
    except Exception as e:
        database.change_status(task_id, status='error')