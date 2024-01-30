from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ChatTestFactory, MessageTestFactory
from main.tests.factories import PostTestFactory
from users.tests.factories import UserTestFactory
from communication.models import Chat, Message


class ChatTestCase(APITestCase):
    def setUp(self):
        self.user = UserTestFactory()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/chats/"

    def test_create_chat(self):
        user = UserTestFactory()
        data = {"user_2": user.pk}

        response = self.client.post(
            self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chat = Chat.objects.last()
        self.assertEqual(chat.user_1, self.user)
        self.assertEqual(chat.user_2, user)
    
    def test_try_to_create_chat_when_exists(self):
        user = UserTestFactory()
        chat = ChatTestFactory(user_1=self.user, user_2=user)
        data = {"user_2": user.pk}

        response = self.client.post(
            self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chats = Chat.objects.all()
        self.assertEqual(chats.count(), 1)
    
    def test_try_to_create_chat_when_exists_reversed(self):
        user = UserTestFactory()
        chat = ChatTestFactory(user_1=user, user_2=self.user)
        data = {"user_2": user.pk}

        response = self.client.post(
            self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chats = Chat.objects.all()
        self.assertEqual(chats.count(), 1)
        
        chat = Chat.objects.last()
        self.assertEqual(chat.user_1, user)
        self.assertEqual(chat.user_2, self.user)
    
    def test_delete_chat(self):
        chat_1 = ChatTestFactory(user_1=self.user)
        chat_2 = ChatTestFactory(user_2=self.user)

        MessageTestFactory(author=self.user, chat=chat_1)
        MessageTestFactory(author=self.user, chat=chat_2)

        response = self.client.delete(f"{self.url}{chat_1.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(f"{self.url}{chat_2.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Chat.objects.all().count(), 0)
        self.assertEqual(Message.objects.all().count(), 0)    

    def test_try_to_delete_other_chat(self):
        chat = ChatTestFactory()

        response = self.client.delete(f"{self.url}{chat.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Chat.objects.all().count(), 1)
