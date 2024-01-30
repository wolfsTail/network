from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ReactionTestFactory, UserTestFactory
from main.tests.factories import PostTestFactory
from main.models import Post, Reaction


class ReactionTestCase(APITestCase):
    def setUp(self):
        self.user = UserTestFactory()
        self.client.force_authenticate(user=self.user)
        self.post = PostTestFactory(author=self.user) 
        self.url = "/api/reactions/"

    def test_create_reaction(self):
        data = {
            "post": self.post.pk,
            "value": Reaction.Values.HEART,
        }         

        response = self.client.post(path=f"{self.url}", data=data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reaction = Reaction.objects.last()

        self.assertEqual(reaction.author, self.user)
        self.assertEqual(reaction.post, self.post)
        self.assertEqual(reaction.value, data["value"])
    
    def test_change_over_reaction(self):
        reaction = ReactionTestFactory(
            author=self.user,
            post=self.post,
            value=Reaction.Values.HEART,
        )

        data = {
            "post": self.post.pk,
            "value": Reaction.Values.LAUGH,
        }         

        response = self.client.post(path=f"{self.url}", data=data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reaction.refresh_from_db()
        self.assertEqual(reaction.value, data["value"])
    
    def test_set_reaction_to_null(self):
        reaction = ReactionTestFactory(
            author=self.user,
            post=self.post,
            value=Reaction.Values.HEART,
        )

        data = {
            "post": self.post.pk,
            "value": Reaction.Values.HEART,
        }         

        response = self.client.post(path=f"{self.url}", data=data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reaction.refresh_from_db()
        self.assertEqual(reaction.value, None)
    
    def test_set_reaction_from_incorect_value(self):
        reaction = ReactionTestFactory(
            author=self.user,
            post=self.post,
            value=Reaction.Values.HEART,
        )

        data = {
            "post": self.post.pk,
            "value": "LOL",
        }         

        response = self.client.post(path=f"{self.url}", data=data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reaction.objects.count(), 1)


