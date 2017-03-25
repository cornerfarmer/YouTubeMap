from peewee import *

from BaseModel import BaseModel
from Channel import Channel


class Overlap(BaseModel):
    channel1 = ForeignKeyField(Channel, related_name="overlap_set2")
    channel2 = ForeignKeyField(Channel, related_name="overlap_set1")
    number = IntegerField(default=0)

    class Meta:
        primary_key = CompositeKey('channel1', 'channel2')
