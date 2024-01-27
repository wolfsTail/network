import factory
from factory.django import DjangoModelFactory

from main.models import Post, Comment, Reaction
from users.tests.factories import UserTestFactory


class PostTestFactory(DjangoModelFactory):
    author = factory.SubFactory(UserTestFactory)
    title = factory.Faker("word")
    content = factory.Faker("text")

    class Meta:
        model = Post


class CommentTestFactory(DjangoModelFactory):
    author = factory.SubFactory(UserTestFactory)
    post = factory.SubFactory(PostTestFactory)
    content = factory.Faker("text")

    class Meta:
        model = Comment


class ReactionTestFactory(DjangoModelFactory):
    author = factory.SubFactory(UserTestFactory)
    post = factory.SubFactory(PostTestFactory)
    value = Reaction.Values.HEART

    class Meta:
        model = Reaction