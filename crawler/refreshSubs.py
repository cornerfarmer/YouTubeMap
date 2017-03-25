
import sys

sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from apiclient.discovery import build
from BaseModel import db, api_key
from Channel import Channel

db.connect()
db.create_tables([Channel], True)

service = build('youtube', 'v3', developerKey=api_key)

for channel in Channel.select():

    request = service.channels().list(part='statistics', id=channel.identifier)
    results = request.execute()

    for item in results["items"]:
        channel.subscriber = int(item['statistics']['subscriberCount'])
        channel.save()
        print(channel.name + " -> " + str(channel.subscriber))


db.close()