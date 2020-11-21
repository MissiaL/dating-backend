from uuid import uuid4

from peewee import CharField, SmallIntegerField, BooleanField, TextField, DateTimeField, ForeignKeyField, IntegerField, \
    BlobField, UUIDField

from app.database import BaseModel
from app.utils import now_in_utc


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    email = CharField(unique=True)
    password = CharField()
    firstname = CharField()
    lastname = CharField()
    age = SmallIntegerField()
    gender = CharField()
    height = SmallIntegerField()
    is_smoke = BooleanField()
    hobbies = TextField(null=True)
    created_at = DateTimeField(default=now_in_utc)

    class Meta:
        table_name = 'users'


class Cost(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, on_delete='CASCADE', backref='costs')
    name = TextField()
    price = IntegerField(default=0)
    created_at = DateTimeField(default=now_in_utc)

    class Meta:
        table_name = 'costs'


class Photo(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, on_delete='CASCADE', backref='photos')
    is_main = BooleanField()
    url = TextField()
    created_at = DateTimeField(default=now_in_utc)

    class Meta:
        table_name = 'photos'


class Action(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, on_delete='CASCADE', backref='actions')
    like_to_user = ForeignKeyField(User, backref='actions', null=True)
    dislike_to_user = ForeignKeyField(User, backref='actions', null=True)
    created_at = DateTimeField(default=now_in_utc)

    class Meta:
        table_name = 'actions'


class Message(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, on_delete='CASCADE', backref='actions')
    to_user = ForeignKeyField(User, backref='actions')
    text = TextField()
    created_at = DateTimeField(default=now_in_utc)

    class Meta:
        table_name = 'messages'
