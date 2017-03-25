from peewee import *

from BaseModel import BaseModel

class Category(BaseModel):
    identifier = CharField(primary_key=True)
    name = CharField()
    isSuper = BooleanField(default=False)
