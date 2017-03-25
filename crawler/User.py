from peewee import *

from BaseModel import BaseModel

class User(BaseModel):
    identifier = CharField(unique=True)

