from peewee import *

from BaseModel import BaseModel
from Category import Category
from Channel import Channel


class ChannelCategory(BaseModel):
    channel = ForeignKeyField(Channel)
    category = ForeignKeyField(Category)

    class Meta:
        primary_key = CompositeKey('channel', 'category')
