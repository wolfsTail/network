import factory
from factory.django import DjangoModelFactory
from users.models import User


class UserTestFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_staff = True

    class Meta:
        model = User
