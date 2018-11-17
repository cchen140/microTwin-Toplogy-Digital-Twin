#!/usr/bin/env python
## -*- coding:utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import re
import os
import shutil
import time
from networkx_viewer import Viewer
import pymongo
from Host import Cnc
from ComponentEvent import EventType, CncEvent
from Device import Stopper, Robot
from link import Host_to_Device_Connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Net_Nodes = []  # The number of physical component in the plant
connectdict = {}  # Store all the connection relationship, key is the current node,
# and value is the list of node connected to current node
splitword = ':'
cachedict = {}  # Store all connection relationships of the error component
cncdict = {}  # Store all the CNCs in the plant, key is ssid, value is the cnc class
originfilename = 'net.txt'
filename = 'update_net.txt'

G = nx.DiGraph()

"""copy the file to another directory for updating without changing the initial topology file  """
if not os.path.isdir(filename):
    shutil.copyfile(originfilename, filename)

"""get Net_Nodes """
file1 = open(filename, 'r')
Node_count = len(file1.readlines())
file1.close()

"""connect to database """
client = pymongo.MongoClient()
db = client['sdcdb']
host_collection = db.mycollection
device_collection = db.mycollection1


def get_nodes(filename):
    """get all the connections"""
    file1 = open(filename, 'r')
    temp = []
    for i in range(0, Node_count):
        connectlist = []
        temp.append(file1.readline())
        index = [m.start() for m in re.finditer(splitword, temp[i])]
        Net_Nodes.append(temp[i][0:temp[i].find(' ')])

        for j in range(0, len(index)):
            if temp[i][index[j]:].find(' ') == -1:
                connectlist.append(temp[i][index[j] + 1:temp[i][index[j]:].find(' ')])

            else:
                connectlist.append(temp[i][index[j] + 1:index[j] + temp[i][index[j]:].find(' ')])
        connectdict.update({Net_Nodes[i]: connectlist})

    file1.close()
    return Net_Nodes


def net_node_add_to_graph(Net_Nodes):
    for i in range(0, Node_count):
        G.add_node(Net_Nodes[i])


def get_links():
    """add link to the graph"""
    node = connectdict.keys()
    for i in range(0, len(node)):
        connectlist = connectdict[node[i]]

        for j in range(0, len(connectlist)):
            G.add_edge(node[i], connectlist[j])


def remove_node(ssid):
    """remove the node from graph and store it in the cache for further process"""
    cachedict.update({ssid: connectdict[ssid]})
    Net_Nodes.remove(ssid)
    G.remove_node(ssid)


def remove_links(ssid):
    """remove all the links connected with the deleted node from graph"""
    for i in range(0, len(connectdict[ssid])):
        G.remove_edge(ssid, (connectdict[ssid])[i])


def draw_figure(pos):
    for i in range(0, Node_count):
        if (Net_Nodes[i][0] == 'H' or Net_Nodes[i][0] == 'h' or Net_Nodes[i][0] == 'C' or Net_Nodes[i][0] == 'c'):
            nx.draw_networkx_nodes(G, pos, nodelist=[Net_Nodes[i]], node_size=500, node_color='r', node_shape='s')

        if (Net_Nodes[i][0] == 'S' or Net_Nodes[i][0] == 's'):
            nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=[Net_Nodes[i]], node_color='b')

        if (Net_Nodes[i][0] == 'R' or Net_Nodes[i][0] == 'r'):
            nx.draw_networkx_nodes(G, pos, node_size=500, nodelist=[Net_Nodes[i]], node_color='g')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()


def draw_Gui():
    app = Viewer(G)
    app.mainloop()
    # code to edit graph
    app.canvas.refresh()


def recover_linknode(ssid):
    """add the node and link back to the graph when these component are recovered"""
    if (cachedict.has_key(ssid)):
        connectdict.update({ssid: cachedict[ssid]})
        del cachedict[ssid]
        Net_Nodes.append(ssid)
        G.add_node(ssid)

        for j in range(0, len(connectdict[ssid])):
            G.add_edge(ssid, connectdict[ssid][j])

    else:
        logger.error("cannot add the link")


