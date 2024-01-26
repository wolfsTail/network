import factory
from factory.django import DjangoModelFactory

from users.factories import UserTestFactory
from communication.models import Chat, Message


class ChatTestFactory(DjangoModelFactory):
    user_1 = factory.SubFactory(UserTestFactory)
    user_2 = factory.SubFactory(UserTestFactory)

    class Meta:
        model = Chat


class MessageTestFactory(DjangoModelFactory):
    author = factory.SubFactory(UserTestFactory)
    chat = factory.LazyAttribute(lambda obj: ChatTestFactory(user_1=obj.author))
    text = factory.Faker("text")

    class Meta:
        model = Message