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
import requests
from bs4 import BeautifulSoup
from BaseModel import db, api_key
from Channel import Channel

db.connect()
db.create_tables([Channel], True)

service = build('youtube', 'v3', developerKey=api_key)

links = [
    "https://socialblade.com/youtube/top/country/de",
"https://socialblade.com/youtube/top/country/de/mostsubscribed",
"https://socialblade.com/youtube/top/country/de/mostviewed"
]

for link in links:

    existingChannels = Channel.select()

    html = requests.get(link).text

    """If you do not want to use requests then you can use the following code below
       with urllib (the snippet above). It should not cause any issue."""
    soup = BeautifulSoup(html, "html5lib")
    res = soup.find("div", {"id": "BodyContainer"}).find("div", {"class": "UserSummaryWrap"}).find("div", {"style": "width: 800px; color:#333;"}).findAll("div", {"class": "TableMonthlyStats"})
    for r in res[2::5]:
        request = service.channels().list(part="statistics", forUsername=r.find('a')['href'].rsplit('/', 1)[-1])
        resultsSubs = request.execute()

        print(r.find('a')['href'].rsplit('/', 1)[-1])

        for itemSubs in resultsSubs["items"]:
            if not any(existingChannel.identifier == itemSubs["id"] for existingChannel in existingChannels):
                if int(itemSubs["statistics"]["subscriberCount"]) > 200000:
                    newChannel = Channel(identifier=itemSubs["id"], name=r.find('a').text)
                    newChannel.save()

