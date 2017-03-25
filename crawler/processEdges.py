
import sys


sys.path.append("/kunden/homepages/42/d584324863/htdocs/youtubemap/crawler/modules/")

from BaseModel import db
from Channel import Channel
from Edge import Edge
from Overlap import Overlap

db.connect()
db.create_tables([Edge], True)

totalAmount = db.execute_sql('SELECT id, users FROM userAmountPerChannel ORDER BY id').fetchall()

totalAmount = dict(totalAmount)

Edge.truncate_table()

for channel in Channel.select():
    print("Channel: " + channel.name)
    edges = []
    for overlap in Overlap.select().where(Overlap.channel1==channel).order_by(Overlap.number.desc()):
        edges.append(Edge(source=overlap.channel1, target=overlap.channel2, weight=(overlap.number / totalAmount[overlap.channel1.id] + overlap.number / totalAmount[overlap.channel2.id]) / 2))

    edges.sort(key=lambda x: x.weight, reverse=True)

    for edge in edges[:5]:
        edge.save(force_insert=True)



db.close()