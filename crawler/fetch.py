#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys


sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from apiclient.errors import HttpError
from peewee import *
from apiclient.discovery import build
from BaseModel import db, api_key
from Comment import Comment
from Channel import Channel
from Video import Video
from User import User
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("crawler_id", help="The id of the crawler to launch.", type=int)
args = parser.parse_args()

total_crawlers = 10

log_file = open("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/logs/"+ str(datetime.now()).replace(" ", "_") + "-" + str(args.crawler_id) + ".log","w", encoding='utf-8')
sys.stdout = log_file
print(sys.stdout.encoding)

print("Starting crawler " + str(args.crawler_id))

try:

    db.connect()
    db.create_tables([Channel, Video, Comment], True)

    service = build('youtube', 'v3', developerKey=api_key)

    for channel in Channel.select().where(fn.Mod(Channel.id, total_crawlers) == args.crawler_id):

        if channel.identifier is None:
            request = service.channels().list(part='id', forUsername=channel.name)
            results = request.execute()
            if len(results) > 0:
                channel.identifier = results['items'][0]['id']
                channel.save()

        if not channel.identifier is None and Video.select().where((Video.lastVisited >> None) & (Video.channel == channel)).count() == 0:
            print("Checking for new videos on channel " + channel.name)

            request = service.search().list(part='snippet', maxResults='50', channelId=channel.identifier, order="date", type="video", publishedAfter="2017-01-01T00:00:00Z", fields='items/id/videoId')
            results = request.execute()

            addedVideos = 0
            for item in results["items"]:
                videoId = item["id"]["videoId"]

                if Video.select().where(Video.identifier == videoId).count() == 0:
                    video = Video(identifier=videoId, channel=channel)
                    video.save(force_insert=True)
                    addedVideos += 1

            print("Found " + str(addedVideos) + " new Videos")

        video = None
        if Video.select().where((Video.lastVisited >> None) & (Video.channel == channel)).count() > 0:
            video = Video.select().where((Video.lastVisited >> None) & (Video.channel == channel)).get()
        elif Video.select().where(Video.channel == channel).count() > 0:
            video = Video.select().where(Video.channel == channel).order_by(Video.lastVisited.asc()).get()

        if not video is None:
            print("Adding comments for video " + video.identifier + " (" + channel.name  + ")")

            video.lastVisited = datetime.now()
            video.save()

            moreComments = True
            addedComments = 0
            results = {'nextPageToken': ''}

            existingCommentFound = False
            while moreComments:
                request = service.commentThreads().list(part='snippet', maxResults='100', videoId=video.identifier, pageToken=results['nextPageToken'], fields='items(id,snippet(topLevelComment(snippet(authorChannelId,publishedAt)))),nextPageToken')
                try:
                    results = request.execute()
                except HttpError as err:
                    print("Could not fetch comments." )
                    break

                comments = []

                if "items" in results:
                    for item in results["items"]:
                        if "authorChannelId" in item["snippet"]["topLevelComment"]["snippet"]:
                            user, created = User.get_or_create(identifier=item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"])

                            if Comment.select().where((Comment.user==user) & (Comment.video==video) & (Comment.publishedAt==item["snippet"]["topLevelComment"]["snippet"]["publishedAt"][:-5])).count() > 0:
                                existingCommentFound = True
                                break

                            comments.append(Comment(user=user, video=video, publishedAt=item["snippet"]["topLevelComment"]["snippet"]["publishedAt"][:-5]))

                for comment in comments:
                    try:
                        comment.save(force_insert=True)
                    except IntegrityError as err:
                        print("Duplicate Comment")

                moreComments = 'nextPageToken' in results and not existingCommentFound
                addedComments += len(comments)


            print("Added " + str(addedComments) + " Comments")

            hasAddedVideo = True
        log_file.flush()
except:
    db.close()
    raise

print("Finished!")

db.close()
log_file.close()


