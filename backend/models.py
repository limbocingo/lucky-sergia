"""
Models for LuckySergia API.

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
    winrate = IntegerField(default=1)

    password = CharField()
    sid = CharField(default=''.join(choices(ascii_letters + digits, k=64)))

    logged = BooleanField(default=False)
    administrator = BooleanField(default=False)
