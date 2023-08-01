import unittest
import os
from fastapi.testclient import TestClient
from main import app

class TestsGetStatus(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)  
            
    def test_send_image_jpg_success(self):
        files = {
            'file': open(os.path.join('tests', 'test_data', 'ok_image.jpg'), 'rb'),
        }        
        response = self.client.post('http://0.0.0.0:8000/send_image', files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1) # len is 1 because result should be {'task_id': 'some value'}
        files['file'].close()
        
    def test_send_image_png_success(self):
        files = {
            'file': open(os.path.join('tests', 'test_data', 'ok_image_2.png'), 'rb'),
        }        
        response = self.client.post('http://0.0.0.0:8000/send_image', files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1) # len is 1 because result should be {'task_id': 'some value'}
        files['file'].close()

    def test_send_image_not_image_fail(self):
        files = {
            'file': open(os.path.join('tests', 'test_data', 'not_image.ipynb'), 'rb'),
        }        
        response = self.client.post('http://0.0.0.0:8000/send_image', files=files)
        excepted_data = {'detail': {'taskId': None, 'error': 'Invalid file type. Supports only images'}}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), excepted_data)
        files['file'].close()
        
    def test_send_image_large_image_fail(self):
        files = {
            'file': open(os.path.join('tests', 'test_data', 'large_image.jpg'), 'rb'),
        }        
        response = self.client.post('http://0.0.0.0:8000/send_image', files=files)
        excepted_data = {'detail': {'taskId': None, 'error': 'Image file is too large'}}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), excepted_data)  
        files['file'].close()     
    

if __name__ == '__main__':
    unittest.main()