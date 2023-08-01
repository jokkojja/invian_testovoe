import unittest

from bson import ObjectId
from fastapi.testclient import TestClient

from main import app

class TestsGetBbox(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)    
            
    def test_get_bbox_success(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7fb")
        response = self.client.get(f"/get_bbox/{task_id}")
        excepted_data = {
                "bbox": [
                    {
                    "index": 0,
                    "xcenter": 0.043890222907066345,
                    "ycenter": 0.509705662727356,
                    "width": 0.06866306066513062,
                    "height": 0.11177687346935272,
                    "confidence": 0.31698957085609436
                    },
                    {
                    "index": 1,
                    "xcenter": 0.5942407846450806,
                    "ycenter": 0.4952731728553772,
                    "width": 0.07611769437789917,
                    "height": 0.1260623037815094,
                    "confidence": 0.26645925641059875
                    },
                ]
            }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_bbox_not_found(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7f1")
        response = self.client.get(f"/get_bbox/{task_id}")
        excepted_data = {"bbox": None, "detail": "Bbox for such ID not found. Check the correctness of the ID."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()