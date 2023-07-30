from my_utils.config import *

def create_object(task_id, image):
    MYCOL.insert_one({
        'processId': task_id,
        'originalImage': image,
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
    status = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'status': 1}))[0]['status']
    return status

def get_bbox_of_process(task_id):
    bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'result': 1}))[0]['result']
    return bbox

def get_max_bbox(task_id):
    bbox = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'maxBbox': 1}))[0]['maxBbox']
    return bbox

def get_picture(task_id):
    image = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'originalImage': 1}))[0]['originalImage']
    return image

def get_processed_image(task_id):
    image = list(MYCOL.find({'processId': task_id}, {'_id': 0, 'processedImage': 1}))[0]['processedImage']
    return image    

