from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ChatTestFactory
from main.tests.factories import PostTestFactory
from users.tests.factories import UserTestFactory
from main.models import Post, Reaction, Comment


class ChatTestCase(APITestCase):
    ...