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

from apiclient.discovery import build
from BaseModel import db, api_key
from Channel import Channel

db.connect()
db.create_tables([Channel], True)

service = build('youtube', 'v3', developerKey=api_key)


for channel in Channel.select().where(Channel.viewedFeaturedChannels==0):
    print("Searching in featured channels of " + channel.name)

    existingChannels = Channel.select()

    request = service.channels().list(part='brandingSettings', id=channel.identifier)
    results = request.execute()

    ids = ""

    for item in results["items"]:
        if "featuredChannelsUrls" in item["brandingSettings"]["channel"]:
            for newId in item["brandingSettings"]["channel"]["featuredChannelsUrls"]:
                ids += newId + ','

    request = service.channels().list(part="snippet", id=ids)
    results = request.execute()

    request = service.channels().list(part="statistics", id=ids)
    resultsSubs = request.execute()

    for item in results["items"]:
        if not any(existingChannel.identifier == item["id"] for existingChannel in existingChannels):
            output = item["snippet"]["title"]
            allow = False

            if "country" in item["snippet"]:
                if item["snippet"]["country"] == "DE":
                    allow = True

            if "defaultLanguage" in item["snippet"]:
                if item["snippet"]["defaultLanguage"] == "de":
                    allow = True

            if not allow:
                continue

            allow = False
            for itemSubs in resultsSubs["items"]:
                if itemSubs["id"] == item["id"]:
                    if int(itemSubs["statistics"]["subscriberCount"]) > 200000:
                        allow = True
                        output += ", " + itemSubs["statistics"]["subscriberCount"]
            if allow:
                print(output)
                newChannel = Channel(identifier=item["id"], name=item["snippet"]["title"])
                newChannel.save()
    channel.viewedFeaturedChannels = 1
    channel.save()


db.close()