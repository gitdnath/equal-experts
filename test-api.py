import unittest
import requests

class TestWebServerAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8080"  # URL where your server is running

    def test_valid_user(self):
        """
        Test the API with a valid GitHub username.
        """
        username = "octocat123"
        response = requests.get(f"{self.BASE_URL}/{username}")

        # Validate the HTTP status code
        self.assertEqual(response.status_code, 200)

        # Validate the response structure
        response_json = response.json()
        self.assertIn("username", response_json)
        self.assertIn("gists", response_json)

        # Validate the username in the response
        self.assertEqual(response_json["username"], username)

        # Ensure gists list is returned
        self.assertIsInstance(response_json["gists"], list)

        # Check the structure of each gist in the list
        for gist in response_json["gists"]:
            self.assertIn("id", gist)
            self.assertIn("description", gist)
            self.assertIn("url", gist)

    def test_invalid_user(self):
        """
        Test the API with an invalid GitHub username.
        """
        username = "thisuserdoesnotexist12345"
        response = requests.get(f"{self.BASE_URL}/{username}")

        # Validate the HTTP status code for a non-existent user
        self.assertEqual(response.status_code, 404)

        # Validate the error response
        response_json = response.json()
        self.assertIn("error", response_json)
        self.assertEqual(response_json["error"], "User not found")

    def test_missing_user(self):
        """
        Test the API with a missing username (invalid endpoint).
        """
        response = requests.get(f"{self.BASE_URL}/")

        # Validate the HTTP status code for a missing username
        self.assertEqual(response.status_code, 404)

# Run the tests
if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
    #unittest.main()
