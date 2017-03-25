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

import requests
from BaseModel import db
from Category import Category
from bs4 import BeautifulSoup

db.connect()
db.create_tables([Category], True)

html = requests.get("https://developers.google.com/youtube/v3/docs/search/list").text

Category.truncate_table()
category = Category(identifier="/m/000000", name="None", isSuper=True)
category.save(force_insert=True)

soup = BeautifulSoup(html, "html5lib")
rows = soup.find(None, {"id": "supported-topic-ids"}).find("table", {"class": "responsive"}).findAll("tr")
for row in rows:
    tds = row.findAll("td")

    if len(tds) > 1:
        name = tds[1].text
        isSuper = False
        if name.find(" (parent topic)") != -1:
            name = name.replace(" (parent topic)", "")
            isSuper = True
        category = Category(identifier=tds[0].text, name=name, isSuper=isSuper)
        category.save(force_insert=True)
        print(category.identifier + " -> " + category.name + " (" + str(category.isSuper) + ")")


db.close()