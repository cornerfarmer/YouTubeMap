from peewee import *

from BaseModel import BaseModel
from Channel import Channel


class Edge(BaseModel):
    source = ForeignKeyField(Channel, related_name="edge_set1")
    target = ForeignKeyField(Channel, related_name="edge_set2")
    weight = FloatField()

    class Meta:
        primary_key = CompositeKey('source', 'target')
