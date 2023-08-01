from my_utils.config import *
import datetime


def set_ttl_index(seconds: str) -> None:
    try:
        ttl_index = MYCOL.index_information()['createdAt_1']
        MYCOL.drop_index('createdAt_1') # if index already exists then make reindex
    except KeyError: # if index doesn't exist create new index
        pass
    MYCOL.create_index("createdAt", expireAfterSeconds=seconds)
    
def create_object(task_id: str) -> None:
    MYCOL.insert_one({
        'processId': task_id,
        'status': 'queue',
        'processedImage': {},
        'createdAt': datetime.datetime.utcnow()
        })

def change_status(task_id: str, status: str = 'processing') -> None:
    MYCOL.update_one({"processId": task_id}, {'$set' : {'status' : status}}, upsert=True)


def add_processsing_results(task_id: str, results: list, 
                            process_image_params: dict, max_confidence_bbox: dict) -> None:
    change_status(task_id, status='completed')
    MYCOL.update_one(
        {'processId': task_id},
        {"$set": {'processedImage': process_image_params, 'result': results,
                  'maxBbox': max_confidence_bbox}})

def get_status_of_process(task_id: str) -> str:
    try:
        status = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'status': 1}))[0]['status']
    except (IndexError, KeyError):
        status = None
    return status

def get_bbox_of_process(task_id: str) -> list:
    try:
        bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'result': 1}))[0]['result']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_max_bbox(task_id: str) -> dict:
    try:
        bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'maxBbox': 1}))[0]['maxBbox']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_processed_image(task_id: str) -> bytes:
    try:
        image = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'processedImage': 1}))[0]['processedImage']
    except (IndexError, KeyError):
        image = None
    return image    

