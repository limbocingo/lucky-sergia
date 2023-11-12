"""
Models for LuckySergia API.

[version: v1]
[author: mrcingo]
"""
from random import choices
from string import ascii_letters, digits

from peewee import *

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(null=True)

    balance = IntegerField(default=100)

    password = CharField()
    sid = CharField(default=''.join(choices(ascii_letters + digits, k=64)))

    administrator = BooleanField(default=False)
