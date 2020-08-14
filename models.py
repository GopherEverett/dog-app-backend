import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))

else:
    DATABASE = SqliteDatabase('dogs.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(unique=True)

    class Meta:
        database = DATABASE

class Dog(Model):
    name = CharField()
    owner = ForeignKeyField(User, backref='dogs')
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Dog], safe=True)
    print("Tables Created")
    DATABASE.close()