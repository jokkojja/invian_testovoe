import torch
from PIL import Image
import io
import json
from my_utils.database import *
from my_utils.config import MIN_TRESHHOLD

def get_model():
    model = torch.hub.load('./yolov5', 'custom', path='./models/best.pt', source='local')
    model.conf = MIN_TRESHHOLD
    return model

def get_image_from_bytes(binary_image, max_size=1024):
    input_image =Image.open(io.BytesIO(binary_image)).convert("RGB")
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize((
        int(input_image.width * resize_factor),
        int(input_image.height * resize_factor)
    ))
    return resized_image

async def process_image(file, model, task_id):
    input_image = get_image_from_bytes(file)
    results = model(input_image)
    #TODO: add valid values of bbox
    detect_res = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    detect_res = json.loads(detect_res)
    #TODO: Add processing of empty result
    print(detect_res)
    add_processsing_results(task_id, detect_res)
    # update task: finished and coords of detecting