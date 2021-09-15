from flask import Flask, request, redirect
from os import getenv
import string
import random
from flask_cors import cross_origin

from settings import host, port
from pymongo import MongoClient
from flask_pymongo import PyMongo

import time

# SET UP FLASK APP
app = Flask(__name__)
if getenv('DATABASE_URL'): # cloud
    client = MongoClient(getenv('DATABASE_URL'))
    db = client.test
elif (getenv('MONGO_INITDB_ROOT_USERNAME') and getenv('MONGO_INITDB_ROOT_PASSWORD')): # docker
    client = MongoClient(host='mongodb',
                            port=27017, 
                            username=getenv('MONGO_INITDB_ROOT_USERNAME'), 
                            password=getenv('MONGO_INITDB_ROOT_PASSWORD'),
                            authSource="admin")
    db = client["urls_db"]
else: # local
    client = PyMongo(app, uri="mongodb://localhost:27017/urls_db")
    db = client.db

# store = {}

# API Routes
@app.route('/<slug>', methods=['GET'])
def redirect_url(slug):
    # url = store.get(slug) # look up specified url using slug
    result = db.urls_tb.find_one({'slug': slug})
    if not result:
        return 'Slug not found'
    current_time = time.time()
    if current_time - result.get('last_accessed') > 10:
        return 'URL is deactivated due to inactivity.'
    db.urls_tb.update_one({
        'slug': slug,
    }, { "$set": { 'last_accessed': current_time } })
    return redirect(result.get('raw_url'), code=302) # redirects to the specified URL

@app.route('/', methods=['POST'])
@cross_origin([
    getenv('FRONTEND_URL_ONE'), getenv('FRONTEND_URL_TWO')
])
def generate_short_url():
    data = request.get_json()
    raw_url = data.get('url')
    new_id = id_generator() # generate unique slug
    current_time = time.time()
    # store[new_id] = raw_url # store as slug => raw_url
    db.urls_tb.insert_one({
        'slug': new_id,
        'raw_url': raw_url,
        'last_accessed': current_time,
    })
    return new_id

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    id = ''.join(random.choice(chars) for _ in range(size))
    # while (id in store):
    while (db.urls_tb.find_one({'slug': id})):
        id = ''.join(random.choice(chars) for _ in range(size))
    return id

@app.route('/', methods=['GET'])
def index():
    return 'Hello. This is the backend for the url shortening service.'

if __name__ == '__main__':
    app.run(host=host, port=port)
