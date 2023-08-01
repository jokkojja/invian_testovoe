import unittest
from fastapi.testclient import TestClient
from main import app

class TestsGetStatus(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)    
            
    def test_get_bbox_success(self):
        task_id = "253e5464-3a7c-40db-ad05-515d055d60a7"
        response = self.client.get(f"/get_bbox/{task_id}")
        excepted_data = {
                "bbox": [
                    {
                    "index": 0,
                    "xcenter": 0.8432590961456299,
                    "ycenter": 0.4610496163368225,
                    "width": 0.04637223482131958,
                    "height": 0.09011130779981613,
                    "confidence": 0.32195380330085754
                    },
                    {
                    "index": 1,
                    "xcenter": 0.06623463332653046,
                    "ycenter": 0.3004019856452942,
                    "width": 0.1324692666530609,
                    "height": 0.2746131122112274,
                    "confidence": 0.3147033452987671
                    },
                    {
                    "index": 2,
                    "xcenter": 0.6308906078338623,
                    "ycenter": 0.3786800801753998,
                    "width": 0.4489380717277527,
                    "height": 0.2510313093662262,
                    "confidence": 0.27342575788497925
                    }
                ]
            }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_bbox_not_found(self):
        task_id = "abc123"
        response = self.client.get(f"/get_bbox/{task_id}")
        excepted_data = {"bbox": None, "detail": "Bbox for such ID not found. Check the correctness of the ID."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()