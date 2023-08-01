import torch
from PIL import Image
import io
import json
from my_utils.database import *
from my_utils.config import MIN_TRESHHOLD, IOU
import base64
import numpy as np

def get_model():
    """ Creates a yolov5 model instance

    Returns:
        models.common.Autoshape: yolov5 model with custom fire weights
    """
    try:
        model = torch.hub.load('./yolov5', 'custom', path='./models/best.pt', source='local')
        model.conf = MIN_TRESHHOLD
        model.iou = IOU
    except Exception as e:
        #TODO: process error
        pass
    return model

def get_image_from_bytes(binary_image: bytes, max_size: int = 1024) -> Image.Image:
    """_summary_

    Args:
        binary_image (bytes): _description_
        max_size (int, optional): _description_. Defaults to 1024.

    Returns:
        Image.Image: _description_
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
    """_summary_

    Args:
        image (np.array): _description_

    Returns:
        dict: _description_
    """
    image = Image.fromarray(image)
    buff = io.BytesIO()
    image.save(buff, format="JPEG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    processed_image_params = {'processedImage': new_image_string, 'width': image.width, 'height': image.height, 'format': 'base64'}
    return processed_image_params

async def process_image(file: bytes, model, task_id: str) -> None:
    """_summary_

    Args:
        file (bytes): _description_
        model (_type_): _description_
        task_id (str): _description_
    """
    try:
        input_image = get_image_from_bytes(file)
        results = model(input_image)
        detect_res = results.pandas().xywhn[0].reset_index().to_dict(orient="records") #TODO: speed up, pandas is slow
        detect_res = [{key:value for key,value in one_box.items() if key not in ['class', 'name']} for one_box in detect_res] # delete class and name field from res dict
        processed_image = results.render()[0]
        processed_image_params = get_processed_image_results(processed_image)
        max_confidence_bbox = max(detect_res, key=lambda x: x['confidence'])
        if detect_res == []:
            #TODO: Add processing of empty result
            pass
        else:
            pass
        add_processsing_results(task_id, detect_res, processed_image_params, max_confidence_bbox)
    except Exception as e:
        change_status(task_id, status='error')