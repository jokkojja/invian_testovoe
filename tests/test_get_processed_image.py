import os
import unittest

from bson import ObjectId
from fastapi.testclient import TestClient

from main import app

class TestsGetProcessedImage(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)  
        self.maxDiff = None
            
    def test_get_processed_image_success(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7fb")
        response = self.client.get(f"/get_processed_image/{task_id}")
        with open(os.path.join('tests', 'test_data', 'test_processed_image.txt'), 'r') as file:
            excepted_img = file.read()
        excepted_data = {'result': {'processedImage': excepted_img,  'width': 1024, 'height': 640, 'format': 'base64'}}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_processed_image_not_found(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7f1")
        response = self.client.get(f"/get_processed_image/{task_id}")
        excepted_data = {"result": None, "detail": "Processed image for such ID not found. Check the correctness of the ID or status."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()