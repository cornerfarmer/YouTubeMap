
import sys


sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from apiclient.discovery import build
from BaseModel import db, api_key
from Video import Video
from Comment import Comment

db.connect()
db.create_tables([Video], True)


# For this example, the API key is provided as a command-line argument.


service = build('youtube', 'v3', developerKey=api_key)

number = 0

for video in Video.select().iterator():
    if not video.lastVisited is None:
        if Comment.select().where(Comment.video_id == video.id).count() <= 50:
            print(video.identifier)
            video.lastVisited = None
            video.save()
            Comment.delete().where(Comment.video_id == video.id).execute()
            number += 1

print("Total videos: " + str(number))


db.close()