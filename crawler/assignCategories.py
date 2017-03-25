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
from Category import Category
from ChannelCategory import ChannelCategory

db.connect()
db.create_tables([ChannelCategory], True)

service = build('youtube', 'v3', developerKey=api_key)

ChannelCategory.truncate_table()

for channel in Channel.select():

    existingChannels = Channel.select()

    request = service.channels().list(part='topicDetails', id=channel.identifier)
    results = request.execute()

    categories = []

    if "items" in results:
        for item in results["items"]:
            if "topicDetails" in item and "topicIds" in item["topicDetails"]:
                for topicId in item["topicDetails"]["topicIds"]:
                    if Category.select().where(Category.identifier == topicId).count() == 0:
                        print("No category found for: " + topicId + " (" + channel.name + ")")
                        exit()
                    categories.append(Category.select().where(Category.identifier == topicId))

    if len(categories) == 0:
        print("No categories found for " + channel.name)
        categories.append(Category.select().where(Category.name == "None"))

    for category in categories:
        if ChannelCategory.select().where((ChannelCategory.category==category) & (ChannelCategory.channel==channel)).count() == 0:
            channelCategory = ChannelCategory(category=category, channel=channel)
            channelCategory.save(force_insert=True)
            print(channelCategory.channel.name + " -> " + channelCategory.category.name)


db.close()