
import sys


sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from apiclient.discovery import build
from BaseModel import db, api_key
from Comment import Comment
from User import User

db.connect()
db.create_tables([User, Comment], True)

service = build('youtube', 'v3', developerKey=api_key)
index = 0
stepSize = 1000000
totalAmount = Comment.select().count()


users = set()
for i in range(int(totalAmount / stepSize) + 1):
    for comment in Comment.select().offset(stepSize * i).limit(stepSize).iterator():


        if index % 100 == 0:
            print(index)

        users.add(comment.userId)

        index+=1

userList = []
for user in users:
    userList.append({'identifier': user})

User.truncate_table()
User.insert_many(userList).execute()

db.close()