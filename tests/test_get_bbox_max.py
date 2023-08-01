import unittest
from fastapi.testclient import TestClient
from main import app

class TestsGetBboxMax(unittest.TestCase):
        
    def setUp(self):
        self.client = TestClient(app)
        
    def test_get_bbox_max_success(self):
        task_id = "253e5464-3a7c-40db-ad05-515d055d60a7"
        response = self.client.get(f"/get_bbox_max/{task_id}")
        excepted_data = {
                "bbox": {
                    "index": 0,
                    "xcenter": 0.8432590961456299,
                    "ycenter": 0.4610496163368225,
                    "width": 0.04637223482131958,
                    "height": 0.09011130779981613,
                    "confidence": 0.32195380330085754
                }
            }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_bbox_max_not_found(self):
        task_id = "abc123"
        response = self.client.get(f"/get_bbox_max/{task_id}")
        excepted_data = {"bbox": None, "detail": "Max bbox for such ID not found. Check the correctness of the ID or status."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()