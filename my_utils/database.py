from my_utils.config import *

def create_object(process_id, image):
    MYCOL.insert_one({
        'processId': process_id,
        'originalImage': image,
        'status': 'queue',
        })

def change_status(process_id, status='processing'):
    MYCOL.update_one({"processId": process_id}, {'$set' : {'status' : status}}, upsert=True)


def add_processsing_results(process_id, results):
    change_status(process_id, status='done')
    MYCOL.update_one(
        {'processId': process_id},
        {"$set": {'result': results}})

def get_status_of_process(process_id):
    status = list(MYCOL.find({'processId': process_id}, {'_id': 0, 'status': 1}))[0]['status']
    return status

def get_bbox_of_process(process_id):
    pass

def get_max_bbox(process_id):
    pass

def get_picture(process_id):
    image = list(MYCOL.find({'processId': process_id}, {'_id': 0, 'originalImage': 1}))[0]['originalImage']
    return image    

