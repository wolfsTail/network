from rest_framework.test import APITestCase
from rest_framework import status

from .factories import UserTestFactory
from main.tests.factories import PostTestFactory
from users.models import User
from main.models import Post


class PostTestCase(APITestCase):
    def setUp(self):
        self.user = UserTestFactory()
        self.client.force_authenticate(user=self.user) 
        self.url = "/api/posts/"

    def test_post_list(self):
        PostTestFactory.create_batch(20)
             
        response = self.client.get(path=self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["count"], 20)
    
    def test_create_post(self):
        data = {
            "title": "test1",
            "content": "test1",
        }

        response = self.client.post(path=self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.last()

        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, data["title"])
        self.assertEqual(post.content, data["content"])
        self.assertIsNotNone(post.created_at)
    
    def test_create_post_negative(self):
        self.client.logout()

        data = {
            "title": "test1",
            "content": "test1",
        }

        response = self.client.post(path=self.url, data=data, format="json") 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_post_list_structure(self):
        post = PostTestFactory()

        response = self.client.get(path=self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        author = post.author
        expected_data = {
            "author": {
                "username": author.username,
                "first_name": author.first_name,
                "last_name": author.last_name,
            },
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.assertDictEqual(response.data["results"][0], expected_data)

