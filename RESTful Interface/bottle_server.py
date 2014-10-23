#!/usr/bin/env python
"""
Server for the RESTful interface to the MongoDB database
of tweets for the Healthcare Twitter Analysis project.

    e:
    cd "E:\HTA\RESTful Interface"
    python bottle_server.py
"""

import pymongo, bottle
from bottle import error, route, get, post, static_file, request, abort, response
import cgi, re, os, json
from urlparse import parse_qsl
import bson.json_util

PATH           = os.path.dirname(__file__)

__author__     = 'George Fisher'
__copyright__  = "Copyright 2014, George Fisher Advisors LLC"
__credits__    = ["George Fisher"]
__license__    = "MIT"
__version__    = "0.1.0"
__maintainer__ = "George Fisher"
__email__      = "george@georgefisher.com"
__status__     = "Prototype"

# for relative addressing
# =======================
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
@route('/js/:path#.+#', name='js')
def static(path):
    return static_file(path, root='js')
    
@route('/css/:path#.+#', name='css')
def static(path):
    return static_file(path, root='css')
    
@route('/img/:path#.+#', name='img')
def static(path):
    return static_file(path, root='img')
    
@route('/data/:path#.+#', name='data')
def data(path):
    return static_file(path, root='data')
    
# Error messages
# ==============
@error(404)
def error404(error):
    return "404 error: file not found %s"%error
    
# RESTful interface
# =================
"""
           url                           | verb   | action                                      | response                                    |
-----------------------------------------+--------+---------------------------------------------+---------------------------------------------+
http://localhost:8082/query/limit        | POST   | send in a query                             | a list of ids meeting the criteria, plus    |
                                                                                                |   the number of items in the list, and      |
                                                                                                |   the first full tweet meeting the criteria |
http://localhost:8082/findOne/id         | GET    | retrieve a single tweet by id               | a single tweet in json format               |       
http://localhost:8082/find/id_list       | GET    | retrieve a list of tweets for a list of ids | a list of tweets                            |
    
"""    
@route('/query/<limit>', method="POST")
def query(limit): 
    data = request.json;
    
    # execute the MongoDB query, returning a list of the _id's that match
    if int(limit) <= 0: 
        id_list = [tweet for tweet in tweets.find(data,dict({"_id":1}))]
    else: 
        id_list = [tweet for tweet in tweets.find(data,dict({"_id":1})).limit(int(limit))]
        
    # how long is the list?
    num = len(id_list)
        
    # also include the first result
    example = tweets.find_one(data)
        
    # create the structure to return
    result            = dict()
    result['num']     = num
    result['id_list'] = id_list
    result['example'] = example
    
    # convert from MongoDB json to strict json and return the result
    result = bson.json_util.dumps(result)
    return result

# Send HTML pages
# ===============
@route('/')
def index():
    return static_file('HTAinterface.html', root=PATH)
    
@route('/:path#.+#', name='root')
def static(path):
    return static_file(path, root=PATH)
    
    
# Shutdown the MongoDB connection
# ===============================
@route('/exit')
def exit():
    connection.disconnect()
    return "MongoDB shut down"


connection_string = "mongodb://localhost"
connection        = pymongo.MongoClient(connection_string)

db     = connection.HTA
tweets = db.grf

# for production use: remove bottle.debug entirely and remove , reloader=True from bottle.run
bottle.debug(True)
bottle.run(host='localhost', port=8082, reloader=True)