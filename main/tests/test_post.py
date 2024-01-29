from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ReactionTestFactory, UserTestFactory
from main.tests.factories import PostTestFactory
from main.models import Post, Reaction


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
            "content": (post.content[:125]+"..." if len(post.content) > 128 else post.content),
            "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.assertDictEqual(response.data["results"][0], expected_data)

    def test_retrieve_structure_reaction_negative(self):
        post = PostTestFactory()

        response = self.client.get(path=f"{self.url}{post.pk}/", format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["self_reaction"], "")

    def test_retrieve_structure_reaction(self):
        post = PostTestFactory()
        author = post.author
        reaction = ReactionTestFactory(author=author, post=post, value=Reaction.Values.HEART)         

        response = self.client.get(path=f"{self.url}{post.pk}/", format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "author": {
                "username": author.username,
                "first_name": author.first_name,
                "last_name": author.last_name,
            },
            "title": post.title,
            "content": post.content,
            "comments": [],
            "self_reaction": "",
            "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }        
        self.assertDictEqual(response.data, expected_data)

    def test_update_self_post(self):
        post = PostTestFactory(
            author=self.user,
            title="test",
            content="test_content",
        )

        updated_data = {
            "title": "test_updated",
            "content": "test_content_updated",
        }

        response = self.client.patch(
            path=f"{self.url}{post.pk}/",
            data=updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_data["title"])
        self.assertEqual(response.data["content"], updated_data["content"])

        post.refresh_from_db()
        self.assertEqual(post.title, updated_data["title"])
        self.assertEqual(post.content, updated_data["content"])

    def test_update_post_negative(self):       
        post = PostTestFactory(            
            title="test",
            content="test_content",
        )

        updated_data = {
            "title": "test_updated",
            "content": "test_content_updated",
        }

        response = self.client.patch(
            path=f"{self.url}{post.pk}/",
            data=updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(post.title, updated_data["title"])
        self.assertNotEqual(post.content, updated_data["content"])

    def test_update_self_post_with_put(self):
        post = PostTestFactory(
            author=self.user,
            title="test",
            content="test_content",
        )

        updated_data = {
            "title": "test_updated",
            "content": "test_content_updated",
        }

        response = self.client.put(
            path=f"{self.url}{post.pk}/",
            data=updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_data["title"])
        self.assertEqual(response.data["content"], updated_data["content"])

        post.refresh_from_db()
        self.assertEqual(post.title, updated_data["title"])
        self.assertEqual(post.content, updated_data["content"])

    def test_update_post_negative_with_put(self):       
        post = PostTestFactory(            
            title="test",
            content="test_content",
        )

        updated_data = {
            "title": "test_updated",
            "content": "test_content_updated",
        }

        response = self.client.put(
            path=f"{self.url}{post.pk}/",
            data=updated_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(post.title, updated_data["title"])
        self.assertNotEqual(post.content, updated_data["content"])

    def test_delete_self_post(self):
        post = PostTestFactory(
            author=self.user,
            title="test",
            content="test_content",
        )

        response = self.client.delete(
            path=f"{self.url}{post.pk}/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)
    
    def test_delete_other_post(self):
        post = PostTestFactory(            
            title="test",
            content="test_content",
        )

        response = self.client.delete(
            path=f"{self.url}{post.pk}/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.all().count(), 1)
