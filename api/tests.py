from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ChatbotResponseViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('chatbot-response')  

    def test_post_missing_query(self):
        """Test that a missing query returns a 400 Bad Request."""
        response = self.client.post(self.url, {})  # Sending an empty body
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Query is required."})  