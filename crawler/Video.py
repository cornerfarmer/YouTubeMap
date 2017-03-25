from Channel import Channel
from peewee import *

from BaseModel import BaseModel

class Video(BaseModel):
    identifier = CharField()
    channel = ForeignKeyField(Channel)
    lastVisited = DateTimeField(null=True)

