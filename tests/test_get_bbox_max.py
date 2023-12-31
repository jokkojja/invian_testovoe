import unittest

from bson import ObjectId
from fastapi.testclient import TestClient

from main import app

class TestsGetBboxMax(unittest.TestCase):
        
    def setUp(self):
        self.client = TestClient(app)
        
    def test_get_bbox_max_success(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7fb")
        response = self.client.get(f"/get_bbox_max/{task_id}")
        excepted_data = {
                "bbox": {
                    "index": 0,
                    "xcenter": 0.043890222907066345,
                    "ycenter": 0.509705662727356,
                    "width": 0.06866306066513062,
                    "height": 0.11177687346935272,
                    "confidence": 0.31698957085609436
                }
            }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_bbox_max_not_found(self):
        task_id = ObjectId("64c8c3ec90784e7e767dc7f1")
        response = self.client.get(f"/get_bbox_max/{task_id}")
        excepted_data = {"bbox": None, "detail": "Max bbox for such ID not found. Check the correctness of the ID or status."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()