def updateorcreate_cnc(Node_count):
    cnctotal = host_collection.find({"hosttype": "cnc"})
    for i in range(0, cnctotal.count()):
        if (cncdict.has_key(cnctotal[i]["ssid"])):
            """Update existed cnc with real-time data in the database"""
            hostlocation = []
            cnc = cncdict[cnctotal[i]["ssid"]]
            cnc.set_hearbeat(cnctotal[i]["heartbeat"])
            cnc.set_ipadd(cnctotal[i]["ipadd"])
            cnc.set_macadd(cnctotal[i]["macadd"])
            cnc.set_program(cnctotal[i]["program"])
            cnc.set_controlmode(cnctotal[i]["controlmode"])
            cnc.set_drivelist(cnctotal[i]["drivelist"])

            """Update location based on the manually defined file"""
            for j in range(0, len(connectdict[cnc.get_hostid()])):
                Host_to_Device_Connection(cnc.get_hostid(), connectdict[cnc.get_hostid()][j])
                hostlocation.append(Host_to_Device_Connection)

            cnc.set_hostlocation(hostlocation)
            CncEvent(EventType('update'), cnc.get_hostid(), time.time())

        else:
            """Creates a new cnc based on input and adds to the current cnc inventory"""
            get_nodes(filename)
            hostlocation = []

            for j in range(0, connectdict["ssid"].count()):
                Host_to_Device_Connection("ssid", connectdict["ssid"][j])
                hostlocation.append(Host_to_Device_Connection)

            cnc = Cnc(cnctotal[i]["ssid"], cnctotal[i]["ipadd"], cnctotal[i]["macadd"], cnctotal[i]["program"],
                      cnctotal[i]["heartbeat"], hostlocation, cnctotal[i]["drivelist"],
                      cnctotal[i]["controlmode"])
            cncdict.update(cnctotal[i]["ssid"], cnc)
            CncEvent(EventType('add'), cnc.get_hostid(), time.time())
            logger.info("new cnc %s is added", cnctotal[i]["ssid"])

        if ((cnc.get_heartbeat() == False) and (not (cachedict.has_key(cnc.get_hostid())))):
            """cnc is down and generate event ERROR"""
            logger.info("cnc %s is down", cnc.get_hostid())
            remove_links(cnc.get_hostid())
            remove_node(cnc.get_hostid())
            CncEvent(EventType('error'), cnc.get_hostid(), time.time())
            Node_count = Node_count - 1
            # add a timer here, if the cnc is not recovered and wait timed out, cnc will generate event remove

        if ((cachedict.has_key(cnc.get_hostid())) and (cnc.get_heartbeat() == True)):
            """cnc is recovered and generate event RECOVER"""
            logger.info("cnc %s is recovered", cnc.get_hostid())
            recover_linknode(cnc.get_hostid())
            CncEvent(EventType('recover'), cnc.get_hostid(), time.time())
            Node_count = Node_count + 1

    return Node_count


if (__name__ == '__main__'):
    # Initialize testbed layout
    get_nodes(filename)
    net_node_add_to_graph(Net_Nodes)
    get_links()
    pos = nx.spring_layout(G)
    draw_figure(pos)
    # app = Viewer(G) for gui

    # Instance devices and host
    post = host_collection.find()
    for i in range(0, post.count()):
        if (post[i]["hosttype"] == "cnc"):
            hostlocation = []
            for j in range(0, len(connectdict[post[i]["ssid"]])):
                Host_to_Device_Connection(post[i]["ssid"], connectdict[post[i]["ssid"]][j])
                hostlocation.append(Host_to_Device_Connection)

            cnc = Cnc(post[i]["ssid"], post[i]["ipadd"], post[i]["macadd"], post[i]["program"], post[i]["heartbeat"],
                      hostlocation, post[i]["drivelist"], post[i]["controlmode"])
            cncdict.update({post[i]["ssid"]: cnc})
            CncEvent(EventType('add'), cnc.get_hostid(), time.time())

    post = device_collection.find()
    for i in range(0, post.count()):
        if (post[i]["devicetype"] == "stopper"):
            stopper = Stopper(post[i]["ssid"], post[i]["state"], post[i]["heartbeat"])

        if (post[i]["devicetype"] == "robot"):
            robot = Robot(post[i]["ssid"], post[i]["state"], post[i]["heartbeat"], post[i]["program"])

    # Update based on the input (listener should be added in the future)
    time.sleep(5)
    Node_count = updateorcreate_cnc(Node_count)
    # app.canvas.refresh() for gui
    draw_figure(pos)

    # test of recovery
    host_collection.update_one({"heartbeat": False},
                               {"$set": {"heartbeat": True}})
    print(cachedict)
    print(Node_count)
    time.sleep(5)
    Node_count = updateorcreate_cnc(Node_count)
    draw_figure(pos)
    print(Node_count)
