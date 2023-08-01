import datetime
from typing import Union
import my_utils.config as config


def set_ttl_index(seconds: str) -> None:
    """ Set ttl index in database every time when API run.

    Args:
        seconds (str): Time to live in seconds.
    """
    try:
        ttl_index = config.MYCOL.index_information()['createdAt_1']
        config.MYCOL.drop_index('createdAt_1') # if index already exists then make reindex
    except KeyError: # if index doesn't exist create new index
        pass
    config.MYCOL.create_index("createdAt", expireAfterSeconds=config.TTL)
    
def create_object(task_id: str) -> None:
    """ Create document of task.

    Args:
        task_id (str): Id of task.
    """
    config.MYCOL.insert_one({
        'processId': task_id,
        'status': 'queue',
        'processedImage': {},
        'createdAt': datetime.datetime.utcnow()
        })

def change_status(task_id: str, status: str = 'processing') -> None:
    """ Change status of task.

    Args:
        task_id (str): Id of task.
        status (str, optional): Status of task. Defaults to 'processing'.
    """
    config.MYCOL.update_one({"processId": task_id}, 
                     {'$set' : {'status' : status}}, upsert=True)


def add_processing_results(task_id: str, results: list, 
                           process_image_params: dict, max_confidence_bbox: dict) -> None:
    """ Add results of image processing.

    Args:
        task_id (str): ID of the task.
        results (list): List of bounding boxes in the following format: 
                        [bbox_id, x_center, y_center, width, height, confidence] 
                        with relative coordinates [0, 1].
        process_image_params (dict): Image in base64 with shape and format.
        max_confidence_bbox (dict): Bounding box with the maximum confidence in the following format: 
                                    [bbox_id, x_center, y_center, width, height, confidence] 
                                    with relative coordinates [0, 1].
    """
    change_status(task_id, status='completed')
    config.MYCOL.update_one(
        {'processId': task_id},
        {"$set": {'processedImage': process_image_params, 'result': results,
                  'maxBbox': max_confidence_bbox}})

def get_status_of_process(task_id: str) -> Union[str, None]:
    """ Get status of process by task ID.

    Args:
        task_id (str): ID of the task.

    Returns:
        Union[str, None]: Status of process. If process not found -> None
    """
    try:
        status = list(config.MYCOL.find({'processId': task_id}, {'_id': 0, 'status': 1}))[0]['status']
    except (IndexError, KeyError):
        status = None
    return status

def get_bbox_of_process(task_id: str) -> Union[list, None]:
    """ Get bbox of process by task ID.

    Args:
        task_id (str): ID of the task.

    Returns:
        Union[list, None]: Bbox of process. If bbox not found -> None
    """
    try:
        bbox = list(config.MYCOL.find({'processId': task_id}, {'_id': 0, 'result': 1}))[0]['result']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_max_bbox(task_id: str) -> Union[dict, None]:
    """ Get bbox with max confidence by task ID.

    Args:
        task_id (str): ID of the task.

    Returns:
        Union[dict, None]: Bbox with max confidence. If bbox not found -> None
    """
    try:
        bbox = list(config.MYCOL.find({'processId': task_id}, {'_id': 0, 'maxBbox': 1}))[0]['maxBbox']
    except (IndexError, KeyError):
        bbox = None
    return bbox

def get_processed_image(task_id: str) -> Union[dict, None]:
    """ Get processed image with height, width, format.

    Args:
        task_id (str): ID of the task.

    Returns:
        Union[dict, None]: Bbox with params. If not found -> None
    """
    try:
        image = list(config.MYCOL.find({'processId': task_id}, {'_id': 0, 'processedImage': 1}))[0]['processedImage']
    except (IndexError, KeyError):
        image = None
    return image    

