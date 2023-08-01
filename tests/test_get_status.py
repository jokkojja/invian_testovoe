import unittest
from fastapi.testclient import TestClient
from main import app


class TestsGetStatus(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
                
    def test_get_status_success(self):
        task_id = "253e5464-3a7c-40db-ad05-515d055d60a7"
        response = self.client.get(f"/get_status/{task_id}")
        excepted_data = {"id": task_id, "status": "completed"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)

    def test_get_status_not_found(self):
        task_id = "abc123"
        response = self.client.get(f"/get_status/{task_id}")
        excepted_data = {"id": task_id, "status": None, "detail": "Status for such ID not found. Check the correctness of the ID."}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), excepted_data)
    

if __name__ == '__main__':
    unittest.main()