import torch
from PIL import Image
import io
import json
from my_utils.database import *
from my_utils.config import MIN_TRESHHOLD

def get_model():
    try:
        model = torch.hub.load('./yolov5', 'custom', path='./models/best.pt', source='local')
        model.conf = MIN_TRESHHOLD
    except Exception as e:
        #TODO: process error
        pass
    return model

def get_image_from_bytes(binary_image, max_size=1024):
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize((
        int(input_image.width * resize_factor),
        int(input_image.height * resize_factor)
    ))
    return resized_image

async def process_image(file, model, task_id):
    try:
        input_image = get_image_from_bytes(file)
        results = model(input_image)
        #TODO: add valid values of bbox
        detect_res = results.pandas().xywhn[0].reset_index().to_dict(orient="records") #TODO: speed up, pandas is slow
        detect_res = [{key:value for key,value in one_box.items() if key not in ['class', 'name']} for one_box in detect_res] # delete class and name field from res dict
        processed_image = results.render()[0].tobytes()
        max_confidence_bbox = max(detect_res, key=lambda x: x['confidence'])
        if detect_res == []:
            #TODO: Add processing of empty result
            pass
        else:
            pass
        add_processsing_results(task_id, detect_res, processed_image, max_confidence_bbox)
    except Exception as e:
        #TODO: Process errors
        print(e)
        change_status(task_id, status='error')
        pass
    # update task: finished and coords of detecting