from random import randint
from uuid import uuid4

import factory
from factory import DictFactory


from app.db_models import User, Cost, Action, Photo, Message
from .base import PeeweeModelFactory


class UserFactory(PeeweeModelFactory):
    email = factory.Faker('email')
    password = factory.Faker('password')
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    age = factory.Faker('pyint', max_value=100)
    gender = factory.Faker('random_element', elements=['male', 'female'])
    height = factory.Faker('pyint', min_value=100, max_value=200)
    is_smoke = factory.Faker('pybool')
    hobbies = factory.Faker('catch_phrase')

    class Meta:
        model = User


class CostFactory(PeeweeModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('catch_phrase')
    price = factory.Faker('pyint', max_value=100000)

    class Meta:
        model = Cost


class ActionFactory(PeeweeModelFactory):
    user = factory.SubFactory(UserFactory)
    like_to_user = factory.SubFactory(UserFactory)
    dislike_to_user = factory.SubFactory(UserFactory)

    class Meta:
        model = Action


class PhotoFactory(PeeweeModelFactory):
    user = factory.SubFactory(UserFactory)
    is_main = factory.Faker('pybool')
    url = factory.Faker('image_url')

    class Meta:
        model = Photo


class MessageFactory(PeeweeModelFactory):
    user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    text = factory.Faker('text')

    class Meta:
        model = Message
