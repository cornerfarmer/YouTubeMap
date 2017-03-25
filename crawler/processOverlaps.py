import sys

import time

sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from peewee import *
from BaseModel import db
from Comment import Comment
from Channel import Channel
from Video import Video
from Overlap import Overlap

db.connect()
db.create_tables([Overlap], True)

index = 0
stepSize = 1000000
channelIds = {}
lastUserId = ""
t0 = time.time()
overlaps = {}
totalAmount = Comment.select().count()

ownViewers = {}

for i in range(int(totalAmount / stepSize) + 1):
    for comment in Comment.select(Comment.user_id, Channel.id).join(Video).join(Channel).offset(stepSize * i).limit(stepSize).order_by(Comment.user_id).dicts().iterator():
        #print("0 " + str(time.time() - t0))
        #t0 = time.time()
        if index % 100 == 0:
            print(index)

        if lastUserId != comment['user']:
            if lastUserId != "":

                channelIdsList = []
                for channelId, count in channelIds.items():
                    if count > 0:
                        channelIdsList.append(channelId)

                if len(channelIdsList) == 1:
                    if channelIdsList[0] in ownViewers:
                        ownViewers[channelIdsList[0]] += 1
                    else:
                        ownViewers[channelIdsList[0]] = 1

                for key, channel1 in enumerate(channelIdsList):
                    for channel2 in channelIdsList[(key + 1):]:

                        if channel1 > channel2:
                            channel1ToStore, channel2ToStore = channel2, channel1
                        else:
                            channel1ToStore, channel2ToStore = channel1, channel2

                        #print(str(channel1ToStore)  + "+" + str(channel2ToStore))

                        if not (channel1ToStore, channel2ToStore) in overlaps:
                            overlaps[(channel1ToStore, channel2ToStore)] = {'channel1': channel1ToStore, 'channel2': channel2ToStore, 'number': 1}
                        else:
                            overlaps[(channel1ToStore, channel2ToStore)]['number'] += 1

                        if not (channel2ToStore, channel1ToStore) in overlaps:
                            overlaps[(channel2ToStore, channel1ToStore)] = {'channel1': channel2ToStore, 'channel2': channel1ToStore, 'number': 1}
                        else:
                            overlaps[(channel2ToStore, channel1ToStore)]['number'] += 1

            lastUserId = comment['user']
            channelIds = {}
            #print("User: " + str(comment['user']))


        if comment['id'] in channelIds:
            channelIds[comment['id']] += 1
        else:
            channelIds[comment['id']] = 1
        #print("1 " + str(time.time() - t0))
        #t0 = time.time()
        index += 1

Channel.update(ownViewers=0).execute()
for channelId, number in ownViewers.items():
    Channel.update(ownViewers=number).where(Channel.id == channelId).execute()
Overlap.truncate_table()
Overlap.insert_many(overlaps.values()).execute()


