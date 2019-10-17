from peewee import *
from utils.util import get_full_path

db = SqliteDatabase(get_full_path('DB', 'discord.db'))


class ModelClass(Model):
    class Meta:
        database = db


class User(ModelClass):
    discord_id = CharField()
    steam_id = CharField()
    last_match = CharField()


db.connect()
db.create_tables([User])
