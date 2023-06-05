import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, Tracer!</p>")
    
    #TEST UPDATE        
    def test_update_agent(self):
        agent_id = 5  # ID of the agent to update
        data = {
            "agent_name": "John Doe",
            "work_area": "New York",
            "phone_no": "1234567890",
            "country": "USA"
        }
        response = self.app.put(f"/agents/{agent_id}", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("agent updated successfully" in response.data.decode())
        # Add additional assertions if needed
        
        
            
if __name__ == "__main__":
    unittest.main()