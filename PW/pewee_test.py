from peewee import *

db = SqliteDatabase('discord.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    birthday = DateField()


class Pet(BaseModel):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()


db.connect()
db.create_tables([Person, Pet])