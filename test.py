#!/usr/bin/env python
## -*- coding:utf-8 -*-
import re
import networkx as nx
import pymongo
from networkx_viewer import Viewer
import datetime
import json
from Host import Drive

Net_Nodes = []
connectdict = {}
splitword = ':'
cachedict = {}
filename = 'net.txt'
datafilename = 'data.txt'


file1 = open(filename, 'r')  # 以读取方式打开文件
Node_count = len(file1.readlines())  # 获得网络节点数
file1.close()

client = pymongo.MongoClient()
db = client['sdcdb']
hostcollection = db.mycollection
devicecollection = db.mycollection1
drive1 = Drive('work')
drive2 = Drive('idle')
drive3 = Drive('work')
drive4 = Drive('idle')


post = {"ssid": "c1",
        "ipadd": "10:10:10:10",
        "macadd": "00:00:00:00:00:00/1",
        "program": "slice",
        "heartbeat": True,
        "drivelist": "idle",
        "controlmode": "automatic",
        "hosttype": "cnc",
        "date": datetime.datetime.utcnow()}


post1={"ssid": "c2",
        "ipadd": "10:10:10:128",
        "macadd": "00:00:00:00:00:01/2",
        "program": "spin",
        "heartbeat": False,
        "drivelist": 'work',
        "controlmode": "automatic",
        "hosttype": "cnc",
        "date": datetime.datetime.utcnow()}

hostcollection.insert(post)
hostcollection.insert(post1)

post = {"ssid": "s1",
        "state": "ON",
        "heartbeat": True,
        "program": " ",
        "devicetype": "stopper",
        "date": datetime.datetime.utcnow()}

post1 = {"ssid": "r1",
        "state": "ON",
        "heartbeat": True,
        "program": "move to c1",
        "devicetype": "robot",
        "date": datetime.datetime.utcnow()}

devicecollection.insert(post)
devicecollection.insert(post1)
