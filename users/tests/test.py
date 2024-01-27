from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.hashers import check_password

from main.tests.factories import PostTestFactory
from .factories import UserTestFactory
from users.models import User


class UsertestCase(APITestCase):

    def setUp(self):
        self.user = UserTestFactory()
        self.url = "/api/users/"      
   
    def test_users_list(self):
        UserTestFactory.create_batch(20)

        self.client.force_authenticate(user=self.user)        
        response = self.client.get(path=self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["count"], 21)
    
    def test_users_list_negative(self):
        
        response = self.client.get(path=self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_users_list_response(self):
        self.client.force_authenticate(user=self.user)        
        response = self.client.get(path=self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        expected_data = {            
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_friend": False,
            }
        
        self.assertDictEqual(response.data["results"][0], expected_data)
    
    def test_users_list_is_friend(self):
        self.client.force_authenticate(user=self.user)
        users = UserTestFactory.create_batch(5)

        self.user.friends.add(users[-1])
        self.user.save()

        with self.assertNumQueries(3):
            response = self.client.get(path=self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 6)
        self.assertTrue(response.data["results"][0]["is_friend"])
        for i in range(1, 6):
            self.assertFalse(response.data["results"][i]["is_friend"])

    def test_users_registration(self):
        data = {
            "username": "test",
            "password": "password",
            "first_name": "test",
            "last_name": "test",
            "email": "test@t.com"
            }

        response = self.client.post(path=self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.last()
        self.assertTrue(check_password(data['password'], created_user.password))

        data.pop("password")
        expected_data = {
            "username": created_user.username,
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
            "email": created_user.email,
        }

        self.assertDictEqual(data, expected_data)
    
    def test_users_registration_negative(self):
        data = {
            "username": self.user.username,
            "password": "password",
            "first_name": "test",
            "last_name": "test",
            "email": "test@t.com"
            }

        response = self.client.post(path=self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 1)
    
    def test_users_add_friend(self):
        self.client.force_authenticate(user=self.user)
        friend = UserTestFactory()        
        url = f"{self.url}{friend.pk}/add-friend/"

        response = self.client.post(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(friend in self.user.friends.all())

    def test_users_add_friend_repeat(self):
        self.client.force_authenticate(user=self.user)
        friend = UserTestFactory()        
        self.user.friends.add(friend)
        self.user.save()
        url = f"{self.url}{friend.pk}/add-friend/"

        response = self.client.post(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(friend in self.user.friends.all())

    def test_users_remove_friend(self):
        self.client.force_authenticate(user=self.user)
        friend = UserTestFactory()        
        self.user.friends.add(friend)
        self.user.save()
        url = f"{self.url}{friend.pk}/remove-friend/"

        response = self.client.post(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertFalse(friend in self.user.friends.all())
    
    def test_users_remove_friend_repeat(self):
        self.client.force_authenticate(user=self.user)
        friend = UserTestFactory()        
        url = f"{self.url}{friend.pk}/remove-friend/"

        response = self.client.post(path=url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertFalse(friend in self.user.friends.all())
    
    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.user)

        target_user = UserTestFactory()

        target_user.friends.add(self.user)
        target_user.friends.add(UserTestFactory())
        target_user.save()

        post_1 = PostTestFactory(author=target_user, title="test", content="test")
        post_2 = PostTestFactory(author=target_user, title="test1", content="test1")

        PostTestFactory.create_batch(10)

        response = self.client.get(
            path=f"{self.url}{target_user.pk}/", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "id": target_user.id,
            "username": target_user.username,
            "first_name": target_user.first_name,
            "last_name": target_user.last_name,
            "email": target_user.email,
            "is_friend": True,
            "qty_of_friends": 2,
            "posts": [
                {                    
                    "title": post_1.title,
                    "content": post_1.content,
                    "created_at": post_1.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                },
                {                    
                    "title": post_2.title,
                    "content": post_2.content,
                    "created_at": post_2.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            ]
        }
        self.assertDictEqual(response.data, expected_data)
    
    def test_get_user_friends(self):
        self.client.force_authenticate(user=self.user)

        target_user = UserTestFactory()
        friends = UserTestFactory.create_batch(3)

        target_user.friends.set(friends)        
        target_user.save()

        UserTestFactory.create_batch(3)

        response = self.client.get(
            path=f"{self.url}{target_user.pk}/friends/", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response.data["count"], 3)
    
    def test_get_user_friends_structure(self):
        self.client.force_authenticate(user=self.user)

        target_user = UserTestFactory()
        friends = UserTestFactory.create_batch(1)

        target_user.friends.set(friends)        
        target_user.save()        

        response = self.client.get(
            path=f"{self.url}{target_user.pk}/friends/", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data["results"]), 1)

        expected_data = {
            "username": friends[0].username,
            "first_name": friends[0].first_name,
            "last_name": friends[0].last_name,
            "is_friend": False,
        }
        self.assertDictEqual(dict(response.data["results"][0]), expected_data)

    def test_retrieve_self_profile(self):
        target_user = UserTestFactory()
        self.client.force_authenticate(user=target_user)

        target_user.friends.add(self.user)
        target_user.friends.add(UserTestFactory())
        target_user.save()

        post_1 = PostTestFactory(author=target_user, title="test", content="test")
        post_2 = PostTestFactory(author=target_user, title="test1", content="test1")

        PostTestFactory.create_batch(10)

        response = self.client.get(
            path=f"{self.url}me/", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "id": target_user.id,
            "username": target_user.username,
            "first_name": target_user.first_name,
            "last_name": target_user.last_name,
            "email": target_user.email,
            "qty_of_friends": 2,
            "posts": [
                {                    
                    "title": post_1.title,
                    "content": post_1.content,
                    "created_at": post_1.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                },
                {                    
                    "title": post_2.title,
                    "content": post_2.content,
                    "created_at": post_2.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            ]
        }
        self.assertDictEqual(response.data, expected_data)
