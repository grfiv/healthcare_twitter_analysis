#!/usr/bin/env python
"""
Server for the RESTful interface to the MongoDB database
of tweets for the Healthcare Twitter Analysis project.
"""
import pymongo, bottle
from bottle import error, route, get, post, static_file, request, abort, response, template
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

# =======================
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
  
# ==============  
# Error messages
# ==============
@error(404)
def error404(error):
    return "404 error: file not found %s"%error
    
# =================
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
    # retrieve the json sent by browser
    data = request.json;
    
    # execute the MongoDB query, returning a list of the _id's that match
    if int(limit) <= 0:      # unlimited (limit = 0)
        id_list = [tweet for tweet in tweets.find(data,dict({"_id":1}))]
    else:                    # limited
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
    
    # convert from MongoDB bson to strict json and return the result
    result = bson.json_util.dumps(result)
    return result
       
@route('/findone/<id>', method="GET")
def findOne(id):
    # convert id to MongoDB _id
    mongo_id = bson.objectid.ObjectId(id)
    
    # execute the query
    tweet    = tweets.find_one({'_id': mongo_id})
    
    # package the query response
    result                = dict()
    result['first_tweet'] = tweet
    
    # convert from MongoDB bson to strict json and return the result
    result   = bson.json_util.dumps(result)
    return result
    
@route('/find/<id_list>', method="GET")
def find(id_list):
    # convert comma-delimited string into list of MongoDB '_id's
    mongo_id_list = map(bson.objectid.ObjectId, id_list.split(','))

    # query MongoDB for the list of '_id's
    result = tweets.find({'_id': { '$in': mongo_id_list}})
    
    # convert from MongoDB bson to strict json and return
    return bson.json_util.dumps(result)
    

# ===============================
# Send files from the root
# ===============================
"""
Templates are stored in the views folder.
index.tpl is the html shell and '% include' 
commands are used to pull in the various pieces
"""
@route('/')
def index():
    return template('index')
    
@route('/:path#.+#', name='root')
def static(path):
    return static_file(path, root=PATH)
    
    
# ===============================   
# Shutdown the MongoDB connection
# ===============================
@route('/exit')
def exit():
    connection.disconnect()
    return "MongoDB shut down"

# ==========================================   
# Connect to the MongoDB database at startup
# ==========================================

connection_string = "mongodb://localhost"
connection        = pymongo.MongoClient(connection_string)

db     = connection.HTA
tweets = db.grf

# =======================   
# Connect to the Internet
# =======================

bottle.debug(True)
bottle.run(host='localhost', port=8082, reloader=True)