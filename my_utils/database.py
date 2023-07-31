from my_utils.config import *

def create_object(task_id, image):
    MYCOL.insert_one({
        'processId': task_id,
        'status': 'queue',
        'processedImage': ''
        })

def change_status(task_id, status='processing'):
    MYCOL.update_one({"processId": task_id}, {'$set' : {'status' : status}}, upsert=True)


def add_processsing_results(task_id, results, processed_image, max_confidence_bbox):
    change_status(task_id, status='done')
    MYCOL.update_one(
        {'processId': task_id},
        {"$set": {'processedImage': processed_image, 'result': results,
                  'maxBbox': max_confidence_bbox}})

def get_status_of_process(task_id):
    try:
        status = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'status': 1}))[0]['status']
    except (IndexError, KeyError):
        status = None
    return status

def get_bbox_of_process(task_id):
    try:
        bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'result': 1}))[0]['result']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_max_bbox(task_id):
    try:
        bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'maxBbox': 1}))[0]['maxBbox']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_processed_image(task_id):
    try:
        image = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'processedImage': 1}))[0]['processedImage']
    except (IndexError, KeyError):
        image = None
    return image    

