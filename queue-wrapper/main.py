import os
import json
import redis
from flask import Flask, jsonify, request
import requests


app = Flask(__name__)

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
    QUEUE_NAME = 'queue:factoring'

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

@app.route('/<bucketname>/<objectname>', methods=['POST'])
def post_one(bucketname, objectname):
    body = {'bucket': bucketname,
            'object': objectname}

    json_packed = json.dumps(body)
    print('packed:', json_packed)
    RedisResource.conn.rpush(
        RedisResource.QUEUE_NAME,
        json_packed)
    
    return jsonify({'status': 'OK'})

@app.route('/<bucketname>', methods=['POST'])
def post_all(bucketname):
    r = requests.get("http://sos:5000/"+bucketname+"?list")
    if(r.status_code ==400):
        error_response = jsonify({'status': 'ERROR'})
        error_response.status_code = 400
        return error_response
    
    objects = (r.json()['objects'])

    for obj in objects:
        post_one(bucketname, obj['name'])
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)