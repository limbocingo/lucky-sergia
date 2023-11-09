from peewee import *

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):  
    username = CharField(unique=True)
    password = CharField()
    balance = IntegerField(default=100)
