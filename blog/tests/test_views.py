from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from blog.models import BookPost

class BookPostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
        self.post_data = {
            "title": "Test Book",
            "author": "Author Name",
            "content": "Book review",
            "rating": 4.5
        }

    def test_create_bookpost(self):
        response = self.client.post(reverse('bookpost-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookPost.objects.count(), 1)
        self.assertEqual(BookPost.objects.get().title, "Test Book")