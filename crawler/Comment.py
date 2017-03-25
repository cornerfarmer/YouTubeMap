from Video import Video
from User import User
from peewee import *

from BaseModel import BaseModel

class Comment(BaseModel):
    user = ForeignKeyField(User)
    video = ForeignKeyField(Video)
    publishedAt = DateTimeField()

    class Meta:
        primary_key = CompositeKey('user', 'video', 'publishedAt')