from rest_framework.test import APITestCase
from rest_framework import status

from .factories import CommentTestFactory, ReactionTestFactory, UserTestFactory
from main.tests.factories import PostTestFactory
from main.models import Post, Reaction, Comment


class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = UserTestFactory()
        self.client.force_authenticate(user=self.user)
        self.post = PostTestFactory()
        self.url = "/api/comments/"

    def test_create_comment(self):
        data = {
            "post": self.post.pk,
            "content": "test_comment",
        }

        response = self.client.post(path=self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.last()

        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.content, data["content"])
        self.assertIsNotNone(comment.created_at)
    
    def test_retrieve_comment_from_not_existing_post(self):
        data = {
            "post": self.post.pk + 10,
            "content": "test_comment",
        }
        response = self.client.post(path=self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_self_comment(self):
        comment = CommentTestFactory(
            author=self.user,
            post=self.post,
            content="test_comment",
        )

        response = self.client.delete(
            path=f"{self.url}{comment.pk}/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.all().count(), 0)
    
    def test_delete_other_comment(self):
        comment = CommentTestFactory()

        response = self.client.delete(
            path=f"{self.url}{comment.pk}/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.all().count(), 1)
    
    def test_comments_list_by_post(self):
        comments = CommentTestFactory.create_batch(10, post=self.post)

        CommentTestFactory.create_batch(5)

        url = f"{self.url}?post__id={self.post.pk}"

        response = self.client.get(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
    
    def test_comment_structure(self):
        comment = CommentTestFactory(post=self.post)

        url = f"{self.url}?post__id={self.post.pk}"

        response = self.client.get(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.last()
        expected_data = {
            "author": {
                "username": comment.author.username,
                "first_name": comment.author.first_name,
                "last_name": comment.author.last_name,
            },
            "post": comment.post.pk,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.assertEqual(response.data["results"][0], expected_data)
