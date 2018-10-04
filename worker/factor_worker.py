#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
# from make_thumbnail import makeGif as make_gif
import requests
import hashlib
from hashlib import md5

LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
QUEUE_NAME = 'queue:factoring'

INSTANCE_NAME = uuid.uuid4().hex

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def watch_queue(redis_conn, queue_name, callback_func, timeout=30):
    active = True

    while active:
        # Fetch a json-encoded task using a blocking (left) pop
        packed = redis_conn.blpop([queue_name], timeout=timeout)

        if not packed:
            # if nothing is returned, poll a again
            continue

        _, packed_task = packed

        # If it's treated to a poison pill, quit the loop
        if packed_task == b'DIE':
            active = False
        else:
            task = None
            try:
                 task = json.loads(packed_task)
            except Exception:
                LOG.exception('json.loads failed')
            if task:
                callback_func(task)

def execute_factor(log, task):
    bucketname,objectname  = task.get('bucket'), task.get('object')
    if bucketname and objectname:
        log.info('Downloading %s/%s', bucketname, objectname)
        r = requests.get("http://sos:5000/"+bucketname+"/"+objectname)
        if not os.path.exists(os.path.dirname("thumbnail/in.mp4")):
            try:
                os.makedirs(os.path.dirname("thumbnail/in.mp4"))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if not os.path.exists(os.path.dirname("thumbnail/out.gif")):
            try:
                os.makedirs(os.path.dirname("thumbnail/out.gif"))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open("thumbnail/in.mp4", "w+b") as in_file:
            in_file.write(r.content)
        # make_gif("thumbnail/in.mp4","thumbnail/out.gif")
        os.system("./make_thumbnail {} {}".format("thumbnail/in.mp4","thumbnail/out.gif"))
        if (requests.post("http://sos:5000/gifs?list").status_code==400):
            requests.post("http://sos:5000/gifs?create")
        requests.delete("http://sos:5000/gifs/"+bucketname+'_'+objectname+".gif?delete")
        requests.post("http://sos:5000/gifs/"+bucketname+'_'+objectname+".gif?create")
        out_file = open("thumbnail/out.gif", "rb")
        out_file_content = out_file.read()
        md5 = str(hashlib.sha1(out_file_content).hexdigest())
        partSize = len(out_file_content) 
        requests.put("http://sos:5000/gifs/"+bucketname+'_'+objectname+".gif?partNumber=1",data=open("thumbnail/out.gif", "rb"), headers={"Content-Length":str(partSize),
                                                                                                "Content-MD5":str(md5)})
        log.info("gifs/"+bucketname+'_'+objectname+".gif")
        requests.post("http://sos:5000/gifs/"+bucketname+'_'+objectname+".gif?complete")

    else:
        log.info('Invalid input.')
        

def main():
    LOG.info('Starting a worker...')
    LOG.info('Unique name: %s', INSTANCE_NAME)
    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    named_logging = LOG.getLogger(name=INSTANCE_NAME)
    named_logging.info('Trying to connect to %s [%s]', host, REDIS_QUEUE_LOCATION)
    redis_conn = redis.Redis(host=host, *port)
    watch_queue(
        redis_conn, 
        QUEUE_NAME, 
        lambda task_descr: execute_factor(named_logging, task_descr))

if __name__ == '__main__':
    main()
